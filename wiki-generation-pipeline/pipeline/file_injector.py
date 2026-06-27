"""Inject file_contents from an XML description into a Markdown template.

Usage example:
  python file_injector.py --xml files.xml --template initial_servant_ai_meta_full_prompt_template.md \
	--output initial_servant_ai_meta_full_prompt.md --backup

The script looks for XML elements that describe a file path and a corresponding
`file_contents` element or attribute. For each entry whose path exists on disk,
the script replaces placeholders in the template of the form
`{{INJECT:PATH}}` (PATH can be the original path, normalized absolute path, or
basename) or regions marked with
`<!-- INJECT path="PATH" -->...<!-- END INJECT -->` with the provided
`file_contents` text. The resulting output overwrites the given output file.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import shutil
import sys
import html
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple


def find_entries(root: ET.Element) -> List[Dict[str, str]]:
	entries: List[Dict[str, str]] = []
	# Prefer <file> elements but be forgiving for other layouts
	for file_el in root.findall('.//file'):
		path = file_el.get('path')
		if path is None:
			p_el = file_el.find('path')
			path = p_el.text if p_el is not None and p_el.text is not None else None

		# file_contents may be an element or an attribute
		fc_el = file_el.find('file_contents') or file_el.find('contents') or file_el.find('content')
		if fc_el is not None:
			file_contents = ''.join(fc_el.itertext())
		else:
			file_contents = file_el.get('file_contents')

		if path:
			entries.append({'path': path.strip(), 'file_contents': file_contents or ''})

	# Also search for any element that contains both a path child and file_contents child
	for el in root.iter():
		if el.tag == 'file':
			continue
		p = el.find('path')
		fc = el.find('file_contents')
		if p is not None and fc is not None and p.text:
			entries.append({'path': p.text.strip(), 'file_contents': ''.join(fc.itertext())})

	# Deduplicate by path (first occurrence wins)
	seen = set()
	out: List[Dict[str, str]] = []
	for e in entries:
		if e['path'] in seen:
			continue
		seen.add(e['path'])
		out.append(e)
	return out


def normalize(path: str, base_dir: str) -> str:
	p = path.strip()
	p = os.path.expanduser(p)
	if not os.path.isabs(p):
		p = os.path.normpath(os.path.join(base_dir, p))
	else:
		p = os.path.normpath(p)
	return p


def load_xml(xml_path: str) -> ET.Element:
	tree = ET.parse(xml_path)
	return tree.getroot()


def inject_file_system_path_blocks(template_text: str, tpl_path: str) -> Tuple[str, int]:
	pattern = re.compile(
		r'(<file_system_path>\s*(?P<path>.*?)\s*</file_system_path>\s*<file_content\b[^>]*>)(?P<inner>.*?)(</file_content>)',
		flags=re.S)
	injected = 0

	def _repl(m: re.Match) -> str:
		path = m.group('path').strip()
		norm = normalize(path, os.path.dirname(tpl_path))
		if not os.path.exists(norm):
			logging.warning('Referenced path does not exist, skipping: %s', norm)
			return m.group(0)
		try:
			with open(norm, 'r', encoding='utf-8') as ff:
				contents = ff.read()
		except Exception as exc:
			logging.warning('Failed to read %s: %s', norm, exc)
			return m.group(0)
		nonlocal injected
		injected += 1
		return m.group(1) + contents + m.group(4)

	new_text = pattern.sub(_repl, template_text)
	return new_text, injected


def inject(template_text: str, mapping: Dict[str, Tuple[str, str]]) -> str:
	"""Replace placeholders in template_text using mapping.

	mapping: original_path -> (normalized_path, file_contents)
	"""
	text = template_text
	for orig, (norm, contents) in mapping.items():
		# try several placeholder forms
		candidates = [orig, norm, os.path.basename(norm)]
		for key in candidates:
			placeholder = '{{INJECT:%s}}' % key
			if placeholder in text:
				text = text.replace(placeholder, contents)

		# region replacement: <!-- INJECT path="..." --> ... <!-- END INJECT -->
		pattern = re.compile(r'<!--\s*INJECT\s+path=["\']%s["\']\s*-->.*?<!--\s*END\s+INJECT\s*-->' % re.escape(orig), flags=re.S)
		text = pattern.sub(lambda _m, c=contents: c, text)
		pattern2 = re.compile(r'<!--\s*INJECT\s+path=["\']%s["\']\s*-->.*?<!--\s*END\s+INJECT\s*-->' % re.escape(norm), flags=re.S)
		text = pattern2.sub(lambda _m, c=contents: c, text)

	return text


def validate_output(text: str, mapping: Dict[str, Tuple[str, str]]) -> Tuple[bool, List[str]]:
	"""Basic validation: check no unreplaced placeholders remain and mapping non-empty.

	Returns (ok, issues)
	"""
	issues: List[str] = []
	if not mapping:
		issues.append('No entries were injected (mapping is empty)')

	if '{{INJECT:' in text:
		issues.append('Unreplaced placeholder(s) detected: "{{INJECT:" remains in output')

	# Optionally check for common malformed XML remnants
	if '<file>' in text and '</file>' in text:
		issues.append('Raw <file> tags found in output; check XML parsing')

	return (len(issues) == 0, issues)


def main() -> None:
	parser = argparse.ArgumentParser(description='Inject file_contents from XML into a template')
	parser.add_argument('--xml', '-x', required=False, help='Path to XML file describing injections (optional)')
	parser.add_argument('--template', '-t', default='initial_servant_ai_meta_full_prompt_template.md')
	parser.add_argument('--output', '-o', default='initial_servant_ai_meta_full_prompt.md')
	parser.add_argument('--workspace-base', '-b', default='.', help='Base dir for resolving relative paths')
	parser.add_argument('--backup', action='store_true', help='Make a .bak copy of the existing output file')
	parser.add_argument('--test', action='store_true', help='Write test output to a temporary testing file named testing_output')
	parser.add_argument('--testing-name', default='testing_output.md', help='Filename to use for test output')
	parser.add_argument('--auto-commit', action='store_true', help='After successful validation, also write the final output file')
	args = parser.parse_args()

	logging.basicConfig(level=logging.INFO, format='%(message)s')

	# If an explicit XML file is provided, use the original behavior.
	if args.xml:
		if not os.path.exists(args.xml):
			logging.error('XML file not found: %s', args.xml)
			sys.exit(2)

		root = load_xml(args.xml)
		entries = find_entries(root)
		base_dir = os.path.abspath(args.workspace_base)

		mapping: Dict[str, Tuple[str, str]] = {}
		for e in entries:
			orig_path = e['path']
			norm = normalize(orig_path, base_dir)
			if os.path.exists(norm):
				logging.info('Found path: %s', norm)
				mapping[orig_path] = (norm, e.get('file_contents', '') or '')
			else:
				logging.warning('Path not found, skipping injection: %s', norm)

		if not os.path.exists(args.template):
			logging.error('Template file not found: %s', args.template)
			sys.exit(3)

		with open(args.template, 'r', encoding='utf-8') as fh:
			template_text = fh.read()

		new_text = inject(template_text, mapping)
	else:
		# Autonomous mode: locate the template, find embedded <file>...</file> blocks,
		# fill their <file_contents> from the filesystem paths, and write the output.
		def find_template_file(name: str) -> str | None:
			# Search current directory and parent directories up to filesystem root
			cur = os.path.abspath(os.getcwd())
			while True:
				cand = os.path.join(cur, name)
				if os.path.exists(cand):
					return cand
				parent = os.path.dirname(cur)
				if parent == cur:
					break
				cur = parent
			return None

		tpl_path = find_template_file(args.template)
		if not tpl_path:
			logging.error('Template file not found in cwd or parent: %s', args.template)
			sys.exit(3)

		with open(tpl_path, 'r', encoding='utf-8') as fh:
			template_text = fh.read()

		mapping: Dict[str, Tuple[str, str]] = {}

		# First: try a regex-based injection for <file_system_path> blocks so the
		# template can still be processed even when the surrounding file is not
		# fully valid XML.
		new_text, injected_count = inject_file_system_path_blocks(template_text, tpl_path)
		if injected_count:
			logging.info('Injected %d <file_system_path> block(s) via regex fallback', injected_count)

		# Second: try to parse template as XML fragment and inject for tags that contain
		# <file_system_path> children, writing their file contents into <file_content>
		try:
			wrapped = '<root>' + template_text + '</root>'
			rootfrag = ET.fromstring(wrapped)
		except ET.ParseError:
			rootfrag = None

		if rootfrag is not None:
			for child in list(rootfrag):
				fsp = child.find('file_system_path')
				if fsp is None or fsp.text is None:
					continue
				path = fsp.text.strip()
				base_dir = os.path.dirname(tpl_path)
				norm = normalize(path, base_dir)
				if not os.path.exists(norm):
					logging.warning('Referenced path does not exist, skipping: %s', norm)
					continue
				try:
					with open(norm, 'r', encoding='utf-8') as ff:
						contents = ff.read()
				except Exception as exc:
					logging.warning('Failed to read %s: %s', norm, exc)
					continue

				fc = child.find('file_content')
				if fc is None:
					fc = ET.SubElement(child, 'file_content')
				# If contents looks like XML, parse and insert as child elements so
				# serialization preserves tags instead of escaping angle brackets.
				try:
					unescaped = html.unescape(contents)
					frag = ET.fromstring('<root>' + unescaped + '</root>')
					# remove any existing children/text
					for sub in list(fc):
						fc.remove(sub)
					fc.text = None
					for sub in list(frag):
						fc.append(sub)
				except ET.ParseError:
					# If whole-content parsing fails, try to find XML-like blocks inside
					unescaped = html.unescape(contents)
					block_re = re.compile(r'(<([A-Za-z0-9_:-]+)[^>]*>.*?</\2>)', flags=re.S)
					matches = list(block_re.finditer(unescaped))
					if not matches:
						fc.text = contents
					else:
						# Clear existing children and interleave text and parsed elements
						for sub in list(fc):
							fc.remove(sub)
						start = 0
						if matches[0].start() > 0:
							fc.text = unescaped[0:matches[0].start()]
						for i, mm in enumerate(matches):
							frag_text = mm.group(1)
							try:
								elem = ET.fromstring(frag_text)
							except ET.ParseError:
								# fallback: append as text
								if fc.text is None:
									fc.text = frag_text
								else:
									# append to last child's tail or fc.text
									if len(fc):
										last = fc[-1]
										last.tail = (last.tail or '') + frag_text
									else:
										fc.text += frag_text
								continue
							# append parsed element
							fc.append(elem)
							# set tail to text between this match end and next match start (or remainder)
							next_start = matches[i+1].start() if i+1 < len(matches) else len(unescaped)
							elem.tail = unescaped[mm.end():next_start]

				# replace original block in template with updated XML for this child
				tag = child.tag
				orig_pattern = re.compile(r'(<%s\b.*?>.*?</%s>)' % (re.escape(tag), re.escape(tag)), flags=re.S)
				# replace first occurrence only
				new_block = ET.tostring(child, encoding='unicode')
				def _repl(m, inner=unescaped):
					matched = m.group(1)
					# replace inner <file_content>...</file_content> with raw unescaped content
					inner_pattern = re.compile(r'(<file_content\b[^>]*>).*?(</file_content>)', flags=re.S)
					if inner_pattern.search(matched):
						return inner_pattern.sub(lambda mm: mm.group(1) + inner + mm.group(2), matched, count=1)
					# fallback
					return matched
				new_text, nsub = orig_pattern.subn(_repl, new_text, count=1)
				if nsub:
					logging.info('Injected content for tag <%s> from %s', tag, norm)
					injected_count += 1

		else:
			# couldn't parse as XML fragment; fall back to previous <file> block search
			file_block_re = re.compile(r'(<file\b.*?>.*?</file>)', flags=re.S)
			matches = list(file_block_re.finditer(new_text))
			if not matches:
				if injected_count == 0:
					logging.info('No embedded <file> blocks found in template; nothing to inject')
			else:
				for m in matches:
					block = m.group(1)
					try:
						el = ET.fromstring(block)
					except ET.ParseError:
						logging.warning('Skipping malformed XML block')
						continue

					# determine path from attribute or child
					path = el.get('path')
					if not path:
						p_el = el.find('path')
						path = p_el.text if p_el is not None and p_el.text is not None else None

					if not path:
						logging.warning('No path found in embedded <file> block; skipping')
						continue

					base_dir = os.path.dirname(tpl_path)
					norm = normalize(path, base_dir)
					if not os.path.exists(norm):
						logging.warning('Referenced path does not exist, skipping: %s', norm)
						continue

					# read file contents
					try:
						with open(norm, 'r', encoding='utf-8') as ff:
							contents = ff.read()
					except Exception as exc:
						logging.warning('Failed to read %s: %s', norm, exc)
						continue

					# find or create file_contents child
					fc = el.find('file_contents')
					if fc is None:
						fc = ET.SubElement(el, 'file_contents')
					# If contents looks like XML, insert as child elements so tags aren't escaped
					try:
						unescaped = html.unescape(contents)
						frag = ET.fromstring('<root>' + unescaped + '</root>')
						for sub in list(fc):
							fc.remove(sub)
						fc.text = None
						for sub in list(frag):
							fc.append(sub)
					except ET.ParseError:
						# try to salvage XML-like blocks inside the contents
						unescaped = html.unescape(contents)
						block_re = re.compile(r'(<([A-Za-z0-9_:-]+)[^>]*>.*?</\2>)', flags=re.S)
						matches = list(block_re.finditer(unescaped))
						if not matches:
							fc.text = contents
						else:
							for sub in list(fc):
								fc.remove(sub)
							if matches[0].start() > 0:
								fc.text = unescaped[0:matches[0].start()]
							for i, mm in enumerate(matches):
								frag_text = mm.group(1)
								try:
									elem = ET.fromstring(frag_text)
								except ET.ParseError:
									if fc.text is None:
										fc.text = frag_text
									else:
										if len(fc):
											last = fc[-1]
											last.tail = (last.tail or '') + frag_text
										else:
											fc.text += frag_text
									continue
								fc.append(elem)
								next_start = matches[i+1].start() if i+1 < len(matches) else len(unescaped)
								elem.tail = unescaped[mm.end():next_start]

					# replace original block in template with updated XML
					new_block = ET.tostring(el, encoding='unicode')
					new_text = new_text.replace(block, new_block)
		# Also handle simple placeholders of the form {{INJECT:relative/path}}
		# and comment-region injections <!-- INJECT path="..." -->...<!-- END INJECT -->
		# placeholders
		ph_re = re.compile(r'\{\{INJECT:([^}]+)\}\}')
		for m in set(ph_re.findall(new_text)):
			path = m.strip()
			norm = normalize(path, os.path.dirname(tpl_path))
			if os.path.exists(norm):
				try:
					with open(norm, 'r', encoding='utf-8') as ff:
						contents = ff.read()
				except Exception as exc:
					logging.warning('Failed to read %s: %s', norm, exc)
					continue
				# replace all matching placeholders for this path
				new_text = new_text.replace('{{INJECT:%s}}' % path, contents)
				injected_count += 1

		# region comments
		region_re = re.compile(r'<!--\s*INJECT\s+path=["\']([^"\']+)["\']\s*-->.*?<!--\s*END\s+INJECT\s*-->', flags=re.S)
		for m in list(region_re.finditer(new_text)):
			path = m.group(1).strip()
			norm = normalize(path, os.path.dirname(tpl_path))
			if not os.path.exists(norm):
				logging.warning('Referenced path does not exist for region injection, skipping: %s', norm)
				continue
			try:
				with open(norm, 'r', encoding='utf-8') as ff:
					contents = ff.read()
			except Exception as exc:
				logging.warning('Failed to read %s: %s', norm, exc)
				continue
			# replace the whole region with the file contents
			new_text = new_text[:m.start()] + contents + new_text[m.end():]
			injected_count += 1

		# Track mapping count for logging/validation
		if injected_count:
			mapping = {f'injected_{i}': (tpl_path, '') for i in range(injected_count)}


		# After autonomous injection, set output path relative to tpl_path directory
		if hasattr(args, 'output') and args.output:
			args.output = os.path.join(os.path.dirname(tpl_path), os.path.basename(args.output))
		else:
			args.output = os.path.join(os.path.dirname(tpl_path), 'initial_servant_ai_meta_full_prompt.md')
		# default to backing up existing output to be safe
		if not hasattr(args, 'backup'):
			args.backup = True



	# If test mode, write to testing file first
	if args.test:
		testing_path = args.testing_name
		with open(testing_path, 'w', encoding='utf-8') as fh:
			fh.write(new_text)
		logging.info('Wrote test output: %s', testing_path)

		ok, issues = validate_output(new_text, mapping)
		if ok:
			logging.info('Validation passed for test output')
			if args.auto_commit:
				if os.path.exists(args.output) and args.backup:
					shutil.copy2(args.output, args.output + '.bak')
				with open(args.output, 'w', encoding='utf-8') as fh:
					fh.write(new_text)
				logging.info('Auto-committed final output: %s', args.output)
		else:
			logging.error('Validation failed for test output:')
			for it in issues:
				logging.error('- %s', it)
			logging.info('Final output not written. Fix issues and re-run with --auto-commit to commit.')
	else:
		if os.path.exists(args.output) and args.backup:
			shutil.copy2(args.output, args.output + '.bak')
		with open(args.output, 'w', encoding='utf-8') as fh:
			fh.write(new_text)
		logging.info('Wrote output: %s', args.output)
		logging.info('Injected %d entries', len(mapping))


if __name__ == '__main__':
	main()

