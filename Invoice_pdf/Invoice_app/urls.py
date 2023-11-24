# from django.urls import path
# from .views import (
#     CustomerCreateView,
#     ProductCreateView,
#     CompanyListCreateView,
#     InvoiceListCreateView,
# )
#
# urlpatterns = [
#     # Customer and Product URLs
#     path('customers/create/', CustomerCreateView.as_view(), name='customer-create'),
#     path('products/create/', ProductCreateView.as_view(), name='product-create'),
#
#     # Company and Invoice URLs
#     path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
#     path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
# ]



# invoicing_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import InvoiceViewSet, ItemViewSet
#
# router = DefaultRouter()
# router.register(r'invoices', InvoiceViewSet)
# router.register(r'items', ItemViewSet)
from . import views
urlpatterns = [
    path('customers/create/', views.InvoiceCreation.as_view(), name='customer-create'),
    path('products/create/', views.ItemCreation.as_view(), name='product-create'),
    path('generate_pdf/<int:invoice_id>/', views.generate_pdf, name='generate_pdf'),

]
