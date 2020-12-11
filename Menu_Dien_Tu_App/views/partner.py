from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from Menu_Dien_Tu.utils import processData, toId, getRole
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Menu_Dien_Tu_App.models import Restaurant, MenuItem, Order, OrderedItem, Table, DescribeItem
from django_countries import countries

# Create your views here

@login_required
def viewTable(request):
    data = {'title': 'View Table for my restaurant'}
    items = Table.objects.all()
    if items and items.count() > 0:
        data['tableItems'] = items
    return render(request, 'partner/owner/view_table.html', processData(request, data))

@login_required
def createTable(request):
    data = {'title': 'Create Items to Table for my restaurant'}
    data['all_table'] = Table.objects.all()
    return render(request, 'partner/owner/create_table.html', processData(request, data))

@login_required
def createTableItem(request):
    data = {'title': 'Create Items to Table for my restaurant'}
    if request.method == "POST":
        table_name = "Bàn " + request.POST.get('name')
        if Table.objects.filter(table_name = table_name).first():
            messages.info(request, table_name + " đã tồn tại!")
        else:
            # create user 
            table_code = "Ban_" + table_name.split(" ", 1)[1]
            username = table_code
            password = "Trung14121999#"
            user = User.objects.create_user(username=username, email="", password=password, first_name="", last_name="")
            user.profile.role = "normal"
            user.save()
            # create table
            Table.objects.create(table_code = table_code, table_name = table_name, status = False)
            messages.info(request, table_name + " đã được thêm!")
    
    return redirect('create_table')

@login_required
def deleteTable(request):
    table_code = request.GET.get('table_code')
    try:
        print(table_code)
        tableItem = Table.objects.filter(table_code = table_code).first()
        if tableItem.status:
            messages.info(request, tableItem.table_name + ' đang được đặt!')
            messages.info(request, 'Không thể xóa ' + tableItem.table_name + '!')
            return redirect('view_table')
        else:
            tableItem.delete()
            messages.error(request, tableItem.table_name + ' đã được xóa!')
            user = User.objects.filter(username=table_code)
            user.delete()
            return redirect('view_table')
    except Exception as ex:
        print("error")
    return redirect('view_table')

@login_required
def addTable(request):
    data = {'title': 'Add Items to Table for my restaurant'}
    # Lấy dữ liệu từ form add table
    if request.method == "POST":
        print("Add")
        table_name = request.POST.get('name')
        table_code = request.GET.get('table_code')
        try:
            table_code_check = Table.objects.filter(table_name = table_name).first()
            if table_code_check.table_code == table_code:
                messages.info(request, table_name + " không thay đổi!")
            else:
                tableItem = Table.objects.filter(table_code = table_code).first()
                tableItem.table_code = "Ban_" + table_name.split(" ", 1)[1]
                tableItem.table_name = table_name
                tableItem.save()

                # user = User.objects.
                messages.info(request, )
        except Exception as ex:
            messages.info(request, 'updated price for item ')
            print(ex)
            return redirect('add_table')
        return redirect('view_table')

    # Tải dữ liệu từ form view table
    table_code = request.GET.get('table_code')
    if table_code:
        data['tableItems'] = Table.objects.filter(table_code=table_code).first()
    return render(request, 'partner/owner/add_table.html', processData(request, data))

@login_required
def restaurantDetails(request):
    data = {'title': 'My Restaurant Details'}
    if request.method == "POST":
        name = request.POST.get('name')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        country = request.POST.get('country', 'Vietnam')
        state = request.POST.get('state', '')
        zip = request.POST.get('zip', '')
        location = request.POST.get('location', '')
        tag = request.POST.get('tag', '')
        if not name:
            messages.error(request, 'cant save restaurant details')
            return redirect('restaurant_details')
        rest = Restaurant()
        try:
            rest = Restaurant.objects.create(user=request.user, name=name, address1=address1,
                                             address2=address2, country=country, state=state, zip=zip, location=location, tag=tag)
            messages.info(request, 'saved restaurant details')

        except IntegrityError:
            rest = Restaurant.objects.get(user=request.user)
            rest.name = name
            rest.address1 = address1
            rest.address2 = address2
            rest.country = country
            rest.state = state
            rest.zip = zip
            rest.location = location
            rest.tag = tag
            rest.save()
            messages.info(request, 'updated restaurant details.')
        except:
            messages.info(request, 'cant save restaurant details. try again')

        return redirect('restaurant_details')

    data['rest'] = Restaurant.objects.filter(
        user=request.user).order_by('id').first()
    data['countries'] = list(countries)
    return render(request, 'partner/owner/restaurant_details.html', processData(request, data))

@login_required
def viewDescribe(request):
    data = {'title': 'View describe for my restaurant'}
    name = request.GET.get('name')
    id_s = request.GET.get('id')
    
    item = MenuItem.objects.filter(name=name)
    data = {
        'info_item_id': item[0].id,
        'info_item_name': item[0].name,
        'info_item_price': str(item[0].price).split("000", 1)[0] + ",000 Đ",
        'info_item_image': item[0].image,
        'info_item_describe': item[0].describe,
    }
    return render(request, 'partner/owner/describe.html', processData(request, data))

@login_required
def viewMenu(request):
    data = {'title': 'View Menu for my restaurant'}
    data['menuItems'] = MenuItem.objects.filter(user=request.user)
    return render(request, 'partner/owner/view_menu.html', processData(request, data))



@login_required
def deleteMenu(request):
    data = {'title': 'Delete item from Menu'}

    if request.method == 'POST':
        confirmed = request.POST.get('confirm', 'no')
        id = request.POST.get('id')

        if not id:
            messages.error(request, 'please select item from menu to delete')
            return redirect('view_menu')

        if confirmed and confirmed.lower() == 'yes':
            try:
                itemToDelete = MenuItem.objects.filter(
                    user=request.user, id=id).first()
                itemToDelete.delete()
                messages.error(request, itemToDelete.name +
                               ' deleted from Menu')
                return redirect('view_menu')
            except Exception as e:
                print(e)
                messages.error(request, 'cant delete item with id' + str(id))
                return redirect('view_menu')

        else:
            messages.error(request, 'please click "yes" to confirm and delete')
            return redirect('view_menu')

    id = request.GET.get('id')

    if not id:
        messages.error(request, 'please select id to delete ')
        return redirect('view_menu')

    if MenuItem.objects.filter(user=request.user, id=id).count() != 1:
        messages.error(request, 'Cant find item from menu to delete')
        return redirect('view_menu')

    data['item'] = MenuItem.objects.filter(user=request.user, id=id).first()
    return render(request, 'partner/owner/confirm_delete_item.html', processData(request, data))


@login_required
def addMenu(request):
    data = {'title': 'Add Items to Menu for my restaurant'}
    if request.method == "POST":

        id = request.POST.get('id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        describe = request.POST.get('describe')

        if not (name and price):
            messages.error(request, 'please specify name of dish')
            return redirect('add_menu')

        try:
            if id:
                print('updating menu item')
                menuItem = MenuItem.objects.filter(
                    user=request.user, id=id).first()
                menuItem.price = price
                menuItem.name = name
                if image:
                    menuItem.image.save(image.name, image)
                menuItem.describe = describe
                menuItem.save()
                messages.info(request, 'updated price for item ' + name)
            else:
                menuItem = MenuItem.objects.create(
                    user=request.user, name=name, price=price, image=image, describe=describe)
                messages.info(request, 'crated new Menu item')

        except Exception as e:
            messages.error(request, 'an error occured try again')
            print(e)
            return redirect('add_menu')

        return redirect('view_menu')

    itemId = request.GET.get('id')
    if itemId:
        data['menuItem'] = MenuItem.objects.filter(id=itemId).first()

    return render(request, 'partner/owner/add_menu.html', processData(request, data))


@login_required
def revenue(request):
    data = {'title': 'Total revenue for my Restaurant'}

    ordersFromDb = Order.objects.all()
    list_date = []
    for order in ordersFromDb:
        str_date = str(order.date).split(" ", 1)[0]
        if str_date not in list_date:
            list_date.append(str_date)
    
    data = {
        'list_date':list_date
    }

    return render(request, 'partner/owner/revenue.html', processData(request, data))

@login_required
def revenueDate(request):
    data = {'title': 'Total revenue for my Restaurant'}

    if request.method == "POST":
        
        date = request.POST.get('date')
        data['date'] = date
        orders = Order.objects.filter(date__date=str(date))
        list_table = []
        total_venenue = 0
        for order in orders:
            if str(order.user.username) not in list_table:
                list_table.append(str(order.user.username))
            total_venenue += order.total_price
        print(list_table)

    
    data['all_table'] = list_table
    data['total_venenue'] = total_venenue
    return render(request, 'partner/owner/revenue_table.html', processData(request, data))

@login_required
def ownerHistory(request):
    data = {'title': 'Previous orders '}

    if request.method == "POST":
        messages.error(request, "cant save. please try again or conact admin")
        return redirect('order_history')
    data['all_table'] = Table.objects.all()

    # o = OrderedItem.objects.filter(item__user=request.user)
    # history = ()
    # for i in o:
    #     history.append(i)
    #     print(i.item)

    # data['history'] = history

    # print(history)
    return render(request, 'partner/owner/view_table_order.html', processData(request, data))

@login_required
def ownerHistoryTable(request):
    data = {'title': 'Previous orders '}
    table_code = request.GET.get('table_code')
    print(table_code)

    user = User.objects.get(username = table_code)
    print(user)
    try:
        ordersFromDb = Order.objects.filter(user=user).order_by('-id')
        print(ordersFromDb[0].id)
    except Exception as ex:
        print(ex)
    print(ordersFromDb)
    newOrders = []
    for order in ordersFromDb:
        tmp_order = {}
        tmp_order['id'] = order.id
        tmp_order['delivered'] = order.delivered
        tmp_order['rider'] = order.rider
        tmp_order['dateTime'] = order.date
        tmp_order['total'] = order.total_price
        tmp_order['items'] = OrderedItem.objects.filter(
            order=order).order_by('-id')
        newOrders.append(tmp_order)

    print(newOrders)

    data['orders'] = newOrders
    data['name_table'] = order.user.username
    return render(request, 'partner/owner/owner_history_details.html', processData(request, data))