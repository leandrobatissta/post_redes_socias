"""
Gerador de PDF e JPG do Paper Técnico — Sistema Kiosk Protegido 24/7
Uso: python3 gerar_paper.py
Requer: Google Chrome instalado em /Applications/Google Chrome.app
"""

import subprocess
import os
import sys

# ── Configurações ────────────────────────────────────────────────────────────

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
HTML_INPUT  = os.path.join(BASE_DIR, "paper_print.html")
PDF_OUTPUT  = os.path.join(BASE_DIR, "PAPER_SISTEMA_KIOSK.pdf")
JPG_OUTPUT  = os.path.join(BASE_DIR, "PAPER_SISTEMA_KIOSK.jpg")
CHROME_BIN  = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Dimensões JPG: A4 a 96dpi (794 x 1123 px) — mesma base do PDF
JPG_WIDTH   = 794
JPG_HEIGHT  = 1123

# ── Validações ───────────────────────────────────────────────────────────────

def check_requirements():
    if not os.path.isfile(CHROME_BIN):
        print(f"[ERRO] Google Chrome não encontrado em:\n  {CHROME_BIN}")
        sys.exit(1)

    if not os.path.isfile(HTML_INPUT):
        print(f"[ERRO] Arquivo HTML de entrada não encontrado:\n  {HTML_INPUT}")
        sys.exit(1)

    print(f"[OK] Chrome encontrado")
    print(f"[OK] HTML de entrada: {HTML_INPUT}")

# ── Geração de PDF ───────────────────────────────────────────────────────────

def gerar_pdf():
    print("\n[→] Gerando PDF...")
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={PDF_OUTPUT}",
        "--print-to-pdf-no-header",
        "--no-margins",
        f"file://{HTML_INPUT}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.isfile(PDF_OUTPUT):
        print(f"[ERRO] Falha ao gerar PDF:\n{result.stderr}")
        sys.exit(1)
    size_kb = os.path.getsize(PDF_OUTPUT) // 1024
    print(f"[OK] PDF gerado: {PDF_OUTPUT} ({size_kb} KB)")

# ── Geração de JPG ───────────────────────────────────────────────────────────

def gerar_jpg():
    print("\n[→] Gerando JPG...")
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        f"--screenshot={JPG_OUTPUT}",
        f"--window-size={JPG_WIDTH},{JPG_HEIGHT}",
        f"file://{HTML_INPUT}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.isfile(JPG_OUTPUT):
        print(f"[ERRO] Falha ao gerar JPG:\n{result.stderr}")
        sys.exit(1)
    size_kb = os.path.getsize(JPG_OUTPUT) // 1024
    print(f"[OK] JPG gerado: {JPG_OUTPUT} ({size_kb} KB)")

# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  Gerador de Paper — Sistema Kiosk Protegido 24/7")
    print("=" * 55)

    check_requirements()
    gerar_pdf()
    gerar_jpg()

    print("\n[✔] Concluído!")
    print(f"    PDF → {PDF_OUTPUT}")
    print(f"    JPG → {JPG_OUTPUT}")
