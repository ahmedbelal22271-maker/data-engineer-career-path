"""
soffice.py — Headless LibreOffice wrapper for document conversion.

Usage:
  python soffice.py --headless --convert-to pdf document.docx
  python soffice.py --headless --convert-to docx document.doc
"""

import sys
import os
import subprocess


def find_soffice():
    candidates = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/usr/lib/libreoffice/program/soffice",
        "/usr/bin/soffice",
        "/snap/bin/soffice",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    # Try PATH
    for path in os.environ.get("PATH", "").split(os.pathsep):
        soffice = os.path.join(path, "soffice")
        if os.path.exists(soffice):
            return soffice
        soffice_exe = os.path.join(path, "soffice.exe")
        if os.path.exists(soffice_exe):
            return soffice_exe
    return None


if __name__ == "__main__":
    soffice = find_soffice()
    if not soffice:
        print("Error: LibreOffice not found. Install LibreOffice or set PATH.")
        sys.exit(1)

    cmd = [soffice] + sys.argv[1:]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(result.returncode)
    print(result.stdout)
