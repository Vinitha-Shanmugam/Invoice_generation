from rest_framework.generics import CreateAPIView
from . import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from . import models
from rest_framework.response import Response
from rest_framework import status


class InvoiceCreation(CreateAPIView):
    serializer_class = serializers.InvoiceSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = serializers.InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'Invoice created successfully',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemCreation(CreateAPIView):
    serializer_class = serializers.ItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'Item details registered successfully',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import os
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Invoice
from .serializers import InvoiceSerializer

from fpdf import FPDF


def axis(y, pdf):
    y += 5
    if y > 270:
        y = 10
        pdf.add_page()
        return y
    return y


def generate_pdf(request, invoice_id):
    # Retrieve the Invoice object from the database
    invoice = get_object_or_404(Invoice, id=invoice_id)
    # item=get_object_or_404(Item)
    # Serialize the Invoice object
    serializer = InvoiceSerializer(invoice)

    # Create a BytesIO buffer to hold the PDF content

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font('times', '', 10)
    pdf.rect(10, 10, 95, 20)
    logo_path = invoice.logo
    pdf.image(str(logo_path), 11, 11, 15, 15)
    pdf.set_xy(35, 13)
    pdf.multi_cell(60, 5, str(invoice.company_address), align='R')

    pdf.set_font('times', '', 10)
    pdf.set_xy(106, 11)
    pdf.cell(105, 10, f"Contact : {invoice.phone_number}", align='L')
    pdf.set_xy(106, 15)
    pdf.cell(105, 10, f"FASSAI Number : {invoice.fssai_number}", align='L')
    pdf.rect(105, 10, 95, 15)

    pdf.set_font('times', '', 12)
    pdf.rect(105, 25, 95, 5)
    pdf.set_xy(125, 25)
    pdf.cell(30, 5, "Customer Invoice", align='C')

    pdf.set_font('times', '', 10)
    pdf.rect(10, 30, 190, 5)
    pdf.set_xy(11, 30)
    pdf.cell(0, 5, "Customer/Consignee Name & address")

    pdf.set_font('times', '', 10)
    pdf.rect(10, 35, 95, 20)
    pdf.set_xy(11, 35)
    pdf.multi_cell(45, 8, invoice.customer_address)

    pdf.set_font('times', '', 10)
    pdf.rect(105, 35, 45, 5)
    pdf.set_xy(105, 35)
    pdf.cell(0, 5, "Invoice NO", align='L')

    pdf.set_font('times', '', 10)
    pdf.rect(150, 35, 50, 5)
    pdf.set_xy(151, 35)
    pdf.cell(0, 5, str(invoice.invoice_number), align='L')

    pdf.set_font('times', '', 10)
    pdf.rect(105, 40, 45, 5)
    pdf.set_xy(106, 40)
    pdf.cell(0, 5, "Date", align='L')

    pdf.set_font('times', '', 10)
    pdf.rect(150, 40, 50, 5)
    pdf.set_xy(151, 40)
    pdf.cell(0, 5, str(invoice.invoice_date), align='L')

    pdf.set_font('times', '', 10)
    pdf.rect(105, 45, 45, 5)
    pdf.set_xy(105, 45)
    pdf.cell(0, 5, "Revision", align='L')

    pdf.set_font('times', '', 10)
    pdf.rect(150, 45, 50, 5)
    pdf.set_xy(151, 45)
    pdf.cell(0, 5, "")

    pdf.set_font('times', '', 10)
    pdf.rect(105, 50, 45, 5)
    pdf.set_xy(106, 50)
    pdf.cell(0, 5, "Date", align='L')

    pdf.set_font('times', '', 10)
    pdf.rect(150, 50, 50, 5)
    pdf.set_xy(151, 50)
    pdf.cell(0, 5, "")

    pdf.set_font('times', '', 10)
    pdf.rect(10, 55, 40, 5)
    pdf.set_xy(11, 55)
    pdf.cell(0, 5, 'Email-id')

    pdf.set_font('times', '', 10)
    pdf.rect(50, 55, 150, 5)
    pdf.set_xy(51, 55)
    pdf.cell(0, 5, str(invoice.customer_email))

    pdf.set_font('times', '', 10)
    pdf.rect(10, 60, 40, 5)
    pdf.set_xy(11, 60)
    pdf.cell(0, 5, 'Contact Person/Mobile')

    pdf.set_font('times', '', 10)
    pdf.rect(50, 60, 150, 5)
    pdf.set_xy(51, 60)
    pdf.cell(0, 5, invoice.customer_mobile_number)

    pdf.set_font('times', '', 10)
    pdf.rect(10, 65, 10, 5)
    pdf.set_xy(10, 65)
    pdf.cell(0, 5, 'S.NO')

    pdf.set_font('times', '', 10)
    pdf.rect(20, 65, 25, 5)
    pdf.set_xy(21, 65)
    pdf.cell(0, 5, 'Item_name')

    pdf.set_font('times', '', 10)
    pdf.rect(45, 65, 15, 5)
    pdf.set_xy(45, 65)
    pdf.cell(0, 5, 'MRP')

    pdf.set_font('times', '', 10)
    pdf.rect(60, 65, 15, 5)
    pdf.set_xy(60, 65)
    pdf.cell(0, 5, 'QTY')

    pdf.set_font('times', '', 10)
    pdf.rect(75, 65, 20, 5)
    pdf.set_xy(75, 65)
    pdf.cell(0, 5, 'Base Rate')

    pdf.set_font('times', '', 10)
    pdf.rect(95, 65, 15, 5)
    pdf.set_xy(95, 65)
    pdf.cell(0, 5, 'Disc1')

    pdf.set_font('times', '', 10)
    pdf.rect(110, 65, 15, 5)
    pdf.set_xy(110, 65)
    pdf.cell(0, 5, 'Disc2')

    pdf.set_font('times', '', 10)
    pdf.rect(125, 65, 20, 5)
    pdf.set_xy(125, 65)
    pdf.cell(0, 5, 'Tax_amt')

    pdf.set_font('times', '', 10)
    pdf.rect(145, 65, 15, 5)
    pdf.set_xy(145, 65)
    pdf.cell(0, 5, 'CGST')

    pdf.set_font('times', '', 10)
    pdf.rect(160, 65, 15, 5)
    pdf.set_xy(160, 65)
    pdf.cell(0, 5, 'UTGST')

    pdf.set_font('times', '', 10)
    pdf.rect(175, 65, 25, 5)
    pdf.set_xy(175, 65)
    pdf.cell(0, 5, 'Net_amt')
    y = 65
    for index, item in enumerate(invoice.items.all(), start=1):
        y = axis(y, pdf)
        pdf.set_font('times', '', 10)
        pdf.rect(10, y, 10, 5)
        pdf.set_xy(10, y)
        pdf.cell(0, 5, str(index))

        pdf.set_font('times', '', 10)
        pdf.rect(20, y, 25, 5)
        pdf.set_xy(21, y)
        pdf.cell(0, 5, item.item_name)

        pdf.set_font('times', '', 10)
        pdf.rect(45, y, 15, 5)
        pdf.set_xy(45, y)
        pdf.cell(0, 5, str(item.mrp))

        pdf.set_font('times', '', 10)
        pdf.rect(60, y, 15, 5)
        pdf.set_xy(60, y)
        pdf.cell(0, 5, str(item.quantity))

        pdf.set_font('times', '', 10)
        pdf.rect(75, y, 20, 5)
        pdf.set_xy(75, y)
        pdf.cell(0, 5, str(item.base_rate))

        pdf.set_font('times', '', 10)
        pdf.rect(95, y, 15, 5)
        pdf.set_xy(95, y)
        pdf.multi_cell(10, 5, str(item.disc_1))

        pdf.set_font('times', '', 10)
        pdf.rect(110, y, 15, 5)
        pdf.set_xy(110, y)
        pdf.cell(0, 5, str(item.disc_2))

        pdf.set_font('times', '', 10)
        pdf.rect(125, y, 20, 5)
        pdf.set_xy(125, y)
        pdf.cell(0, 5, str(item.taxable_amount))

        pdf.set_font('times', '', 10)
        pdf.rect(145, y, 15, 5)
        pdf.set_xy(145, y)
        pdf.cell(0, 5, str(item.cgst_amount))

        pdf.set_font('times', '', 10)
        pdf.rect(160, y, 15, 5)
        pdf.set_xy(160, y)
        pdf.cell(0, 5, str(item.sgst_amount))

        pdf.set_font('times', '', 10)
        pdf.rect(175, y, 25, 5)
        pdf.set_xy(175, y)
        pdf.cell(0, 5, str(item.net_amount))
    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(10, y, 190, 5)

    y = axis(y, pdf)
    pdf.set_font('times', 'BU', 10)
    pdf.set_text_color(255, 0, 0)
    pdf.rect(10, y, 95, 25)
    pdf.set_xy(11, y)
    pdf.cell(0, 5, 'Note')
    pdf.set_font('times', '', 10)
    pdf.set_text_color(255, 0, 0)
    pdf.set_xy(11, y + 4)
    pdf.multi_cell(85, 5, invoice.product_note)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 45, 5)
    pdf.set_xy(105, y)
    pdf.cell(0, 5, 'Sub_Total')

    pdf.set_text_color(255, 0, 0)
    pdf.set_font('times', '', 10)
    pdf.rect(150, y, 15, 5)
    pdf.set_xy(151, y)
    pdf.cell(0, 5, '4')

    pdf.set_font('times', '', 10)
    pdf.rect(165, y, 35, 5)
    pdf.set_xy(166, y)
    pdf.cell(0, 5, '31202')

    y = axis(y, pdf)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 45, 5)
    pdf.set_xy(105, y)
    pdf.cell(0, 5, 'Others')

    pdf.set_font('times', '', 10)
    pdf.rect(150, y, 15, 5)
    pdf.set_xy(151, y)
    pdf.cell(0, 5, '0')

    pdf.set_font('times', '', 10)
    pdf.rect(165, y, 35, 5)
    pdf.set_xy(166, y)
    pdf.cell(0, 5, '0.00')

    if invoice.Company_name == 'Voni':
        y = axis(y, pdf)
        pdf.set_font('times', '', 10)
        pdf.rect(105, y, 45, 5)
        pdf.set_xy(105, y)
        pdf.cell(0, 5, 'Installation')

    elif invoice.Company_name == 'Vrihodha Organics Private Limited':
        y = axis(y, pdf)
        pdf.set_font('times', '', 10)
        pdf.rect(105, y, 45, 5)
        pdf.set_xy(105, y)
        pdf.cell(0, 5, 'Transport')

    pdf.set_font('times', '', 10)
    pdf.rect(165, y, 35, 5)
    pdf.set_xy(166, y)
    pdf.cell(0, 5, '')

    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 60, 5)
    pdf.set_xy(105, y)
    pdf.cell(0, 5, 'Total Amount')

    total = item.taxable_amount + item.net_amount
    pdf.set_font('times', '', 10)
    pdf.rect(165, y, 35, 5)
    pdf.set_xy(166, y)
    pdf.cell(0, 5, 'INR ' + str(total))

    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 60, 5)
    pdf.set_xy(106, y)
    pdf.cell(0, 5, 'Round Off')

    pdf.set_font('times', '', 10)
    pdf.rect(165, y, 35, 5)
    pdf.set_xy(166, y)
    pdf.cell(0, 5, 'INR ' + str(round(total)))

    y = axis(y, pdf)
    pdf.set_text_color(255, 0, 0)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 15, 5)
    pdf.set_xy(105, y)
    pdf.cell(0, 5, 'In Words')

    pdf.set_text_color(255, 0, 0)
    pdf.set_font('times', '', 10)
    pdf.rect(120, y, 80, 5)
    pdf.set_xy(120, y)
    pdf.cell(0, 5, 'Thirty-One Thousand Two Hundred Three Rupees')

    y = axis(y, pdf)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('times', '', 10)
    pdf.rect(10, y, 40, 10)
    pdf.set_xy(11, y)
    pdf.cell(0, 5, 'OUR PAN_NO')
    pdf.set_xy(11, y + 4)
    pdf.cell(0, 5, str(invoice.company_pan))

    pdf.set_font('times', '', 10)
    pdf.rect(50, y, 55, 10)
    pdf.set_xy(51, y)
    pdf.multi_cell(0, 5, 'OUR GSTIN')
    pdf.set_xy(51, y + 4)
    pdf.multi_cell(0, 5, str(invoice.gst_number))

    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 95, 5)
    pdf.set_xy(106, y)
    pdf.cell(0, 5, 'Terms & Conditions:')

    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 15, 5)
    pdf.set_xy(106, y)
    pdf.cell(0, 5, 'Price')

    pdf.set_font('times', '', 10)
    pdf.rect(120, y, 80, 10)
    pdf.set_xy(120, y)
    pdf.cell(0, 5, 'Ex-GoDown-COIMBATORE')

    y = axis(y, pdf)
    pdf.set_font('times', 'BU', 10)
    pdf.rect(10, y, 95, 40)
    pdf.set_xy(11, y)
    pdf.cell(0, 5, 'Bank Details')
    pdf.set_font('times', '', 10)
    pdf.set_xy(11, y + 4)
    pdf.multi_cell(0, 5, f'Name : {invoice.company_accHolder}')
    pdf.set_xy(11, y + 8)
    pdf.multi_cell(0, 5, f'Bank : {invoice.company_bankName}')
    pdf.set_xy(11, y + 12)
    pdf.multi_cell(0, 5, f'A/C No : {invoice.company_accountNo}')
    pdf.set_xy(11, y + 16)
    pdf.multi_cell(0, 5, f'IFSC : {invoice.company_bankifsc}')
    pdf.set_xy(11, y + 20)
    pdf.multi_cell(0, 5, f'Branch : {invoice.company_bankBranch}')

    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 15, 5)
    pdf.set_xy(106, y)
    pdf.cell(0, 5, 'GST')

    if item.sgst_rate == '' or item.sgst_rate is None:
        pass
    else:
        pdf.set_font('times', '', 10)
        pdf.rect(135, y, 15, 5)
        pdf.set_xy(136, y)
        pdf.cell(0, 5, 'SGST')

        pdf.set_font('times', '', 10)
        pdf.rect(150, y, 15, 5)
        pdf.set_xy(151, y)
        pdf.cell(0, 5, str(item.sgst_rate) + "%")

    if item.cgst_rate == '' or item.cgst_rate is None:
        pass
    else:
        pdf.set_font('times', '', 10)
        pdf.rect(165, y, 15, 5)
        pdf.set_xy(166, y)
        pdf.cell(0, 5, 'CGST')

        pdf.set_font('times', '', 10)
        pdf.rect(180, y, 20, 5)
        pdf.set_xy(181, y)
        pdf.cell(0, 5, str(item.cgst_rate) + "%")

    pdf.set_font('times', '', 10)
    pdf.rect(120, y, 80, 5)
    pdf.set_xy(120, y)
    pdf.cell(0, 5, '18%')

    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 15, 5)
    pdf.set_xy(106, y)
    pdf.cell(0, 5, 'Frieght')

    pdf.set_font('times', '', 10)
    pdf.rect(120, y, 80, 5)
    pdf.set_xy(120, y)
    pdf.cell(0, 5, 'Extra as Actual')

    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y, 15, 10)
    pdf.set_xy(106, y)
    pdf.cell(0, 10, 'Validity')

    pdf.set_font('times', '', 8)
    pdf.rect(120, y, 80, 10)
    pdf.set_xy(120, y)
    pdf.multi_cell(78, 5,
                   'As mentioned in the product package')

    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y + 5, 15, 10)
    pdf.set_xy(106, y + 5)
    pdf.cell(0, 10, 'Delivery')

    pdf.set_font('times', '', 8)
    pdf.rect(120, y + 5, 80, 10)
    pdf.set_xy(120, y + 5)
    pdf.multi_cell(78, 5, 'We shall supply the items within 3 week from the receipt of your confirmed order.')

    y = axis(y, pdf)
    pdf.set_font('times', '', 10)
    pdf.rect(105, y + 10, 15, 10)
    pdf.set_xy(106, y + 10)
    pdf.cell(0, 10, 'Payment')

    pdf.set_font('times', '', 10)
    pdf.rect(120, y + 10, 80, 10)
    pdf.set_xy(120, y + 10)
    pdf.cell(0, 10, item.payment_type)

    if invoice.Company_name == "Vrihodha Organics":
        y = axis(y, pdf)
        pdf.set_font('times', '', 10)
        pdf.rect(10, y + 15, 190, 20)
        pdf.set_xy(11, y + 20)
        pdf.cell(0, 10, 'THANK YOU FOR YOUR BUSINESS', align='C')

    elif invoice.Company_name == "Voni":
        y = axis(y, pdf)
        pdf.set_font('times', '', 10)
        pdf.rect(10, y + 15, 190, 20)
        pdf.set_xy(11, y + 20)
        pdf.cell(0, 10, 'THANK YOU FOR YOUR BUSINESS', align='C')

        pdf.set_font('times', '', 10)
        pdf.rect(105, y + 15, 25, 10)
        pdf.set_xy(106, y + 15)
        pdf.cell(0, 10, 'Created By')

        pdf.set_font('times', '', 10)
        pdf.rect(130, y + 15, 25, 10)
        pdf.set_xy(131, y + 15)
        pdf.cell(0, 10, 'Ashema Begam')

        pdf.set_font('times', '', 10)
        pdf.rect(155, y + 15, 45, 10)
        pdf.set_xy(156, y + 15)
        pdf.cell(0, 10, '7810021422')

        y = axis(y, pdf)
        pdf.set_font('times', '', 10)
        pdf.rect(105, y + 20, 25, 10)
        pdf.set_xy(106, y + 20)
        pdf.cell(0, 10, 'Executive')

        pdf.set_font('times', '', 10)
        pdf.rect(130, y + 20, 25, 10)
        pdf.set_xy(131, y + 20)
        pdf.cell(0, 10, 'Mukesh Tiwari')

        pdf.set_font('times', '', 10)
        pdf.rect(155, y + 20, 45, 10)
        pdf.set_xy(156, y + 20)
        pdf.cell(0, 10, '7810021451')

    pdf.output('pdf.pdf')


# ReportLab
# import os
# from io import BytesIO
# from django.http import HttpResponse
# from reportlab.lib.pagesizes import letter, landscape
# from reportlab.pdfgen import canvas
# from django.shortcuts import get_object_or_404
# from django.conf import settings
#
# from .models import Invoice
# from .serializers import InvoiceSerializer
#
#
# def generate_pdf(request, invoice_id):
#     # Retrieve the Invoice object from the database
#     invoice = get_object_or_404(Invoice, id=invoice_id)
#     # item=get_object_or_404(Item)
#     # Serialize the Invoice object
#     serializer = InvoiceSerializer(invoice)
#
#     # Create a BytesIO buffer to hold the PDF content
#     buffer = BytesIO()
#
#     # Create the PDF object using the BytesIO buffer
#     pdf = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4
#     pdf.setPageSize((width, height))
#     pdf.drawString(250, height - 120, "Customer Invoice")
#     # Draw a horizontal line at the top of the page
#     pdf.setStrokeColorRGB(0, 0, 1)
#     pdf.line(30, height - 130, 30 + 530, height - 130)
#
#     # Set the fill color to blue
#     pdf.setFillColorRGB(0, 0, 1)
#
#     # Draw the text in blue color
#     pdf.setFont("Helvetica", 7)
#     pdf.drawString(30, height - 165, f"{invoice.Company_name}")
#     pdf.setFillColorRGB(0, 0, 0)
#     pdf.drawString(30, height - 180, f"{invoice.company_address}")
#     pdf.drawString(30, height - 200, f"Phone Number:{invoice.phone_number}")
#     pdf.drawString(30, height - 210, f"GST Number:{invoice.gst_number}")
#     pdf.drawString(30, height - 220, f"FSSAI Number:{invoice.fssai_number}")
#     pdf.drawString(320, height - 165, 'To')
#     pdf.drawString(320, height - 180, f"Invoice No: {invoice.invoice_number}")
#     pdf.drawString(320, height - 190, f"Invoice Date: {invoice.invoice_date}")
#     pdf.drawString(320, height - 200, f"Customer: {invoice.customer_name}")
#     pdf.drawString(320, height - 210, f"Address: {invoice.customer_address}")
#     pdf.drawString(320, height - 220, f"Customer Mobile No: {invoice.customer_mobile_number}")
#     logo_path = invoice.logo
#     pdf.drawImage(str(logo_path), 30, height - 80, width=100, height=50)
#     pdf.setFont("Helvetica-Bold", 6)
#     pdf.setFillColorRGB(0, 0, 1)
#     pdf.drawString(30, height - 260, "Your Orders")
#     pdf.setFillColorRGB(0, 0, 0)
#     pdf.drawString(30, height - 275, "S.No")
#     pdf.setFont("Helvetica", 6)
#     pdf.drawString(65, height - 275, "Item Name")
#     pdf.drawString(150, height - 275, "MRP")
#     pdf.drawString(190, height - 275, "Quantity")
#     pdf.drawString(190, height - 285, "pcs")
#     pdf.drawString(230, height - 275, "Base Rate")
#     pdf.drawString(285, height - 275, "Disc 1")
#     pdf.drawString(320, height - 275, "Disc 2")
#     pdf.drawString(350, height - 275, "Taxable amt")
#     pdf.drawString(400, height - 275, "CGST Amt")
#     pdf.drawString(400, height - 285, "CGST Tax%")
#     pdf.drawString(450, height - 275, "S/UTGST Amt")
#     pdf.drawString(450, height - 285, "S/UTGST Amt")
#     pdf.drawString(500, height - 275, "Net Amount")
#     pdf.setStrokeColorRGB(128, 0, 128)
#     pdf.line(30, height - 290, 30 + 530, height - 290)
#     line_height = 10  # Adjust this value based on your desired spacing between items
#     y_position = height - 300
#
#     for index, item in enumerate(invoice.items.all(), start=1):
#         pdf.drawString(30, y_position, str(index))
#         pdf.drawString(65, y_position, item.item_name)
#         pdf.drawString(150, y_position, str(item.mrp))
#         pdf.drawString(190, y_position, str(item.quantity))
#         pdf.drawString(230, y_position, str(item.base_rate))
#         pdf.drawString(285, y_position, str(item.disc_1))
#         pdf.drawString(320, y_position, str(item.disc_2))
#         pdf.drawString(350, y_position, str(item.taxable_amount))
#         pdf.drawString(400, y_position, str(item.cgst_amount))
#         pdf.drawString(400, y_position - 10, f"{str(item.cgst_rate)}%")
#         pdf.drawString(450, y_position, str(item.sgst_amount))
#         pdf.drawString(450, y_position - 10, f"{str(item.sgst_rate)}%")
#         pdf.drawString(500, y_position, str(item.net_amount))
#
#         # Move to the next line with a gap
#         y_position -= line_height
#
#         # Check if it's not the last item to avoid extra lines
#         if index < len(invoice.items.all()):
#             y_position -= line_height
#
#     # Add logic here for details related to all items (if needed)
#     # ...
#
#     # Example for displaying total CGST and SGST at the end
#     # pdf.drawString(400, y_position, "Total CGST:")
#     # pdf.drawString(450, y_position, str(invoice.total_cgst_amount))
#     # pdf.drawString(400, y_position - line_height, "Total SGST:")
#     # pdf.drawString(450, y_position - line_height, str(invoice.total_sgst_amount))
#
#     # PDF generation logic here
#     # You can use the same logic as in your previous code
#
#     # pdf.drawString(100, 750, f"Invoice Number: {invoice.invoice_number}")
#     # pdf.drawString(100, 730, f"Invoice Date: {invoice.invoice_date}")
#     # pdf.drawString(100, 710, f"Customer: {invoice.customer_name}")
#     # #
#     # # Add order items
#     # y_position = 690
#     # for item in invoice.items.all():
#     #     pdf.drawString(100, y_position, f"Item: {item.item_name}")
#     #     pdf.drawString(200, y_position, f"Quantity: {item.quantity}")
#     #     pdf.drawString(300, y_position, f"Net Amount: {item.net_amount}")
#     #     y_position -= 20
#
#     # Add total amount and discounts
#     # pdf.drawString(100, y_position, f"Order Discount: {invoice.order_discount}")
#     # y_position -= 20
#     # pdf.drawString(100, y_position, f"Total Amount: {invoice.total_amount}")
#
#     # Save the PDF to the BytesIO buffer
#     pdf.showPage()
#     pdf.save()
#
#     # Move the buffer's position back to the beginning
#     buffer.seek(0)
#
#     # Specify the local file path to save the PDF
#     pdf_file_path = fr"C:\Users\Vrdella\Documents\invoice\{invoice.invoice_number}.pdf"
#     with open(pdf_file_path, 'wb') as pdf_file:
#         pdf_file.write(buffer.read())
#
#     # Close the BytesIO buffer
#     buffer.close()
#
#     return HttpResponse("PDF saved to local storage.")
