
import os
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Invoice
from .serializers import InvoiceSerializer


def generate_pdf(request, invoice_id):
    # Retrieve the Invoice object from the database
    invoice = get_object_or_404(Invoice, id=invoice_id)
    # item=get_object_or_404(Item)
    # Serialize the Invoice object
    serializer = InvoiceSerializer(invoice)

    # Create a BytesIO buffer to hold the PDF content
    buffer = BytesIO()

    # Create the PDF object using the BytesIO buffer
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    pdf.setPageSize((width, height))
    pdf.drawString(250, height - 120, "Customer Invoice")
    # Draw a horizontal line at the top of the page
    pdf.setStrokeColorRGB(0, 0, 1)
    pdf.line(30, height - 130, 30 + 530, height - 130)

    # Set the fill color to blue
    pdf.setFillColorRGB(0, 0, 1)

    # Draw the text in blue color
    pdf.setFont("Helvetica", 7)
    pdf.drawString(30, height - 165, f"{invoice.Company_name}")
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(30, height - 180, f"{invoice.company_address}")
    pdf.drawString(30, height - 200, f"Phone Number:{invoice.phone_number}")
    pdf.drawString(30, height - 210, f"GST Number:{invoice.gst_number}")
    pdf.drawString(30, height - 220, f"FSSAI Number:{invoice.fssai_number}")
    pdf.drawString(320, height - 165, 'To')
    pdf.drawString(320, height - 180, f"Invoice No: {invoice.invoice_number}")
    pdf.drawString(320, height - 190, f"Invoice Date: {invoice.invoice_date}")
    pdf.drawString(320, height - 200, f"Customer: {invoice.customer_name}")
    pdf.drawString(320, height - 210, f"Address: {invoice.customer_address}")
    pdf.drawString(320, height - 220, f"Customer Mobile No: {invoice.customer_mobile_number}")
    logo_path = invoice.logo
    pdf.drawImage(str(logo_path), 30, height - 80, width=100, height=50)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColorRGB(0, 0, 1)
    pdf.drawString(30, height - 260, "Your Orders")
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(30, height - 275, "S.No")
    pdf.setFont("Helvetica", 6)
    pdf.drawString(65, height - 275, "Item Name")
    pdf.drawString(150, height - 275, "MRP")
    pdf.drawString(190, height - 275, "Quantity")
    pdf.drawString(190, height - 285, "pcs")
    pdf.drawString(230, height - 275, "Base Rate")
    pdf.drawString(285, height - 275, "Disc 1")
    pdf.drawString(320, height - 275, "Disc 2")
    pdf.drawString(350, height - 275, "Taxable amt")
    pdf.drawString(400, height - 275, "CGST Amt")
    pdf.drawString(400, height - 285, "CGST Tax%")
    pdf.drawString(450, height - 275, "S/UTGST Amt")
    pdf.drawString(450, height - 285, "S/UTGST Amt")
    pdf.drawString(500, height - 275, "Net Amount")
    pdf.setStrokeColorRGB(128, 0, 128)
    pdf.line(30, height - 290, 30 + 530, height - 290)
    line_height = 10  # Adjust this value based on your desired spacing between items
    y_position = height - 300

    for index, item in enumerate(invoice.items.all(), start=1):
        pdf.drawString(30, y_position, str(index))
        pdf.drawString(65, y_position, item.item_name)
        pdf.drawString(150, y_position, str(item.mrp))
        pdf.drawString(190, y_position, str(item.quantity))
        pdf.drawString(230, y_position, str(item.base_rate))
        pdf.drawString(285, y_position, str(item.disc_1))
        pdf.drawString(320, y_position, str(item.disc_2))
        pdf.drawString(350, y_position, str(item.taxable_amount))
        pdf.drawString(400, y_position, str(item.cgst_amount))
        pdf.drawString(400, y_position - 10, f"{str(item.cgst_rate)}%")
        pdf.drawString(450, y_position, str(item.sgst_amount))
        pdf.drawString(450, y_position - 10, f"{str(item.sgst_rate)}%")
        pdf.drawString(500, y_position, str(item.net_amount))

        # Move to the next line with a gap
        y_position -= line_height

        # Check if it's not the last item to avoid extra lines
        if index < len(invoice.items.all()):
            y_position -= line_height

    # Add logic here for details related to all items (if needed)
    # ...

    # Example for displaying total CGST and SGST at the end
    # pdf.drawString(400, y_position, "Total CGST:")
    # pdf.drawString(450, y_position, str(invoice.total_cgst_amount))
    # pdf.drawString(400, y_position - line_height, "Total SGST:")
    # pdf.drawString(450, y_position - line_height, str(invoice.total_sgst_amount))

    # PDF generation logic here
    # You can use the same logic as in your previous code

    # pdf.drawString(100, 750, f"Invoice Number: {invoice.invoice_number}")
    # pdf.drawString(100, 730, f"Invoice Date: {invoice.invoice_date}")
    # pdf.drawString(100, 710, f"Customer: {invoice.customer_name}")
    # #
    # # Add order items
    # y_position = 690
    # for item in invoice.items.all():
    #     pdf.drawString(100, y_position, f"Item: {item.item_name}")
    #     pdf.drawString(200, y_position, f"Quantity: {item.quantity}")
    #     pdf.drawString(300, y_position, f"Net Amount: {item.net_amount}")
    #     y_position -= 20

    # Add total amount and discounts
    # pdf.drawString(100, y_position, f"Order Discount: {invoice.order_discount}")
    # y_position -= 20
    # pdf.drawString(100, y_position, f"Total Amount: {invoice.total_amount}")

    # Save the PDF to the BytesIO buffer
    pdf.showPage()
    pdf.save()

    # Move the buffer's position back to the beginning
    buffer.seek(0)

    # Specify the local file path to save the PDF
    pdf_file_path = fr"C:\Users\Vrdella\Documents\invoice\{invoice.invoice_number}.pdf"
    with open(pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(buffer.read())

    # Close the BytesIO buffer
    buffer.close()

    return HttpResponse("PDF saved to local storage.")
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    pdf.setPageSize((width, height))
    pdf.rect(35, height - 120, 265, 80)
    pdf.rect(300, height - 120, 265, 80)
    logo_path = invoice.logo
    pdf.setFont("Helvetica", 8, leading=True)
    pdf.drawImage(str(logo_path), 40, height - 110, width=90, height=50)
    pdf.drawString(80, height - 80, f"{invoice.company_address}")
