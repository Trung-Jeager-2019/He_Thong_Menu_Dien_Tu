from django import template
from decimal import Decimal
from Menu_Dien_Tu_App.models import Restaurant, MenuItem, Order, OrderedItem, Table
register = template.Library()


@register.filter
def calculateCharges(total, output='delivery'):
    if not total:
        return 0.0
    delivery_charge = Decimal(total) * Decimal(0.08)

    if output == 'delivery':
        total = 0
    
    return round(total + delivery_charge, 2)


@register.filter
def calculatePrice(items, output='total'):
    priceDetails = {}

    total_price = 0

    for item in items:
        if not item['quantity']:
            item['quantity'] = 1
        total_price = total_price + item['price'] * item['quantity']

    total_delivery = total_price

    grad_total = total_price

    priceDetails['payable'] = round(grad_total, 2)
    # priceDetails['total_delivery'] = round(total_delivery, 2)
    priceDetails['total'] = round(total_price, 2)

    return priceDetails[output]


@register.filter
def calculateTotalQuantity(items):
    total = 0
    for item in items:
        if not item['quantity']:
            item['quantity'] = 1
        total = total + item['quantity']
    return total


@register.filter
def displayPrice(price):
    price = str(price).split("000", 1)[0] + ",000 đ"
    return price

@register.filter
def listOrderID(ID):
    ordersFromDb = Order.objects.filter(id=ID)
    return ordersFromDb

@register.filter
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price
