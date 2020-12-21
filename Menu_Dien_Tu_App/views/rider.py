from django.db.models import Q
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from Menu_Dien_Tu.utils import processData, toId, getRole
from django.contrib.auth.decorators import login_required
from Menu_Dien_Tu_App.models import Restaurant, MenuItem, Order, OrderedItem


@login_required
def getOrder(request):
    data = {'title': 'Danh Sách Đơn'}
    
    ordersFromDb = Order.objects.filter(Q(delivered=False), Q(rider=None) | Q(rider=request.user))
    
    newOrders = []
    for order in ordersFromDb:
        tmp_order = {}
        tmp_order['id'] = order.id
        tmp_order['delivered'] = order.delivered
        tmp_order['rider'] = order.rider
        tmp_order['table'] = order.user.username
        print(order.user.username)
        tmp_order['dateTime'] = order.date
        tmp_order['total'] = order.total_price
        tmp_order['items'] = OrderedItem.objects.filter(
            order=order).order_by('-id')
        newOrders.append(tmp_order)

    print(newOrders)

    data['orders'] = newOrders

    return render(request, 'partner/rider/get_order.html', processData(request, data))


@login_required
def takeForDelivery(request):
    data = {'title': 'Nhận Đơn'}
    id = request.GET.get('id')
    if not id:
        messages.error(request, "")
        return redirect('get_order')
    try:
        orders = Order.objects.filter(id=id)
        for item in orders:
            item.rider = request.user
            item.delivered = False
            item.save()
        
    except Exception as e:
        print(e)
    messages.info(request, "Order mã " + id + " đã được nhận!")
    return redirect('get_order')


@login_required
def completeDelivery(request):
    data = {'title': 'Hoàn Thành Đơn'}
    id = request.GET.get('id')
    if not id:
        messages.error(request, 'Nhận đơn để hoàn thành!')
    orders = Order.objects.filter(id=id, rider=request.user)
    if not orders:
        messages.error(request, 'Không tìm thấy đơn đã hoàn thành!')
    else:
        for item in orders:
            item.delivered = True
            item.deliveredOn = datetime.now()
            item.save()
        messages.info(
            request, "Đơn mã " + id + " đã phục vụ khách hàng!")
    return redirect('get_order')

@login_required
def deliveryHistory(request):
    data = {'title': 'Nhật Ký Đơn'}

    ordersFromDb = Order.objects.filter(rider=request.user, delivered=True)
    
    newOrders = []
    for order in ordersFromDb:
        tmp_order = {}
        tmp_order['id'] = order.id
        tmp_order['delivered'] = order.delivered
        tmp_order['rider'] = order.rider
        tmp_order['table'] = order.user.username
        print(order.user.username)
        tmp_order['dateTime'] = order.date
        tmp_order['total'] = order.total_price
        tmp_order['items'] = OrderedItem.objects.filter(
            order=order).order_by('-id')
        newOrders.append(tmp_order)

    print(newOrders)

    data['orders'] = newOrders
    return render(request, 'partner/rider/delivery_history.html', processData(request, data))
