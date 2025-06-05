from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_circular(output_path: str):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    text = c.beginText(40, height - 50)
    text.setFont("Helvetica-Bold", 16)
    text.textLine("Cabinet Mobilization Circular")
    text.moveCursor(0, 20)

    text.setFont("Helvetica", 12)
    paragraphs = [
        "Subject: National Funeral Operational Readiness",
        "To: All Cabinet Ministers and Permanent Secretaries",
        "",  # blank line
        "This circular serves as official notification of the activation of the National Mourning Protocol Framework.",
        "All ministries are required to lower national flags to half-mast within 48 hours and maintain this status until further notice.",
        "Cabinet will convene to coordinate funeral rites, state honors, and inter-agency support.",
        "ZAFSA and AIA will monitor all consular outputs and provide intelligence updates.",
        "Military and diplomatic units must finalize escort planning for dignitaries.",
        "The Ministry of Foreign Affairs and Ministry of Health are tasked with liaison and body transfer logistics.",
        "ZNBC will prepare a national address and comply with Media Control Measures to suspend speculative broadcasts until cleared.",
        "",  # blank line
        "All ministries must appoint focal points and submit readiness reports within three days.",
        "",  # blank line
        "Signed,",
        "Secretary to the Cabinet",
    ]

    for line in paragraphs:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()


if __name__ == "__main__":
    create_circular("cabinet_mobilization_circular.pdf")
