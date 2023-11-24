# # serializers.py
# from rest_framework import serializers
# from .models import Company, Customer, Product, Order, Invoice
#
#
# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = '__all__'
#
#
# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['name', 'address', 'mobile_number']
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

#
# class OrderSerializer(serializers.ModelSerializer):
#     customer = CustomerSerializer()
#     product = ProductSerializer()
#
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#
# class InvoiceSerializer(serializers.ModelSerializer):
#     company = CompanySerializer()
#     orders = OrderSerializer(many=True)
#
#     class Meta:
#         model = Invoice
#         fields = '__all__'
#
#     def create(self, validated_data):
#         company_data = validated_data.pop('company')
#         orders_data = validated_data.pop('orders')
#
#         company_instance = Company.objects.create(**company_data)
#
#         orders_instances = []
#         for order_data in orders_data:
#             order_instance = Order.objects.create(**order_data, customer=company_instance)
#             orders_instances.append(order_instance)
#
#         invoice_instance = Invoice.objects.create(company=company_instance, **validated_data)
#         invoice_instance.orders.set(orders_instances)
#
#         return invoice_instance


# invoicing_app/serializers.py
from rest_framework import serializers
from .models import Invoice, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
