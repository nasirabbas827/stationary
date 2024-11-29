from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Category, Items, Sale, Purchase
from django.utils.timezone import localdate


class SaleAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'sale_price', 'total_price', 'date')
    list_filter = ('date',)  # Filter by date
    search_fields = ('item__name',)

    # CSV export functionality
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        # Creating a response with the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales.csv"'

        writer = csv.writer(response)
        writer.writerow(['Item', 'Quantity', 'Sale Price', 'Total Price', 'Date'])

        # Write data rows
        for sale in queryset:
            writer.writerow([sale.item.name, sale.quantity, sale.sale_price, sale.total_price, sale.date])

        return response

    export_to_csv.short_description = "Export selected sales to CSV"


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'purchase_price', 'total_price', 'date')
    list_filter = ('date',)  # Filter by date
    search_fields = ('item__name',)

    # CSV export functionality
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        # Creating a response with the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="purchases.csv"'

        writer = csv.writer(response)
        writer.writerow(['Item', 'Quantity', 'Purchase Price', 'Total Price', 'Date'])

        # Write data rows
        for purchase in queryset:
            writer.writerow([purchase.item.name, purchase.quantity, purchase.purchase_price, purchase.total_price, purchase.date])

        return response

    export_to_csv.short_description = "Export selected purchases to CSV"


# Registering the models with their custom admin classes
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Purchase, PurchaseAdmin)
