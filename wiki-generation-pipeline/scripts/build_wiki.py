"""
Build complete self-contained HTML wiki from 34 markdown topic pages.
Usage: python scripts/build_wiki.py

Hash-manifest auto-detection for LTHP highlighting:
  - .lthp_state.json stores SHA-256 hashes of every source .md file
  - On each build, compares current hashes to manifest to classify cards:
    "new"       → file not in manifest (never seen before)
    "modified"  → hash changed since last build
    "original"  → hash unchanged
  - First build (empty manifest) treats every card as "new"
"""
import os, re, json, hashlib

WIKI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_DIR = os.path.join(WIKI_DIR, "de_wiki", "topics")
OUTPUT = os.path.join(WIKI_DIR, "output", "option_a", "index.html")
MANIFEST = os.path.join(WIKI_DIR, "de_wiki", ".lthp_state.json")

# ── Section definition (from output_map.md) ──
SECTIONS = [
    ("overview", "Data Engineering Scope", [
        ("Data Engineering Scope", "data_engineering_scope.md", "overview"),
        ("Modern Data Ecosystem", "modern_data_ecosystem.md", "overview"),
    ]),
    ("foundations", "Defining Data Engineering", [
        ("Practitioner Definitions", "defining_data_engineering.md", "foundations"),
        ("Evolution of Data Engineering", "evolution_of_data_engineering.md", "foundations"),
    ]),
    ("roles", "Data Roles & Responsibilities", [
        ("Data Roles Overview", "data_roles_overview.md", "roles"),
        ("DE Specializations", "data_engineering_specializations.md", "roles"),
        ("Role Comparisons Deep Dive", "role_comparisons_deep_dive.md", "roles"),
        ("Day in the Life", "day_in_the_life.md", "roles"),
    ]),
    ("skills", "Skills & Qualities", [
        ("Skill Taxonomy", "skills_and_responsibilities.md", "skills"),
        ("Practitioner Viewpoints", "practitioner_skills_viewpoints.md", "skills"),
    ]),
    ("ecosystem", "Data Ecosystem \u2014 Types, Sources & Languages", [
        ("Types of Data", "data_types.md", "ecosystem"),
        ("File Formats", "file_formats.md", "ecosystem"),
        ("Data Sources", "data_sources.md", "ecosystem"),
        ("Languages for Data Professionals", "languages_for_data_pros.md", "ecosystem"),
        ("Metadata Management", "metadata_management.md", "ecosystem"),
    ]),
    ("storage", "Data Storage & Repositories", [
        ("Data Repositories", "data_repositories.md", "storage"),
        ("Relational Databases", "relational_databases.md", "storage"),
        ("NoSQL Databases", "nosql_databases.md", "storage"),
        ("Data Warehouses, Lakes & Lakehouses", "data_warehouses_lakes.md", "storage"),
        ("Unstructured Data Storage", "unstructured_data_storage.md", "storage"),
    ]),
    ("processing", "Data Processing & Big Data Platforms", [
        ("ETL, ELT & Data Pipelines", "etl_elt_pipelines.md", "processing"),
        ("Data Integration Platforms", "data_integration_platforms.md", "processing"),
        ("Big Data Foundations", "big_data_foundations.md", "processing"),
        ("Hadoop Ecosystem", "hadoop_ecosystem.md", "processing"),
        ("Data Platform Architecture", "data_platform_architecture.md", "processing"),
        ("SQL Vendors & Dialects", "sql_vendors_dialects.md", "processing"),
    ]),
    ("quiz", "Quiz & Exam Reference", [
        ("Quiz Study Reference", "quiz_study_reference.md", "quiz"),
        ("Weakness Review", "checkpoint_weakness_review.md", "quiz"),
    ]),
    ("career", "Course & Career", [
        ("Course Syllabus & Index", "course_syllabus_and_index.md", "career"),
        ("16-Course Sequence", "course_sequence_16.md", "career"),
        ("Career Ladder & MVP", "career_ladder.md", "career"),
        ("Certification Roadmap", "certification_roadmap.md", "career"),
        ("Enhancement Modules", "enhancement_modules.md", "career"),
    ]),
]

# ── Hash manifest logic ──
def compute_status_map():
    """Return (status_map, new_manifest).

    status_map: {md_file: "new"|"modified"|"original"}
    new_manifest: {md_file: sha256_hex}
    """
    manifest = {}
    if os.path.exists(MANIFEST):
        try:
            with open(MANIFEST, encoding="utf-8") as f:
                manifest = json.load(f)
            if not isinstance(manifest, dict):
                raise ValueError("manifest root is not a dict")
        except (json.JSONDecodeError, OSError, ValueError):
            print("Warning: corrupt .lthp_state.json — treating as first build")
            manifest = {}

    status, new_manifest = {}, {}
    all_md_files = [md for _, _, cards in SECTIONS for _, md, _ in cards]

    for md_file in all_md_files:
        path = os.path.join(TOPICS_DIR, md_file)
        if not os.path.exists(path):
            status[md_file] = "original"
            continue
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        new_manifest[md_file] = h

        if md_file not in manifest:
            status[md_file] = "new"
        elif manifest[md_file] != h:
            status[md_file] = "modified"
        else:
            status[md_file] = "original"

    return status, new_manifest


# ── Markdown → HTML conversion ──
def md_to_html(text, card_id=""):
    """Convert markdown text to HTML, handling wiki-specific patterns."""
    lines = text.split('\n')
    html = []
    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []
    in_list = None
    list_buf = []
    in_blockquote = False
    quote_buf = []

    def close_list():
        nonlocal in_list, list_buf
        if in_list and list_buf:
            tag = 'ol' if in_list == 'ol' else 'ul'
            html.append(f'<{tag}>\n{"".join(list_buf)}\n</{tag}>')
            list_buf = []
            in_list = None

    def close_blockquote():
        nonlocal in_blockquote, quote_buf
        if in_blockquote:
            html.append(f'<blockquote>{"<br>".join(quote_buf)}</blockquote>\n')
            quote_buf = []
            in_blockquote = False

    def close_table():
        nonlocal in_table, table_buf
        if in_table:
            html.append('<table>\n')
            header = True
            for row in table_buf:
                cells = [c.strip() for c in row.split('|')]
                cells = [c for c in cells if c]
                if header:
                    html.append('<thead><tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr></thead>\n<tbody>\n')
                    header = False
                else:
                    if all(set(c) <= set('-: ') for c in cells):
                        continue
                    html.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n')
            html.append('</tbody>\n</table>\n')
            table_buf = []
            in_table = False

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith('```'):
            if in_code:
                close_table(); close_list(); close_blockquote()
                code_text = '\n'.join(code_buf)
                if code_buf and code_buf[0] == 'mermaid':
                    html.append(f'<div class="mermaid">{escape_html("\n".join(code_buf[1:]))}</div>\n')
                else:
                    html.append(f'<pre><code>{escape_html(code_text)}</code></pre>\n')
                code_buf = []
                in_code = False
            else:
                close_table(); close_list(); close_blockquote()
                lang = line.strip()[3:].strip()
                code_buf.append(lang if lang else '')
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if not line.strip():
            close_table(); close_list(); close_blockquote()
            html.append('\n')
            i += 1
            continue

        if line.strip().startswith('[Cross-ref:') or line.strip().startswith('[cross-ref:'):
            close_table(); close_list(); close_blockquote()
            ref = line.strip()
            m = re.match(r'\[(?:Cross-ref|cross-ref):\s*(.+?)(?:\s*\u2014\s*(.+))?\]', ref)
            if m:
                url = m.group(1).strip()
                text = m.group(2).strip() if m.group(2) else url
                html.append(f'<div class="cross-ref"><a href="#{url_to_anchor(url)}" class="cross-ref">{escape_html(text)}</a></div>\n')
            else:
                html.append(f'<div class="cross-ref">{escape_html(ref)}</div>\n')
            i += 1
            continue

        if line.strip().startswith('[LOW-RELEVANCE') or line.strip().startswith('[SUPERSEDED') or line.strip().startswith('[REDUNDANT'):
            close_table(); close_list(); close_blockquote()
            html.append(f'<div class="cross-ref">{escape_html(line.strip())}</div>\n')
            i += 1
            continue

        h_match = re.match(r'^(#{1,5})\s+(.+)$', line)
        if h_match:
            close_table(); close_list(); close_blockquote()
            level = len(h_match.group(1))
            title = h_match.group(2).strip()
            if level == 1 and not title.startswith('\u00a7'):
                i += 1
                continue
            html_level = min(level + 1, 6)
            html.append(f'<h{html_level}>{escape_html(title)}</h{html_level}>\n')
            i += 1
            continue

        if re.match(r'^-{3,}$', line.strip()):
            close_table(); close_list(); close_blockquote()
            html.append('<hr>\n')
            i += 1
            continue

        if line.strip().startswith('|') and line.strip().endswith('|'):
            in_blockquote = False
            in_table = True
            table_buf.append(line.strip())
            i += 1
            continue

        if line.strip().startswith('> '):
            close_table(); close_list()
            if not in_blockquote:
                in_blockquote = True
                quote_buf = []
            quote_buf.append(escape_html(re.sub(r'^>\s?', '', line.strip())))
            i += 1
            continue
        if line.strip() == '>':
            close_table(); close_list()
            if not in_blockquote:
                in_blockquote = True
                quote_buf = []
            quote_buf.append('')
            i += 1
            continue

        close_blockquote()

        ol_match = re.match(r'^\d+[.)]\s+(.+)$', line)
        if ol_match:
            close_table()
            if in_list != 'ol':
                close_list()
                in_list = 'ol'
            list_buf.append(f'<li>{inline_html(ol_match.group(1).strip())}</li>\n')
            i += 1
            continue

        ul_match = re.match(r'^[\-\*]\s+(.+)$', line)
        if ul_match:
            close_table()
            if in_list != 'ul':
                close_list()
                in_list = 'ul'
            list_buf.append(f'<li>{inline_html(ul_match.group(1).strip())}</li>\n')
            i += 1
            continue

        close_list()
        close_table()
        html.append(f'<p>{inline_html(line.strip())}</p>\n')
        i += 1

    close_list()
    close_blockquote()
    close_table()
    return ''.join(html)


def url_to_anchor(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text[:50]


def escape_html(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def inline_html(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def build_card_html(title, md_file, category):
    """Read a markdown file and convert to HTML card body (no outer div)."""
    filepath = os.path.join(TOPICS_DIR, md_file)
    if not os.path.exists(filepath):
        return f'<h3>{escape_html(title)}</h3><p><em>Content pending.</em></p>\n'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'^# .+\n?', '', content, count=1)
    content = re.sub(r'\n\*Source:.*?\*', '', content)
    return md_to_html(content)


# ── Build HTML sections ──
def build_toc():
    groups_html = []
    for section_id, section_title, cards in SECTIONS:
        links = ''.join(
            f'<a href="#{url_to_anchor(title)}" class="toc-link">{escape_html(title)}</a>\n'
            for title, _, _ in cards
        )
        groups_html.append(
            f'<div class="toc-group">\n<div class="toc-group-title">{escape_html(section_title)}</div>\n{links}</div>'
        )
    return '\n'.join(groups_html)


def build_sections(status_map):
    sections_html = []
    for section_id, section_title, cards in SECTIONS:
        cards_html = []
        for title, md_file, category in cards:
            body = build_card_html(title, md_file, category)
            anchor = url_to_anchor(title)

            st = status_map.get(md_file, "original")
            if st == "new":
                cls = "card lthp-highlight"
                tag = '<span class="tag green">NEW</span>'
            elif st == "modified":
                cls = "card lthp-highlight"
                tag = '<span class="tag amber">MODIFIED</span>'
            else:
                cls = "card"
                tag = ""

            # Inject tag at top of card body, after the first h3
            # If body doesn't start with h3, prepend one
            if not body.lstrip().startswith('<h3'):
                body = f'<h3>{escape_html(title)}</h3>\n{tag}\n{body}'
            else:
                # Insert tag right after opening h3 tag
                body = re.sub(r'(<h3>.*?</h3>)', lambda m: f'{m.group(1)}\n{tag}', body, count=1)

            cards_html.append(f'<div class="{cls}" id="{anchor}">\n{body}\n</div>')

        sections_html.append(
            f'<section class="category">\n<div class="category-header">\n<h2>{escape_html(section_title)}</h2>\n'
            f'<span class="category-count">{escape_html(category)}</span>\n</div>\n{"".join(cards_html)}\n</section>'
        )
    return '\n'.join(sections_html)


def build_glossary():
    """Parse glossary.md and build HTML table."""
    gpath = os.path.join(TOPICS_DIR, "glossary.md")
    if not os.path.exists(gpath):
        return ""
    with open(gpath, 'r', encoding='utf-8') as f:
        content = f.read()
    rows_html = []
    for line in content.split('\n'):
        if line.strip().startswith('|') and not line.strip().startswith('| Term') and not re.match(r'^\|[\s\-:]+\|', line):
            if 'Cross-ref' in line:
                continue
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]
            if len(parts) >= 2:
                term = escape_html(parts[0])
                defn = escape_html(parts[1])
                src = escape_html(parts[2]) if len(parts) > 2 else ''
                rows_html.append(f'<tr><td>{term}</td><td>{defn}</td><td>{src}</td></tr>\n')
    return f'''<section class="category" id="glossary">
<div class="category-header">
<h2>Consolidated Glossary</h2>
<span class="category-count">Reference</span>
</div>
<div class="card">
<p>{len(rows_html)} data engineering terms from all source files.</p>
<table>
<thead><tr><th>Term</th><th>Definition</th><th>Source Files</th></tr></thead>
<tbody>
{"".join(rows_html)}
</tbody>
</table>
<div class="cross-ref"><a href="#overview" class="cross-ref">All topic pages \u2014 this glossary consolidates terms from every source file</a></div>
</div>
</section>'''


def build_future():
    return """<section class="category" id="future">
<div class="category-header">
<h2>Coming Next \u2014 Modules 3\u201310</h2>
<span class="category-count">Preview</span>
</div>
<div class="future-card"><h3>Module 3 (Course 3) \u2014 Data Collection and Data Wrangling</h3><p>How to Gather and Import Data, Data Wrangling, Tools for Data Wrangling, CSV/Db2 lab exercises. <span class="tag">Course 1</span></p></div>
<div class="future-card"><h3>Module 4 (Course 3) \u2014 Querying Data, Performance Tuning, and Troubleshooting</h3><p>Querying and Analyzing Data, Performance Tuning and Troubleshooting, SQL exploration labs. <span class="tag">Course 1</span></p></div>
<div class="future-card"><h3>Module 5 (Course 3) \u2014 Governance and Compliance</h3><p>Governance frameworks, compliance regulations, DataOps methodology overview. <span class="tag">Course 1</span></p></div>
<div class="future-card"><h3>Courses 2\u201316 \u2014 Full IBM Certificate</h3><p>Python, SQL, Linux, DBA, ETL/Airflow/Kafka, Data Warehousing, BI, NoSQL, Big Data/Spark, ML, Capstone, GenAI, Career. See 16-Course Sequence card for details. <span class="tag">Full Track</span></p></div>
</section>"""


# ── CSS ──
CSS = """:root {
  --accent: #3b82f6;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --border: #334155;
  --bg-subtle: #1e293b;
  --bg-card: #0f172a;
  --bg-body: #0b1120;
  --shadow: 0 1px 2px rgba(0,0,0,0.04);
  --highlight-bg: rgba(234, 179, 8, 0.12);
  --highlight-border: rgba(234, 179, 8, 0.9);
}
html.light body {
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --border: #e2e8f0;
  --bg-subtle: #f8fafc;
  --bg-card: #ffffff;
  --bg-body: #ffffff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 1rem; line-height: 1.6;
  color: var(--text-primary); background: var(--bg-body);
}
.container { max-width: 960px; margin: 0 auto; padding: 0 24px; }
h1 { font-size: 2.25rem; font-weight: 700; line-height: 1.2; letter-spacing: -0.02em; }
h2 { font-size: 1.5rem; font-weight: 700; line-height: 1.3; margin: 0 0 16px; }
h3 { font-size: 1.15rem; font-weight: 600; line-height: 1.4; margin: 0 0 8px; }
h4 { font-size: 1.05rem; font-weight: 600; line-height: 1.4; margin: 16px 0 6px; }
h5 { font-size: 0.95rem; font-weight: 600; line-height: 1.4; margin: 12px 0 6px; color: var(--text-secondary); }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.doc-header { padding: 40px 0 24px; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
.doc-header h1 { margin-bottom: 8px; }
.doc-subtitle { color: var(--text-secondary); font-size: 1.05rem; margin-bottom: 16px; }
.doc-meta { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.meta-badge {
  font-size: 0.8rem; font-weight: 600;
  padding: 4px 12px; border-radius: 999px;
  background: var(--bg-subtle); border: 1px solid var(--border);
  color: var(--text-secondary);
}
.controls { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
.search-input {
  flex: 1; min-width: 200px;
  padding: 8px 14px; border: 1px solid var(--border);
  border-radius: 8px; font-size: 0.9rem;
  background: var(--bg-body); color: var(--text-primary);
}
.search-input:focus { outline: none; border-color: var(--accent); }
.dark-toggle {
  padding: 8px 16px; border: 1px solid var(--border);
  border-radius: 8px; cursor: pointer;
  font-size: 0.85rem; font-weight: 600;
  background: var(--bg-card); color: var(--text-primary);
  white-space: nowrap;
}
.dark-toggle:hover { background: var(--bg-subtle); }
.toc {
  background: var(--bg-subtle); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px; margin-bottom: 48px;
}
.toc-title {
  font-size: 0.85rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: var(--text-muted);
  margin-bottom: 16px; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
}
.toc-title::after { content: "\\25bc"; font-size: 0.7rem; }
.toc.collapsed .toc-title::after { content: "\\25b6"; }
.toc.collapsed .toc-body { display: none; }
.toc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.toc-group-title { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); margin-bottom: 6px; }
.toc-link {
  display: block; font-size: 0.85rem; color: var(--text-secondary);
  padding: 3px 0; transition: color 0.15s;
}
.toc-link:hover { color: var(--accent); text-decoration: none; }
.category { margin-bottom: 48px; }
.category-header {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 20px; padding-bottom: 8px;
  border-bottom: 2px solid var(--accent);
}
.category-header h2 { margin: 0; }
.category-count {
  font-size: 0.75rem; font-weight: 600; color: var(--text-muted);
  background: var(--bg-subtle); padding: 2px 10px;
  border-radius: 999px; border: 1px solid var(--border);
}
.card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px;
  box-shadow: var(--shadow); margin-bottom: 16px;
}
.lthp-highlight {
  box-shadow: inset 0 0 0 2px var(--highlight-border);
  background: var(--highlight-bg);
  border-radius: 4px;
  transition: background 0.3s ease;
}
table { width: 100%; border-collapse: collapse; font-size: 0.875rem; margin: 12px 0; }
th, td { padding: 8px 12px; border-bottom: 1px solid var(--border); text-align: left; }
th { font-weight: 600; color: var(--text-secondary); background: var(--bg-subtle); }
blockquote {
  border-left: 3px solid var(--accent);
  padding: 8px 16px; margin: 12px 0;
  color: var(--text-secondary);
  background: var(--bg-subtle);
  border-radius: 0 8px 8px 0;
  font-size: 0.9rem;
}
code {
  font-family: 'SF Mono', 'Fira Code', monospace;
  background: var(--bg-subtle); border-radius: 4px;
  padding: 2px 6px; font-size: 0.85rem;
}
pre {
  font-family: 'SF Mono', 'Fira Code', monospace;
  background: var(--bg-subtle); border-radius: 8px;
  padding: 12px 16px; overflow-x: auto;
  font-size: 0.85rem; margin: 12px 0;
}
ul, ol { padding-left: 20px; margin: 8px 0; }
li { margin-bottom: 4px; }
hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
.future-card {
  background: var(--bg-subtle); border: 1px dashed var(--border);
  border-radius: 12px; padding: 20px; margin-bottom: 12px;
  opacity: 0.6;
}
.future-card h3 { color: var(--text-muted); }
.future-card p { color: var(--text-muted); font-size: 0.85rem; }
.cross-ref {
  font-size: 0.8rem; color: var(--text-muted);
  margin-top: 8px;
}
.tag {
  display: inline-block; font-size: 0.7rem; font-weight: 600;
  padding: 2px 8px; border-radius: 999px;
  background: rgba(37,99,235,0.1); color: var(--accent);
  margin-right: 4px;
  margin-bottom: 8px;
}
.tag.green { background: rgba(22,163,74,0.1); color: #16a34a; }
.tag.amber { background: rgba(217,119,6,0.1); color: #d97706; }
.tag.purple { background: rgba(139,92,246,0.1); color: #8b5cf6; }
.search-highlight { background: rgba(234,179,8,0.25); border-radius: 2px; }
footer {
  margin-top: 48px; padding: 24px 0;
  border-top: 1px solid var(--border);
  text-align: center; font-size: 0.8rem; color: var(--text-muted);
}
@media (max-width: 768px) {
  h1 { font-size: 1.6rem; }
  h2 { font-size: 1.25rem; }
  .toc-grid { grid-template-columns: 1fr; }
  .container { padding: 0 16px; }
  .doc-header { padding: 24px 0 16px; }
}
@media (max-width: 480px) {
  table { font-size: 0.75rem; }
  th, td { padding: 6px 8px; }
  .controls { flex-direction: column; }
  .search-input { min-width: 100%; }
}"""


# ── JavaScript ──
JS = """(() => {
  const toggle = document.getElementById('darkToggle');
  const stored = localStorage.getItem('de-wiki-light');
  if (stored === 'true') { document.documentElement.classList.add('light'); toggle.textContent = 'Dark Mode'; }
  toggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('light');
    const isLight = document.documentElement.classList.contains('light');
    localStorage.setItem('de-wiki-light', isLight);
    toggle.textContent = isLight ? 'Dark Mode' : 'Light Mode';
  });
  const tocToggle = document.getElementById('tocToggle');
  const toc = document.getElementById('toc');
  tocToggle.addEventListener('click', () => { toc.classList.toggle('collapsed'); });
  const input = document.getElementById('searchInput');
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();
    const cards = document.querySelectorAll('.card, .future-card');
    if (!q) {
      cards.forEach(c => { c.style.display = ''; });
      document.querySelectorAll('.category').forEach(s => { s.style.display = ''; });
      return;
    }
    cards.forEach(c => {
      const text = c.textContent.toLowerCase();
      c.style.display = text.includes(q) ? '' : 'none';
    });
    document.querySelectorAll('.category').forEach(s => {
      const visible = Array.from(s.querySelectorAll('.card, .future-card')).some(c => c.style.display !== 'none');
      s.style.display = visible ? '' : 'none';
    });
  });
})();"""


# ── Main ──
def main():
    # Compute status from hash manifest
    status_map, new_manifest = compute_status_map()

    toc_html = build_toc()
    sections_html = build_sections(status_map)
    glossary_html = build_glossary()
    future_html = build_future()

    total_cards = sum(len(cards) for _, _, cards in SECTIONS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="dark light">
<title>Data Engineering Wiki</title>
<script>if(localStorage.getItem('de-wiki-light')==='true'){{document.documentElement.classList.add('light')}}</script>
<style>
{CSS}
</style>
</head>
<body>
<div class="container">

<header class="doc-header">
  <h1>Data Engineering Wiki</h1>
  <p class="doc-subtitle">Technical reference covering the IBM Data Engineering Professional Certificate \u2014 Modules 1 &amp; 2 in depth, plus the full 16-course career blueprint.</p>
  <div class="doc-meta">
    <span class="meta-badge">{total_cards} Topic Cards</span>
    <span class="meta-badge">{len(SECTIONS)} Categories</span>
    <span class="meta-badge">63 Source Files</span>
  </div>
  <div class="controls">
    <input type="text" class="search-input" id="searchInput" placeholder="Search topics, roles, tools, or concepts...">
    <button class="dark-toggle" id="darkToggle">Light Mode</button>
  </div>
</header>

<nav class="toc" id="toc">
  <div class="toc-title" id="tocToggle">Contents</div>
  <div class="toc-body">
    <div class="toc-grid">
{toc_html}
    </div>
  </div>
</nav>

{sections_html}

{glossary_html}

{future_html}

<footer>
  <p>Generated from IBM Data Engineering Professional Certificate source files. 63 source files, {total_cards} topic cards.</p>
</footer>

</div>

<script>{JS}</script>

</body>
</html>"""

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)

    # Write manifest only on success
    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(new_manifest, f, indent=2)

    new_count = sum(1 for v in status_map.values() if v == "new")
    mod_count = sum(1 for v in status_map.values() if v == "modified")
    orig_count = total_cards - new_count - mod_count

    file_size = os.path.getsize(OUTPUT)
    print(f"Written: {OUTPUT}")
    print(f"Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"Cards: {total_cards} (NEW: {new_count}, MODIFIED: {mod_count}, ORIGINAL: {orig_count})")


if __name__ == '__main__':
    main()
