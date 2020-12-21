from django.db import transaction
from django.shortcuts import render, redirect
from Menu_Dien_Tu.utils import processData, toId, getRole, getTotalFromOrder
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Menu_Dien_Tu_App.models import Restaurant, MenuItem, Order, OrderedItem
from datetime import datetime

# Create your views here

@login_required
def checkout(request):
    items = request.session.get('items')

    if request.method != 'POST':
        messages.error(request, 'Vui lòng thanh toán!')
        return redirect('cart')

    if not items or len(items) <= 0:
        messages.error(request, 'Vui lòng chọn ít nhất 1 mục!')
        return redirect('cart')

    placedOrdersCount = 0

    try:
        with transaction.atomic():
            total_price = getTotalFromOrder(items)
            dateTime = datetime.now()

            result_date = datetime(
                dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second, 00
                )
            print(result_date)

            orderDetails = Order.objects.create(
                user=request.user, deliveredOn=None, total_price=total_price, date=result_date)

            for item in items:
                menuItem = MenuItem.objects.filter(id=item['id']).first()
                OrderedItem.objects.create(
                    item=menuItem, quantity=item['quantity'], order=orderDetails)
                placedOrdersCount += 1

    except Exception as e:
        print(e)
        placedOrdersCount = 0
        messages.error(request, "Không thể đặt đơn, vui lòng thử lại")
        return redirect('cart')

    request.session['items'] = []

    messages.info(request, 'Đơn của bạn đã được ghi nhận.')
    return redirect('pay')

@login_required
def pay(request):
    data = {
        'title': 'Thanh toán'
    }
    return render(request, 'pay.html', processData(request, data))

@login_required
def completePay(request):
    data = {
        'title': 'Đơn của bạn đã được nhận'
    }
    return render(request, 'complete_pay.html', processData(request, data))