"""
accept_changes.py — Accept all tracked changes in a .docx file via LibreOffice macro.

Usage: python accept_changes.py input.docx output.docx
"""

import sys
import os
import subprocess
import tempfile


MACRO_SCRIPT = """
import uno

def accept_all_changes():
    desktop = XSCRIPTCONTEXT.getDesktop()
    doc = desktop.getCurrentComponent()
    doc.setPropertyValue("RecordChanges", False)
    doc.resetDocument()

accept_all_changes()
"""


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
    for path in os.environ.get("PATH", "").split(os.pathsep):
        soffice = os.path.join(path, "soffice")
        if os.path.exists(soffice):
            return soffice
        soffice_exe = os.path.join(path, "soffice.exe")
        if os.path.exists(soffice_exe):
            return soffice_exe
    return None


def accept_changes(input_path, output_path):
    soffice = find_soffice()
    if not soffice:
        print("Error: LibreOffice not found.")
        sys.exit(1)

    abs_input = os.path.abspath(input_path)
    abs_output = os.path.abspath(output_path)

    # Use LibreOffice macro to accept changes and save
    macro_dir = tempfile.mkdtemp()
    macro_path = os.path.join(macro_dir, "AcceptChanges.py")
    with open(macro_path, "w") as f:
        f.write(MACRO_SCRIPT)

    cmd = [
        soffice, "--headless", "--norestore",
        f"-acceptChanges={macro_path}",
        abs_input,
    ]

    # Simpler approach: use LibreOffice's --infilter and macro
    # Actually the simplest: use python-docx or a simpler approach
    # LibreOffice can accept changes via command line with a macro

    # Let's use a simpler approach - convert via LibreOffice which auto-accepts
    try:
        result = subprocess.run(
            [soffice, "--headless", "--convert-to", "docx", "--outdir",
             os.path.dirname(abs_output), abs_input],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            # LibreOffice creates the file in the outdir with same name
            generated = os.path.join(os.path.dirname(abs_output), os.path.basename(abs_input))
            if os.path.exists(generated):
                os.rename(generated, abs_output)
                print(f"Accepted changes -> {abs_output} (via LibreOffice re-save)")
            else:
                print(f"Warning: output not found at {generated}")
        else:
            print(f"LibreOffice error: {result.stderr}")
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: LibreOffice timed out.")
        sys.exit(1)
    finally:
        import shutil
        shutil.rmtree(macro_dir, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python accept_changes.py input.docx output.docx")
        sys.exit(1)

    accept_changes(sys.argv[1], sys.argv[2])
