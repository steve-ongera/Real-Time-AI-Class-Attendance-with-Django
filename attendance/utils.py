from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

def generate_attendance_pdf(units_data, weeks):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))

    # Add logo
    logo = Image('media/mutlogo.png', width=1*inch, height=1*inch)
    logo.hAlign = 'CENTER'
    elements.append(logo)

    # Add university information
    uni_info = """
    <para alignment="center">
    <font size="14"><b>Murang'a University of  Technology</b></font><br/>
    <font size="10">P.O. Box 972-60200, Murang'a, Kenya<br/>
    Tel: +254-064-30049/30057<br/>
    Email: info@mut.ac.ke</font>
    </para>
    """
    elements.append(Paragraph(uni_info, styles['Center']))
    elements.append(Spacer(1, 0.2*inch))

    for unit in units_data:
        # Add unit header
        unit_header = f"<para alignment='center'><font size='12'><b>{unit['unit_name']} ({unit['unit_code']})</b></font></para>"
        elements.append(Paragraph(unit_header, styles['Center']))
        elements.append(Spacer(1, 0.1*inch))

        # Prepare data for the table
        data = [['Student'] + [f'Week {week}' for week in weeks]]
        for student in unit['students']:
            row = [student['name']] + [student['attendance'][week] for week in weeks]
            data.append(row)

        # Create the table
        table = Table(data, colWidths=[2*inch] + [0.6*inch] * len(weeks))

        # Add style to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Align first column (names) to left
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),  # Center all other columns
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        # Add the table to the elements
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer