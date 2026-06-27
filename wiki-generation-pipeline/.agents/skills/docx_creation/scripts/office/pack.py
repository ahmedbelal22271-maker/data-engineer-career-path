"""
pack.py — Repack XML files into .docx, validate, and auto-repair common issues.

Usage: python pack.py unpacked_dir/ output.docx [--original original.docx] [--validate false]
"""

import os
import sys
import zipfile
import re
from lxml import etree


def condense_xml(xml_content):
    """Remove unnecessary whitespace from XML."""
    root = etree.fromstring(xml_content)
    return etree.tostring(root, encoding="unicode", method="xml")


def repair_durable_id(xml_content):
    """Fix durableId values >= 0x7FFFFFFF."""
    import random
    def fix_id(m):
        return f'w:durableId="{{{random.randint(1, 0x7FFFFFFE):08X}}}"'
    return re.sub(r'w:durableId="\{[^}]+\}"', fix_id, xml_content)


def repair_whitespace(xml_content):
    """Add xml:space=\"preserve\" on <w:t> elements with leading/trailing whitespace."""
    root = etree.fromstring(xml_content.encode("utf-8"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    for t in root.xpath("//w:t", namespaces=ns):
        if t.text and (t.text != t.text.strip() or not t.text.strip()):
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return etree.tostring(root, encoding="unicode")


def auto_repair(xml_content):
    xml_content = repair_durable_id(xml_content)
    xml_content = repair_whitespace(xml_content)
    return xml_content


def pack(source_dir, output_path, original_path=None, do_validate=True):
    if original_path and os.path.exists(original_path):
        with zipfile.ZipFile(original_path, "r") as z:
            z.extractall(source_dir)
        print(f"Seeded from original {original_path}")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for root_dir, dirs, files in os.walk(source_dir):
            for fname in files:
                fpath = os.path.join(root_dir, fname)
                arcname = os.path.relpath(fpath, source_dir)
                with open(fpath, "rb") as f:
                    content = f.read()

                if fname.endswith(".xml") or fname.endswith(".rels"):
                    try:
                        decoded = content.decode("utf-8")
                        decoded = auto_repair(decoded)
                        decoded = condense_xml(decoded)
                        content = decoded.encode("utf-8")
                    except Exception:
                        pass

                zout.writestr(arcname, content)

    print(f"Packed to {output_path}")

    if do_validate:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "zipfile", "-t", output_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("Validation passed.")
        else:
            print(f"Validation failed: {result.stderr}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pack.py unpacked_dir/ output.docx [--original source.docx] [--validate false]")
        sys.exit(1)

    source = sys.argv[1]
    output = sys.argv[2]
    original = None
    do_val = True

    for i, arg in enumerate(sys.argv[3:], start=3):
        if arg == "--original" and i + 1 < len(sys.argv):
            original = sys.argv[i + 1]
        if arg == "--validate" and i + 1 < len(sys.argv):
            do_val = sys.argv[i + 1].lower() != "false"

    pack(source, output, original_path=original, do_validate=do_val)
