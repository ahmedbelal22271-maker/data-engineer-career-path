"""
comment.py — Add comment boilerplate to unpacked .docx XML parts.

Usage:
  python comment.py unpacked_dir/ 0 "Comment text" [--parent -1] [--author "Author"]
  python comment.py unpacked_dir/ 1 "Reply text" --parent 0

After running, add markers to document.xml (see XML Reference in SKILL.md).
"""

import os
import sys
import html
from lxml import etree


def get_or_create_comments_xml(source_dir):
    """Return the path to comments.xml, creating it if needed."""
    comments_path = os.path.join(source_dir, "word", "comments.xml")
    if os.path.exists(comments_path):
        return comments_path

    # Create minimal comments.xml
    nsmap = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    root = etree.Element("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}comments", nsmap=nsmap)
    tree = etree.ElementTree(root)
    tree.write(comments_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    return comments_path


def add_comment(source_dir, comment_id, text, parent_id=-1, author="Claude"):
    escaped = html.escape(text).replace("'", "&#x2019;").replace('"', "&#x201D;")
    now = "2025-01-01T00:00:00Z"

    comments_path = get_or_create_comments_xml(source_dir)
    tree = etree.parse(comments_path)
    root = tree.getroot()
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    comment = etree.SubElement(root, f"{{{ns}}}comment")
    comment.set("w:id", str(comment_id))
    comment.set("w:author", author)
    comment.set("w:date", now)

    if parent_id >= 0:
        comment.set("w:parentId", str(parent_id))

    p = etree.SubElement(comment, f"{{{ns}}}p")
    r = etree.SubElement(p, f"{{{ns}}}r")
    t = etree.SubElement(r, f"{{{ns}}}t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = escaped

    tree.write(comments_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"Added comment {comment_id} to {comments_path}")

    # Ensure relationship exists in document.xml.rels
    rels_path = os.path.join(source_dir, "word", "_rels", "document.xml.rels")
    if os.path.exists(rels_path):
        rels_tree = etree.parse(rels_path)
        rels_root = rels_tree.getroot()
        rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"

        # Check if comments relationship exists
        existing = rels_root.findall(f"{{{rel_ns}}}Relationship")
        has_comments = any(
            r.get("Type", "").endswith("/comments") for r in existing
        )
        if not has_comments:
            max_id = 0
            for r in existing:
                rid = r.get("Id", "rId0")
                try:
                    max_id = max(max_id, int(rid[3:]))
                except ValueError:
                    pass
            new_rid = f"rId{max_id + 1}"
            rel = etree.SubElement(rels_root, f"{{{rel_ns}}}Relationship")
            rel.set("Id", new_rid)
            rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments")
            rel.set("Target", "comments.xml")
            rels_tree.write(rels_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
            print(f"Added comments relationship ({new_rid}) to document.xml.rels")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python comment.py unpacked_dir/ comment_id \"text\" [--parent id] [--author name]")
        sys.exit(1)

    source_dir = sys.argv[1]
    comment_id = int(sys.argv[2])
    text = sys.argv[3]
    parent_id = -1
    author = "Claude"

    for i, arg in enumerate(sys.argv[4:], start=4):
        if arg == "--parent" and i + 1 < len(sys.argv):
            parent_id = int(sys.argv[i + 1])
        if arg == "--author" and i + 1 < len(sys.argv):
            author = sys.argv[i + 1]

    add_comment(source_dir, comment_id, text, parent_id=parent_id, author=author)
