from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import csv
from django.db.models import Sum
from .models import Sale, Purchase, Items
from datetime import datetime


def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'index.html')


@login_required
def home(request):
    query = request.GET.get('q', '')

    # Search by item name if a query is provided
    if query:
        items = Items.objects.filter(name__icontains=query)
    else:
        items = Items.objects.all()

    return render(request, 'home.html', {
        'items': items,
        'query': query,
    })


@login_required
def purchase_or_sale(request):
    if request.method == 'POST':
        item_id = request.POST.get('item')  # Corrected to match 'Items' model
        quantity = int(request.POST.get('quantity'))
        action = request.POST.get('action')
        
        item = get_object_or_404(Items, id=item_id)
        
        if action == 'purchase':
            # Handle purchase
            Purchase.objects.create(item=item, quantity=quantity, purchase_price=item.price)
            messages.success(request, f'Successfully purchased {quantity} units of {item.name}.')
        elif action == 'sale':
            # Handle sale
            if quantity <= item.quantity_in_stock:
                Sale.objects.create(item=item, quantity=quantity, sale_price=item.price)
                messages.success(request, f'Successfully sold {quantity} units of {item.name}.')
            else:
                messages.error(request, f'Not enough stock for {item.name}.')

    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def report_view(request):
    # Initialize empty lists for reports and profit
    sales = []
    purchases = []
    profit = 0

    # Default date range (last 30 days)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            start_date = None
            end_date = None

    # Query based on date range
    if start_date and end_date:
        sales = Sale.objects.filter(date__range=[start_date, end_date])
        purchases = Purchase.objects.filter(date__range=[start_date, end_date])
    else:
        sales = Sale.objects.all()
        purchases = Purchase.objects.all()

    # Calculate total sales and purchases
    total_sales = sales.aggregate(total=Sum('total_price'))['total'] or 0
    total_purchases = purchases.aggregate(total=Sum('total_price'))['total'] or 0
    profit = total_sales - total_purchases

    # If no records found, show a message
    no_records_message = "No records found for the selected date range." if not sales and not purchases else ""

    context = {
        'sales': sales,
        'purchases': purchases,
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'profit': profit,
        'no_records_message': no_records_message,
    }

    return render(request, 'report.html', context)


@login_required
def download_csv(request):
    start_date = request.POST.get('start_date', None)
    end_date = request.POST.get('end_date', None)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Type', 'Item', 'Quantity', 'Price', 'Total Price', 'Date'])

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            start_date = None
            end_date = None

    if start_date and end_date:
        sales = Sale.objects.filter(date__range=[start_date, end_date])
        purchases = Purchase.objects.filter(date__range=[start_date, end_date])
    else:
        sales = Sale.objects.all()
        purchases = Purchase.objects.all()

    # Write sales to CSV
    for sale in sales:
        writer.writerow(['Sale', sale.item.name, sale.quantity, sale.sale_price, sale.total_price, sale.date])

    # Write purchases to CSV
    for purchase in purchases:
        writer.writerow(['Purchase', purchase.item.name, purchase.quantity, purchase.purchase_price, purchase.total_price, purchase.date])

    return response
