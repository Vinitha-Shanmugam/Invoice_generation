from django.db import models


class Invoice(models.Model):
    Company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    company_pan = models.CharField(max_length=100)
    company_accountNo = models.BigIntegerField()
    company_bankName = models.CharField(max_length=100)
    company_bankifsc = models.CharField(max_length=100)
    company_bankBranch = models.CharField(max_length=100)
    company_accHolder = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=15)
    fssai_number = models.CharField(max_length=15)
    product_note = models.CharField(max_length=200)
    invoice_number = models.CharField(max_length=20)
    invoice_date = models.DateField()
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField()
    customer_mobile_number = models.CharField(max_length=15)
    customer_email=models.EmailField()



class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    disc_1 = models.DecimalField(max_digits=10, decimal_places=2)
    disc_2 = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_discount = models.DecimalField(max_digits=10, decimal_places=2)
    Choices = [('Credit_card','Credit_card'),
               ('Debit_card','Debit_card'),
               ('COD','COD')]
    payment_type=models.CharField(max_length=200,choices=Choices)


