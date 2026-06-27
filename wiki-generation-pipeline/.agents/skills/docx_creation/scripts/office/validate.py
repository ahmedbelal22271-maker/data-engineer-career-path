"""
validate.py — Validate .docx file: check ZIP structure and XML well-formedness.

Usage: python validate.py document.docx
"""

import sys
import zipfile
from lxml import etree


def validate(docx_path):
    errors = []

    # Check ZIP structure
    try:
        with zipfile.ZipFile(docx_path, "r") as z:
            names = z.namelist()
            required = ["word/document.xml", "[Content_Types].xml"]
            for r in required:
                if r not in names:
                    errors.append(f"Missing required entry: {r}")

            # Validate each XML entry
            for name in names:
                if name.endswith(".xml") or name.endswith(".rels"):
                    try:
                        raw = z.read(name)
                        etree.fromstring(raw)
                    except Exception as e:
                        errors.append(f"XML error in {name}: {e}")

    except zipfile.BadZipFile:
        errors.append("Not a valid ZIP file")

    # Check file extension
    if not docx_path.lower().endswith(".docx"):
        errors.append("File does not have .docx extension")

    if errors:
        print("Validation FAILED:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("Validation PASSED")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py document.docx")
        sys.exit(1)

    success = validate(sys.argv[1])
    sys.exit(0 if success else 1)
