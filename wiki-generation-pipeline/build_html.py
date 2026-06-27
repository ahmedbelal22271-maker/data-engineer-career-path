"""Regenerate output/option_a/index.html from de_wiki/topics/*.md"""

import re
import os

def md_to_html(text):
    """Simple markdown-to-HTML conversion for the subset we use."""
    lines = text.split('\n')
    out = []
    i = 0
    in_table = False
    in_list = False
    in_ol = False
    in_code = False
    code_buf = []

    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith('```'):
            if in_code:
                out.append('<pre>' + ''.join(code_buf) + '</pre>')
                code_buf = []
                in_code = False
                i += 1
                continue
            else:
                in_code = True
                i += 1
                continue
        if in_code:
            code_buf.append(line + '\n')
            i += 1
            continue

        # Close lists if needed
        if in_list and not line.startswith('- ') and not line.startswith('* ') and line.strip():
            out.append('</ul>')
            in_list = False
        if in_ol and not re.match(r'^\d+\. ', line) and line.strip():
            out.append('</ol>')
            in_ol = False

        # Tables
        if line.strip().startswith('|') and line.strip().endswith('|'):
            cells = fmt_cells([c.strip() for c in line.strip().strip('|').split('|')])
            if not in_table:
                out.append('<table>')
                in_table = True
                is_header = True
                # Check if next line is separator row
                if i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1]):
                    out.append('<thead><tr>')
                    for c in cells:
                        out.append(f'<th>{c}</th>')
                    out.append('</tr></thead><tbody>')
                    i += 2  # skip separator
                    continue
                else:
                    out.append('<tr>')
                    for c in cells:
                        out.append(f'<td>{c}</td>')
                    out.append('</tr>')
            else:
                out.append('<tr>')
                for c in cells:
                    out.append(f'<td>{c}</td>')
                out.append('</tr>')
            i += 1
            # Check if next line breaks table
            if i >= len(lines) or not (lines[i].strip().startswith('|') and lines[i].strip().endswith('|')):
                out.append('</tbody></table>')
                in_table = False
            continue
        elif in_table:
            out.append('</tbody></table>')
            in_table = False

        # Skip separator row for tables
        if re.match(r'^\|[\s\-:|]+\|$', line):
            i += 1
            continue

        s = line.strip()
        if not s:
            out.append('')
            i += 1
            continue

        # Cross-ref: render as clickable link
        if s.startswith('[Cross-ref:') or s.startswith('[REDUNDANT'):
            rendered = convert_cross_ref(s)
            out.append(f'<div class="cross-ref">{rendered}</div>')
            i += 1
            continue

        # Horizontal rule
        if s == '---':
            out.append('<hr>')
            i += 1
            continue

        # Inline formatting helper
        def fmt(text):
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
            return text

        # Table cell content
        def fmt_cells(cells):
            return [fmt(c) for c in cells]

        # Blockquote
        if s.startswith('> '):
            content = fmt(s[2:])
            out.append(f'<blockquote>{content}</blockquote>')
            i += 1
            continue

        # Headings
        h_match = re.match(r'^(#{1,4})\s+(.+)$', s)
        if h_match:
            level = len(h_match.group(1))
            content = h_match.group(2)
            if level == 1:
                out.append(f'<h1>{content}</h1>')
            elif level == 2:
                out.append(f'<h3>{content}</h3>')  # Use h3 inside cards for h2
            elif level == 3:
                out.append(f'<h4>{content}</h4>')
            else:
                out.append(f'<h5>{content}</h5>')
            i += 1
            continue

        # Unordered list
        if s.startswith('- ') or s.startswith('* '):
            if not in_list:
                out.append('<ul>')
                in_list = True
            content = fmt(re.sub(r'^[-*]\s+', '', s))
            out.append(f'<li>{content}</li>')
            i += 1
            continue

        # Ordered list
        ol_match = re.match(r'^(\d+)\.\s+(.+)$', s)
        if ol_match:
            if not in_ol:
                out.append('<ol>')
                in_ol = True
            out.append(f'<li>{fmt(ol_match.group(2))}</li>')
            i += 1
            continue

        # Inline formatting for paragraphs
        s = fmt(s)

        # Regular paragraph
        out.append(f'<p>{s}</p>')
        i += 1

    if in_table:
        out.append('</tbody></table>')
    if in_list:
        out.append('</ul>')
    if in_ol:
        out.append('</ol>')

    return '\n'.join(out)


def extract_section(md_text):
    """Extract the main content body from a markdown file (skip the H1 title)."""
    lines = md_text.split('\n')
    # Skip the H1 title line
    body = []
    for line in lines:
        if line.startswith('# ') and not body:
            continue  # skip title
        body.append(line)
    return '\n'.join(body)


# Mapping: section_id -> topic file
SECTIONS = {
    'scope': 'data_engineering_scope.md',
    'ecosystem': 'modern_data_ecosystem.md',
    'defining': 'defining_data_engineering.md',
    'evolution': 'evolution_of_data_engineering.md',
    'roles-overview': 'data_roles_overview.md',
    'specializations': 'data_engineering_specializations.md',
    'comparisons': 'role_comparisons_deep_dive.md',
    'day-in-life': 'day_in_the_life.md',
    'skills': 'skills_and_responsibilities.md',
    'viewpoints': 'practitioner_skills_viewpoints.md',
    'quiz': 'quiz_study_reference.md',
    'weakness': 'checkpoint_weakness_review.md',
    'syllabus': 'course_syllabus_and_index.md',
    'career-ladder': 'career_ladder.md',
    'certifications': 'certification_roadmap.md',
    'course-seq': 'course_sequence_16.md',
    'enhancements': 'enhancement_modules.md',
}

# Reverse mapping: topic filename -> section anchor id
FILE_TO_ANCHOR = {v: k for k, v in SECTIONS.items()}
FILE_TO_ANCHOR['glossary.md'] = 'glossary'

# Cross-ref pattern: [Cross-ref: topics/FILE.md — description]
CROSS_REF_RE = re.compile(r'\[Cross-ref:\s*topics/([^\]]+\.md)\s*[—–-]\s*(.+)\]')

def convert_cross_ref(text: str) -> str:
    """Convert [Cross-ref: topics/FILE.md — description] to <a href="#anchor">description</a>."""
    def _repl(m):
        filename = m.group(1)
        desc = m.group(2).strip().rstrip(']')
        anchor = FILE_TO_ANCHOR.get(filename)
        if anchor:
            return f'<a href="#{anchor}" class="cross-ref">{desc}</a>'
        else:
            return f'<span class="cross-ref">[Cross-ref: topics/{filename} — {desc}]</span>'
    return CROSS_REF_RE.sub(_repl, text)

BASE = os.path.dirname(os.path.abspath(__file__))
TOPICS_DIR = os.path.join(BASE, 'de_wiki', 'topics')
HTML_PATH = os.path.join(BASE, 'output', 'option_a', 'index.html')

# Read existing HTML
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# For each section, extract the markdown content, convert to HTML, and inject
for sec_id, topic_file in SECTIONS.items():
    md_path = os.path.join(TOPICS_DIR, topic_file)
    if not os.path.exists(md_path):
        continue

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    body_md = extract_section(md_text)

    # Separate cross-references from main body
    lines = body_md.split('\n')
    main_lines = []
    ref_lines = []
    for line in lines:
        if line.strip().startswith('[Cross-ref:') or line.strip().startswith('[REDUNDANT'):
            ref_lines.append(line.strip())
        else:
            main_lines.append(line)

    html_body = md_to_html('\n'.join(main_lines))

    if ref_lines:
        html_body += '\n'
        for ref_line in ref_lines:
            rendered = convert_cross_ref(ref_line)
            html_body += f'<div class="cross-ref">{rendered}</div>\n'

    # Find the section in HTML and replace the card content
    # Pattern: <section class="category" id="SEC_ID"> ... <div class="card"> ... </div>
    start_pattern = f'<section class="category" id="{sec_id}">'
    start_idx = html.find(start_pattern)
    if start_idx == -1:
        continue

    # Find the <div class="card"> inside this section
    card_start = html.find('<div class="card">', start_idx)
    # Or future-card
    future_card = html.find('<div class="future-card">', start_idx)
    if card_start == -1 and future_card == -1:
        continue

    if card_start != -1:
        # Find end of this card's </div> (matching depth)
        depth = 0
        card_content_start = card_start + len('<div class="card">')
        # Find the closing </div> that ends this card
        pos = card_content_start
        while pos < len(html):
            if html[pos:pos+5] == '<div ' or html[pos:pos+6] == '<div class':
                depth += 1
                pos += 1
            elif html[pos:pos+6] == '</div>':
                if depth == 0:
                    card_end = pos + 6
                    break
                depth -= 1
                pos += 1
            else:
                pos += 1
        else:
            continue  # didn't find end

        new_card = f'<div class="card lthp-highlight">\n{html_body}\n</div>'
        html = html[:card_start] + new_card + html[card_end:]
    elif future_card != -1:
        # future cards handled differently - just skip them
        pass

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Regenerated {HTML_PATH}")
