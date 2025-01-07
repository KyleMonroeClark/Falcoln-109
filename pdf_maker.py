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
    title_style = ParagraphStyle(
        "Title",
        fontName="Helvetica-Bold",
        fontSize=24,
        spaceAfter=12,
        alignment=1  # Center alignment
    )

    # Define the fields with placeholder values
    patient_name = "Placeholder Name"
    patient_dob = "Placeholder Date of Birth"
    insurance = "Placeholder Insurance"
    today_date = date.today().strftime("%B %d, %Y")
    
    # New fields (Garment details)
    part_id = "Placeholder Part ID"
    side = "Placeholder Side"
    quantity = "Placeholder Quantity"
    garment_type = "Placeholder Garment Type"
    hcpcs_code = "Placeholder HCPCS"
    fee = "$Placeholder Fee"
    notes = "Placeholder notes regarding the compression garment. Please follow the usage instructions carefully."

    # Set the image file path
    logo_path = "CCLWC_Logo.png"
    
    # Original dimensions of the PNG
    original_logo_width = 690  # Logo width in pixels
    original_logo_height = 180  # Logo height in pixels
    
    # Scaling factor to reduce the size to 1/6
    scale_factor = 1 / 2  # Scale to 1/6 of the original size
    
    # Calculate the new dimensions
    scaled_logo_width = original_logo_width * scale_factor  # 1/6th of original width
    scaled_logo_height = original_logo_height * scale_factor  # 1/6th of original height

    # Calculate the x position to center the logo
    x_position = (width - scaled_logo_width) / 2  # Center the logo horizontally
    y_position = height - scaled_logo_height - 10  # Position slightly below the top edge
    
    # Draw the logo on the PDF
    c.drawImage(logo_path, x_position, y_position, scaled_logo_width, scaled_logo_height)

    # Create the title
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 120, "Durable Medical Equipment Proof of Delivery")

    # Create the patient info fields centered below the title
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 140, "Patient Name:")
    c.setFont("Helvetica", 12)
    c.drawString(300, height - 140, patient_name)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 160, "Patient Date of Birth:")
    c.setFont("Helvetica", 12)
    c.drawString(300, height - 160, patient_dob)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 180, "Insurance:")
    c.setFont("Helvetica", 12)
    c.drawString(300, height - 180, insurance)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 200, "Date:")
    c.setFont("Helvetica", 12)
    c.drawString(300, height - 200, today_date)

    # Draw a horizontal line under the fields
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(50, height - 210, width - 50, height - 210)

    # Garment Details Section (labels individually underlined)
    c.setFont("Helvetica-Bold", 12)

    # Label starting positions (aligned to the left)
    label_y = height - 230  # Starting y-position for labels

    label_spacing = (width - 100) / 3  # Divide space into 3 equal parts for first row

    # First row of labels (aligned from the left)
    c.drawString(50, label_y, "Part ID")
    c.drawString(50 + label_spacing, label_y, "Side")
    c.drawString(50 + 2 * label_spacing, label_y, "Quantity")
    
    # Draw underlines for the labels
    c.line(50, label_y - 2, 150, label_y - 2)  # Underline "Part ID"
    c.line(50 + label_spacing, label_y - 2, 150 + label_spacing, label_y - 2)  # Underline "Side"
    c.line(50 + 2 * label_spacing, label_y - 2, 150 + 2 * label_spacing, label_y - 2)  # Underline "Quantity"

    # Move down to start printing values
    value_y = label_y - 30  # Position for values (a bit lower than the labels)

    # First row of values
    c.setFont("Helvetica", 12)
    c.drawString(50, value_y, part_id)
    c.drawString(50 + label_spacing, value_y, side)
    c.drawString(50 + 2 * label_spacing, value_y, quantity)

    # Second line of labels (moved below first line)
    label_y -= 70  # Adjusting vertical position for the second row of labels

    # Bold font for the second group of labels
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, label_y, "Garment Type")
    c.drawString(50 + label_spacing, label_y, "HCPCS")
    c.drawString(50 + 2 * label_spacing, label_y, "Fee")

    # Draw underlines for the second row of labels
    c.setFont("Helvetica", 12)
    c.line(50, label_y - 2, 150, label_y - 2)  # Underline "Garment Type"
    c.line(50 + label_spacing, label_y - 2, 150 + label_spacing, label_y - 2)  # Underline "HCPCS"
    c.line(50 + 2 * label_spacing, label_y - 2, 150 + 2 * label_spacing, label_y - 2)  # Underline "Fee"

    # Move down to start printing the second set of values (increased space)
    value_y = label_y - 30  # Increased vertical spacing for the second group of values

    c.drawString(50, value_y, garment_type)
    c.drawString(50 + label_spacing, value_y, hcpcs_code)
    c.drawString(50 + 2 * label_spacing, value_y, fee)

    # Move to the next section for additional notes
    notes_label_y = value_y - 40  # Space between the garment details and notes label
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, notes_label_y, "Additional Notes:")

    # Add a long text for the notes
    notes_text = notes  # Long text that needs to wrap

    # Set up the paragraph style for notes (to wrap text)
    paragraph_style = ParagraphStyle(
        'Normal', 
        fontName='Helvetica', 
        fontSize=10, 
        spaceBefore=6, 
        spaceAfter=6,
        alignment=0,  # Left-align the text
        wordWrap='CJK',  # Ensure text wraps properly
        width=width - 100  # Set width for text wrapping
    )
    
    # Create the paragraph for notes
    paragraph = Paragraph(notes_text, paragraph_style)

    # Adjust the starting position for the long notes text
    notes_start_y = notes_label_y - 20  # Start position for the notes text (below the label)
    
    # Wrap the paragraph to fit the available space
    paragraph.wrap(width - 100, height - notes_start_y)
    paragraph.drawOn(c, 50, notes_start_y)

    # Add the long legal text at the bottom (as before)
    long_text = (
        "I request that payment of authorized Medicare benefits (or other any other insurance) "
        "be made either to me or on my behalf to Central Coast Lymphedema for any services furnished "
        "for me by that company. I authorize any holder of medical information about me to release to the "
        "Health Care Financing Administration (or other insurance administrations) and its agents any "
        "information needed to determine these benefits or the benefits payable for related services.\n\n"
        "Please be aware that Central Coast Lymphedema and Wound Center is not liable for any injuries "
        "or complications resulting from the improper use of garments or other equipment provided. It is "
        "important to follow all usage instructions and consult with a healthcare professional for any concerns "
        "regarding the use of these items."
    )
    
    # Adjust the starting position for the long text
    signature_line_y = 40  # y position for the signature line
    buffer_space = 0  # Adjust space above the signature line
    text_start_y = signature_line_y + buffer_space + 50  # Starting position for the text, 50 units above the signature line

    # Set up the paragraph style for long text
    long_text_style = ParagraphStyle(
        'Normal', 
        fontName='Helvetica', 
        fontSize=10, 
        spaceBefore=6, 
        spaceAfter=6,
        alignment=0,  # Left-align the text
        wordWrap='CJK',  # Ensure text wraps properly
        width=width - 100  # Set width for text wrapping
    )
    
    # Create the paragraph for long text
    long_paragraph = Paragraph(long_text, long_text_style)

    # Wrap the paragraph to fit the available space
    long_paragraph.wrap(width - 100, height - text_start_y)
    long_paragraph.drawOn(c, 50, text_start_y)

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(50, text_start_y+85, width - 50, text_start_y+85)

    # Add a signature line at the bottom
    c.setFont("Helvetica", 12)
    c.drawString(100, signature_line_y, "Signature: __________________________________________")

    # Save the PDF
    c.save()

# Call the function to create the PDF
create_pdf()

print(f"PDF '{pdf_filename}' has been created successfully.")
