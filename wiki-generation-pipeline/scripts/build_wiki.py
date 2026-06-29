"""
Build complete self-contained HTML wiki with SPA page navigation.
Usage: python scripts/build_wiki.py

Features:
  - Hash-manifest LTHP auto-detection (NEW / MODIFIED / ORIGINAL)
  - SPA page navigation (one section at a time, hash-routed)
  - Fixed left sidebar with section links
  - Working cross-reference links (filename-to-anchor mapping)
  - Content cleaning (strips course-ware artifacts)
  - LOW-RELEVANCE / SUPERSEDED / REDUNDANT as styled semantic blocks
  - Glossary tracked in manifest for highlighting
"""
import os, re, json, hashlib

WIKI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_DIR = os.path.join(WIKI_DIR, "de_wiki", "topics")
OUTPUT = os.path.join(WIKI_DIR, "wiki.html")
OUTPUT_OPTION_A = os.path.join(WIKI_DIR, "output", "option_a", "index.html")
MANIFEST = os.path.join(WIKI_DIR, "de_wiki", ".lthp_state.json")

# ── Section definition ──
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
    ("ecosystem", "Data Ecosystem — Types, Sources & Languages", [
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
    ("governance", "Data Lifecycle & Governance", [
        ("DataOps Methodology", "dataops_methodology.md", "governance"),
        ("Governance & Compliance", "governance_compliance.md", "governance"),
        ("Governance & Compliance Summary", "governance_compliance_summary.md", "governance"),
        ("Data Volume Monitoring Q&A", "c1_m3_data_volume_monitoring_qa.md", "governance"),
    ]),
    ("lifecycle", "Data Collection & Wrangling", [
        ("Data Collection Methods", "c1_m3_data_collection.md", "lifecycle"),
        ("Data Wrangling", "c1_m3_data_wrangling.md", "lifecycle"),
        ("Querying & Performance Tuning", "c1_m3_querying_performance.md", "lifecycle"),
    ]),
    ("python", "Python for Data Science", [
        ("Python Basics", "c2_python_basics.md", "python"),
        ("String Operations", "c2_string_operations.md", "python"),
        ("Jupyter Notebooks", "c2_jupyter_intro.md", "python"),
        ("Lists and Tuples", "c2_lists_and_tuples.md", "python"),
        ("Dictionaries", "c2_dictionaries.md", "python"),
        ("Sets", "c2_sets.md", "python"),
        ("Conditions & Branching", "c2_conditions_branching.md", "python"),
        ("Loops", "c2_loops.md", "python"),
        ("Functions", "c2_functions.md", "python"),
        ("Exception Handling", "c2_exception_handling.md", "python"),
        ("Objects & Classes", "c2_objects_classes.md", "python"),
    ]),
    ("bigdata", "Big Data Specialization (UCSD)", [
        ("Big Data Specialization — UC San Diego", "big_data_specialization_ucsd.md", "bigdata"),
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
        ("Full Course Index", "c1_full_course_index.md", "career"),
        ("Career Opportunities", "c1_m4_career_opportunities.md", "career"),
        ("Data Manager", "c1_m4_data_manager.md", "career"),
        ("Data Warehousing Specialist", "c1_m4_data_warehousing_specialist.md", "career"),
        ("Data Engineering Learning Path", "data_engineering_learning_path.md", "career"),
        ("Viewpoints: Get into Data Engineering", "viewpoints_get_into_data_engineering.md", "career"),
        ("Viewpoints: Employer Expectations", "viewpoints_employer_expectations.md", "career"),
        ("Viewpoints: Many Paths to DE", "viewpoints_many_paths_to_de.md", "career"),
        ("Viewpoints: Advice to Aspiring DEs", "viewpoints_advice_aspiring_de.md", "career"),
    ]),
]

# ── Helpers ──
def url_to_anchor(text):
    t = text.lower()
    t = re.sub(r'[^a-z0-9]+', '-', t)
    return t.strip('-')[:50]

def escape_html(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text

# ── Filename → anchor map for cross-ref resolution ──
def build_filename_to_anchor_map():
    m = {}
    for _, _, cards in SECTIONS:
        for title, md_file, _ in cards:
            anchor = url_to_anchor(title)
            m[md_file] = anchor
            m[f"topics/{md_file}"] = anchor
    m["glossary.md"] = "glossary"
    m["topics/glossary.md"] = "glossary"
    return m

# ── Hash manifest ──
def compute_status_map():
    manifest = {}
    if os.path.exists(MANIFEST):
        try:
            with open(MANIFEST, encoding="utf-8") as f:
                manifest = json.load(f)
            if not isinstance(manifest, dict):
                raise ValueError("not a dict")
        except (json.JSONDecodeError, OSError, ValueError):
            print("Warning: corrupt .lthp_state.json — treating as fresh")
            manifest = {}

    status, new_manifest = {}, {}
    all_md = [md for _, _, cards in SECTIONS for _, md, _ in cards] + ["glossary.md"]
    is_first_build = (len(manifest) == 0)

    for md_file in all_md:
        path = os.path.join(TOPICS_DIR, md_file)
        if not os.path.exists(path):
            status[md_file] = "original"
            continue
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        new_manifest[md_file] = h

        if is_first_build:
            status[md_file] = "original"
        elif md_file not in manifest:
            status[md_file] = "new"
        elif manifest[md_file] != h:
            status[md_file] = "modified"
        else:
            status[md_file] = "original"

    return status, new_manifest

# ── Content cleaning ──
def clean_content(text):
    """Strip course-ware structural artifacts from markdown before rendering."""
    lines = text.split('\n')
    out = []
    skip_table = False
    table_lines = []

    for line in lines:
        # Skip numbered section headings like "### 4.3 Course Wrap-Up"
        if re.match(r'^#{1,5}\s+\d+\.\d+\s', line):
            continue

        # Skip low-value boilerplate lines
        low_val = ["course wrap-up", "congratulations and next steps",
                    "summary and highlights", "practice quiz", "graded quiz"]
        if any(p in line.lower() for p in low_val):
            if not line.strip().startswith('|'):  # don't break table detection
                continue

        # Detect and skip content-map tables (sequential number in col 1)
        if line.strip().startswith('|'):
            table_lines.append(line)
            if not line.strip().endswith('|'):
                skip_table = True
                continue
            # Check if this is a content map row: first cell is a bare number
            cells = [c.strip() for c in line.split('|')]
            cells = [c for c in cells if c]
            if len(cells) >= 2 and re.match(r'^\d+$', cells[0]):
                skip_table = True
                continue
            if skip_table:
                continue
            out.append(line)
        else:
            if skip_table and table_lines:
                table_lines = []
                skip_table = False
            elif table_lines:
                out.extend(table_lines)
                table_lines = []
            out.append(line)

    # Flush remaining table buffer
    if not skip_table and table_lines:
        out.extend(table_lines)

    return '\n'.join(out)

# ── Markdown → HTML ──
def md_to_html(text):
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

    FILENAME_ANCHOR_MAP = build_filename_to_anchor_map()

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

        # ── LOW-RELEVANCE ──
        if line.strip().startswith('[LOW-RELEVANCE'):
            close_table(); close_list(); close_blockquote()
            text = escape_html(line.strip())
            html.append(f'<details class="low-relevance-note"><summary>Low relevance</summary>{text}</details>\n')
            i += 1
            continue

        # ── SUPERSEDED ──
        if line.strip().startswith('[SUPERSEDED'):
            close_table(); close_list(); close_blockquote()
            text = escape_html(line.strip())
            html.append(f'<div class="superseded-note"><span class="tag-icon">&#x26A0;</span> {text}</div>\n')
            i += 1
            continue

        # ── REDUNDANT ──
        if line.strip().startswith('[REDUNDANT'):
            close_table(); close_list(); close_blockquote()
            text = escape_html(line.strip())
            html.append(f'<div class="redundant-note"><span class="tag-icon">&#x21BB;</span> {text}</div>\n')
            i += 1
            continue

        # ── OFF-TOPIC inline (handle without dedicated block) ──
        if line.strip().startswith('[OFF-TOPIC'):
            close_table(); close_list(); close_blockquote()
            html.append(f'<div class="redundant-note">{escape_html(line.strip())}</div>\n')
            i += 1
            continue

        # ── Cross-ref ──
        if line.strip().startswith('[Cross-ref:') or line.strip().startswith('[cross-ref:'):
            close_table(); close_list(); close_blockquote()
            ref = line.strip()
            m = re.match(r'\[(?:Cross-ref|cross-ref):\s*(.+?)(?:\s*(?:—|-)\s*(.+))?\]', ref)
            if m:
                url = m.group(1).strip()
                text = m.group(2).strip() if m.group(2) else url
                anchor = FILENAME_ANCHOR_MAP.get(url) or url_to_anchor(url)
                html.append(f'<div class="cross-ref"><a href="#{anchor}" class="cross-ref-link">{escape_html(text)}</a></div>\n')
            else:
                html.append(f'<div class="cross-ref">{escape_html(ref)}</div>\n')
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


def inline_html(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def build_card_html(title, md_file, category):
    filepath = os.path.join(TOPICS_DIR, md_file)
    if not os.path.exists(filepath):
        return f'<h3>{escape_html(title)}</h3><p><em>Content pending.</em></p>\n'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'^# .+\n?', '', content, count=1)
    content = re.sub(r'\n\*Source:.*?\*', '', content)
    content = clean_content(content)
    return md_to_html(content)


# ── Build sections ──
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

            if not body.lstrip().startswith('<h3'):
                body = f'<h3>{escape_html(title)}</h3>\n{tag}\n{body}'
            else:
                body = re.sub(r'(<h3>.*?</h3>)', lambda m: f'{m.group(1)}\n{tag}', body, count=1)

            cards_html.append(f'<div class="{cls}" id="{anchor}">\n{body}\n</div>')

        sections_html.append(
            f'<section class="category" id="{section_id}">\n<div class="category-header">\n<h2>{escape_html(section_title)}</h2>\n'
            f'<span class="category-count">{escape_html(category)}</span>\n</div>\n{"".join(cards_html)}\n</section>'
        )
    return '\n'.join(sections_html)


# ── Glossary ──
def build_glossary(status_map):
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

    st = status_map.get("glossary.md", "original")
    if st == "new":
        cls = "card lthp-highlight"
        tag = '<span class="tag green">NEW</span>'
    elif st == "modified":
        cls = "card lthp-highlight"
        tag = '<span class="tag amber">MODIFIED</span>'
    else:
        cls = "card"
        tag = ""

    return f'''<section class="category" id="glossary">
<div class="category-header">
<h2>Consolidated Glossary</h2>
<span class="category-count">Reference</span>
</div>
<div class="{cls}">
{tag}
<p>{len(rows_html)} data engineering terms from all source files.</p>
<table>
<thead><tr><th>Term</th><th>Definition</th><th>Source Files</th></tr></thead>
<tbody>
{"".join(rows_html)}
</tbody>
</table>
<div class="cross-ref"><a href="#data-engineering-scope" class="cross-ref-link">All topic pages — this glossary consolidates terms from every source file</a></div>
</div>
</section>'''


# ── Future ──
def build_future():
    return """<section class="category" id="future">
<div class="category-header">
<h2>Coming Next — Modules 3–10</h2>
<span class="category-count">Preview</span>
</div>
<div class="future-card"><h3>Module 3 (Course 3) — Data Collection and Data Wrangling</h3><p>How to Gather and Import Data, Data Wrangling, Tools for Data Wrangling, CSV/Db2 lab exercises. <span class="tag">Course 1</span></p></div>
<div class="future-card"><h3>Module 4 (Course 3) — Querying Data, Performance Tuning, and Troubleshooting</h3><p>Querying and Analyzing Data, Performance Tuning and Troubleshooting, SQL exploration labs. <span class="tag">Course 1</span></p></div>
<div class="future-card"><h3>Module 5 (Course 3) — Governance and Compliance</h3><p>Governance frameworks, compliance regulations, DataOps methodology overview. <span class="tag">Course 1</span></p></div>
<div class="future-card"><h3>Courses 2–16 — Full IBM Certificate</h3><p>Python, SQL, Linux, DBA, ETL/Airflow/Kafka, Data Warehousing, BI, NoSQL, Big Data/Spark, ML, Capstone, GenAI, Career. See 16-Course Sequence card for details. <span class="tag">Full Track</span></p></div>
</section>"""


# ── Sidebar ──
def build_sidebar():
    items = []
    for section_id, section_title, cards in SECTIONS:
        first_anchor = url_to_anchor(cards[0][0])
        items.append(f'<a href="#{first_anchor}" class="sidebar-link" data-section="{section_id}">{escape_html(section_title)}</a>')
        for title, _, _ in cards:
            anchor = url_to_anchor(title)
            items.append(f'<a href="#{anchor}" class="sidebar-sub-link" data-section="{section_id}">{escape_html(title)}</a>')
    items.append('<div class="sidebar-divider"></div>')
    items.append('<a href="#glossary" class="sidebar-link" data-section="glossary">Glossary</a>')
    items.append('<a href="#future" class="sidebar-link" data-section="future">Coming Next</a>')
    return ''.join(items)


# ── Template ──
TEMPLATE_PATH = os.path.join(WIKI_DIR, "wiki_template.html")


# ── Main ──
def main():
    status_map, new_manifest = compute_status_map()

    sections_html = build_sections(status_map)
    glossary_html = build_glossary(status_map)
    future_html = build_future()
    sidebar_html = build_sidebar()

    content = sections_html + '\n\n' + glossary_html + '\n\n' + future_html

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('{{WIKI_CONTENT}}', content)
    html = html.replace('{{SIDEBAR_NAV}}', sidebar_html)

    total_cards = sum(len(cards) for _, _, cards in SECTIONS)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # Inline Mermaid JS into the HTML for a single self-contained file
    mermaid_src = os.path.join(WIKI_DIR, 'node_modules', 'mermaid', 'dist', 'mermaid.min.js')
    if os.path.exists(mermaid_src):
        with open(mermaid_src, 'r', encoding='utf-8') as f:
            mermaid_js = f.read()
        html = html.replace('{{MERMAID_JS}}', '<script>' + mermaid_js + '</script>')
    else:
        html = html.replace('{{MERMAID_JS}}', '<script>console.warn("Mermaid not bundled")</script>')

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)

    # Copy to output/option_a/ (pipeline HTML output target)
    os.makedirs(os.path.dirname(OUTPUT_OPTION_A), exist_ok=True)
    with open(OUTPUT_OPTION_A, 'w', encoding='utf-8') as f:
        f.write(html)

    # Copy to git repo root as index.html (GitHub Pages entry)
    repo_root = os.path.dirname(WIKI_DIR)
    repo_index = os.path.join(repo_root, 'index.html')
    with open(repo_index, 'w', encoding='utf-8') as f:
        f.write(html)

    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(new_manifest, f, indent=2)

    new_count = sum(1 for v in status_map.values() if v == "new")
    mod_count = sum(1 for v in status_map.values() if v == "modified")
    orig_count = total_cards - new_count - mod_count

    file_size = os.path.getsize(OUTPUT)
    print(f"Written: {OUTPUT}")
    print(f"Written: {repo_index}")
    print(f"Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"Cards: {total_cards} (NEW: {new_count}, MODIFIED: {mod_count}, ORIGINAL: {orig_count})")


if __name__ == '__main__':
    main()
