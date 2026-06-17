"""detached OCR runner - uses subprocess.Popen with DETACHED_PROCESS to survive session kill"""
import sys
import os
import subprocess

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: detached_runner.py <pdf> <output_txt> [dpi]")
        sys.exit(1)

    pdf = sys.argv[1]
    out = sys.argv[2]
    dpi = sys.argv[3] if len(sys.argv) > 3 else "150"

    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(here, "ocr_pdf.py")

    cmd = [sys.executable, script, pdf, out, "--dpi", dpi]
    log = out + ".log"

    flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    with open(log, "ab") as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=f, stdin=subprocess.DEVNULL,
                              creationflags=flags, close_fds=True)
    print(f"Started detached PID={p.pid}, log={log}")
    # Don't wait - return immediately
