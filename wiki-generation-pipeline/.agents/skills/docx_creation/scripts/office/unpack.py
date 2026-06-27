"""
unpack.py — Extract .docx archive, pretty-print XML, merge adjacent runs,
       and convert smart quotes to XML entities.

Usage: python unpack.py document.docx output_dir/ [--merge-runs true|false]
"""

import os
import sys
import zipfile
import re
from xml.dom import minidom
from lxml import etree


SMART_QUOTES = {
    "\u2018": "&#x2018;",
    "\u2019": "&#x2019;",
    "\u201c": "&#x201C;",
    "\u201d": "&#x201D;",
}


def convert_smart_quotes(text):
    for char, entity in SMART_QUOTES.items():
        text = text.replace(char, entity)
    return text


def pretty_print_xml(raw):
    root = etree.fromstring(raw)
    return etree.tostring(root, pretty_print=True, encoding="unicode")


def merge_adjacent_runs(xml_content):
    """
    Merge adjacent <w:r> elements that share the same formatting (<w:rPr>).
    This reduces noise when editing text.
    """
    root = etree.fromstring(xml_content)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    for parent in root.xpath(".//w:p", namespaces=ns):
        runs = parent.findall("w:r", ns)
        i = 0
        while i < len(runs) - 1:
            r1 = runs[i]
            r2 = runs[i + 1]
            rpr1 = r1.find("w:rPr", ns)
            rpr2 = r2.find("w:rPr", ns)
            # Compare rPr by string serialization (None == None means same)
            if etree.tostring(rpr1) == etree.tostring(rpr2):
                t1 = r1.find("w:t", ns)
                t2 = r2.find("w:t", ns)
                if t1 is not None and t2 is not None:
                    t1.text = (t1.text or "") + (t2.text or "")
                    parent.remove(r2)
                    runs = parent.findall("w:r", ns)
                    continue
            i += 1

    return etree.tostring(root, encoding="unicode")


def unpack(docx_path, output_dir, merge_runs=True):
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(docx_path, "r") as z:
        for entry in z.namelist():
            raw = z.read(entry)

            if entry.endswith(".xml") or entry.endswith(".rels"):
                try:
                    decoded = raw.decode("utf-8")
                    decoded = convert_smart_quotes(decoded)
                    if merge_runs and "document.xml" in entry:
                        decoded = merge_adjacent_runs(decoded)
                    pretty = pretty_print_xml(bytes(decoded, "utf-8"))
                    raw = bytes(pretty, "utf-8")
                except Exception:
                    pass  # Binary file, write as-is

            dest = os.path.join(output_dir, entry)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(raw)

    print(f"Unpacked {docx_path} to {output_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python unpack.py document.docx output_dir/ [--merge-runs true|false]")
        sys.exit(1)

    merge = True
    if len(sys.argv) > 3:
        if sys.argv[3] == "--merge-runs":
            merge = sys.argv[4].lower() != "false" if len(sys.argv) > 4 else True

    unpack(sys.argv[1], sys.argv[2], merge_runs=merge)
