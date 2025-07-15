from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Category, Items, Sale, Purchase
from django.utils.timezone import localdate
from django.contrib.admin import DateFieldListFilter

class SaleAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'sale_price', 'total_price', 'profit', 'date')
    list_filter = (('date', DateFieldListFilter), 'item__category')
    search_fields = ('item__name',)
    list_per_page = 20
    date_hierarchy = 'date'
    ordering = ('-date',)

    def profit(self, obj):
        """Calculate profit for a sale."""
        return (obj.sale_price - obj.item.price) * obj.quantity
    profit.short_description = 'Profit'

    actions = ['export_sales_to_csv']

    def export_sales_to_csv(self, request, queryset):
        """Export selected sales to CSV with profit."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Item', 'Quantity', 'Sale Price', 'Total Price', 'Profit', 'Date'])

        total_profit = 0
        for sale in queryset:
            profit = (sale.sale_price - sale.item.price) * sale.quantity
            total_profit += profit
            writer.writerow([sale.item.name, sale.quantity, sale.sale_price, sale.total_price, profit, sale.date])
        
        writer.writerow(['', '', '', 'Total Sale Profit', total_profit, ''])

        return response
    export_sales_to_csv.short_description = "Export selected sales to CSV"

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'purchase_price', 'total_price', 'profit', 'date')
    list_filter = (('date', DateFieldListFilter), 'item__category')
    search_fields = ('item__name',)
    list_per_page = 20
    date_hierarchy = 'date'
    ordering = ('-date',)

    def profit(self, obj):
        """Calculate profit for a purchase."""
        return (obj.item.price - obj.purchase_price) * obj.quantity
    profit.short_description = 'Profit'

    actions = ['export_purchases_to_csv']

    def export_purchases_to_csv(self, request, queryset):
        """Export selected purchases to CSV with profit."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="purchases_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Item', 'Quantity', 'Purchase Price', 'Total Price', 'Profit', 'Date'])

        total_profit = 0
        for purchase in queryset:
            profit = (purchase.item.price - purchase.purchase_price) * purchase.quantity
            total_profit += profit
            writer.writerow([purchase.item.name, purchase.quantity, purchase.purchase_price, purchase.total_price, profit, purchase.date])
        
        writer.writerow(['', '', '', 'Total Purchase Profit', total_profit, ''])

        return response
    export_purchases_to_csv.short_description = "Export selected purchases to CSV"

# Register models with their custom admin classes
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Purchase, PurchaseAdmin)