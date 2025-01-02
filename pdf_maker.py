from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from datetime import date

# Define the file name for the PDF
pdf_filename = "compression_garment_proof_of_delivery.pdf"

# Function to create the PDF
def create_pdf():
    # Create a canvas object
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    # Get the page width and height
    width, height = letter
    
    # Define some styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        fontName="Helvetica-Bold",
        fontSize=24,
        spaceAfter=12,
        alignment=1  # Center alignment
    )

    # Define the fields with placeholders
    patient_name = "Placeholder Name"
    patient_dob = "Placeholder Date of Birth"
    insurance = "Placeholder Insurance"
    today_date = date.today().strftime("%B %d, %Y")

    # Create the title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 60, "Compression Garment Proof of Delivery")

    # Create the patient info fields centered below the title
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 120, "Patient Name:")
    c.drawString(300, height - 120, patient_name)

    c.drawString(100, height - 140, "Patient Date of Birth:")
    c.drawString(300, height - 140, patient_dob)

    c.drawString(100, height - 160, "Insurance:")
    c.drawString(300, height - 160, insurance)

    c.drawString(100, height - 180, "Date:")
    c.drawString(300, height - 180, today_date)

    # Draw a horizontal line under the fields
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(50, height - 200, width - 50, height - 200)

    # Add the long text at the bottom of the page with wrapping
    long_text = (
        "I request that payment of authorized Medicare benefits (or other third-party insurance) "
        "be made either to me or on my behalf to Central Coast Lymphedema for any services furnished "
        "for me by that company. I authorize any holder of medical information about me to release to the "
        "Health Care Financing Administration (or other Insurance Administrations) and its agents any "
        "information needed to determine these benefits or the benefits payable for related services.\n\n"
        "Please be aware that Central Coast Lymphedema and Wound Center is not liable for any injuries "
        "or complications resulting from the improper use of garments or other equipment provided. It is "
        "important to follow all usage instructions and consult with a healthcare professional for any concerns "
        "regarding the use of these items."
    )
    
    # Adjust the starting position for the long text
    # Set the y position just above the signature line (with a small buffer)
    signature_line_y = 40  # y position for the signature line
    buffer_space = 0  # Adjust space above the signature line
    text_start_y = signature_line_y + buffer_space + 50  # Starting position for the text, 50 units above the signature line

    # Set up the paragraph style
    paragraph_style = ParagraphStyle(
        'Normal', 
        fontName='Helvetica', 
        fontSize=10, 
        spaceBefore=6, 
        spaceAfter=6,
        alignment=0,  # Left align the text
        wordWrap='CJK',  # Ensure text wraps properly
        width=width - 100  # Set width for text wrapping
    )
    
    # Create the paragraph
    paragraph = Paragraph(long_text, paragraph_style)

    # Wrap the paragraph to fit the available space
    paragraph.wrap(width - 100, height - text_start_y)
    paragraph.drawOn(c, 50, text_start_y)

    # Add a signature line at the bottom
    c.setFont("Helvetica", 12)
    c.drawString(100, signature_line_y, "Signature: ____________________________")

    # Save the PDF
    c.save()

# Call the function to create the PDF
create_pdf()

print(f"PDF '{pdf_filename}' has been created successfully.")
