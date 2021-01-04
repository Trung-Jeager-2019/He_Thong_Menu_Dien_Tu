from django.shortcuts import render, redirect
from Menu_Dien_Tu.utils import processData, toId, getRole
from Menu_Dien_Tu_App.cart import addItemToCart
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from Menu_Dien_Tu_App.models import Restaurant, MenuItem, Profile, Table, Category, Order, OrderedItem

# Create your views here

def index(request):
    data = {
        'title': 'Hệ thống e-menu'
    }
    items = Table.objects.all()
    if items and items.count() > 0:
        data['tableItems'] = items
    return render(request, 'user/select.html', processData(request, data))

def select(request):
    data = {
        'title': 'Đăng nhập'
    }
    table_code = request.GET.get('table_code')

    try:
        username = table_code
        password = "Trung14121999#"

        status = Table.objects.get(table_code=table_code)
        status.status = True
        status.save()

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                nextUrl = request.POST.get('next')
                print(nextUrl)
                if not nextUrl:
                    nextUrl = 'home'
            return redirect(nextUrl)
    except Exception as ex:
        print(ex)
        messages.error(request, "Xảy ra lỗi! Vui lòng liên hệ cửa hàng!")
    return redirect('index')

def home(request):
    data = {
        'title': 'Hệ thống e-menu',
    }
    
    data['slideBar'] = Category.objects.all()
    categoryFromDb = Category.objects.all()
    
    newCategory = []
    for category in categoryFromDb:
        tmp_category = {}
        tmp_category['categoryCode'] = category.category_code
        tmp_category['categoryName'] = category.category_name
        tmp_category['categoryItems'] = MenuItem.objects.filter(category=category.category_code)
        newCategory.append(tmp_category)

    data['category'] = newCategory
    return render(request, 'index.html', processData(request, data))

def logoutUser(request):
    check_User = str(request.user)
    if request.user.is_authenticated:
        try:
            status = Table.objects.get(table_code=check_User)
            status.status = False
            status.save()
            auth.logout(request)
            messages.info(request, 'Bạn đã trả bàn!')
        except Exception as ex:
            auth.logout(request)
            messages.info(request, 'Đã đăng xuất tài khoản!')
    return redirect('index')


def loginUser(request):
    data = {
        'title': 'Đăng nhập'
    }
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            messages.error(request, 'Hãy nhập đầy đủ thông tin tài khoản!')
            return redirect('login')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                nextUrl = request.POST.get('next')
                print(nextUrl)
                if not nextUrl:
                    nextUrl = 'dashboard'

                return redirect(nextUrl)

        messages.error(request, 'Đăng nhập thành công!')
        return redirect('login')

    else:
        # check account type, 3 types normal, rider and restaurent owner

        data['role'] = getRole(request)
        return render(request, 'login.html', processData(request, data))


def signup(request):
    data = {
        'title': 'Tạo tài khoản'
    }
    
    if(request.method == 'POST'):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not(first_name and last_name and username and email and password1 and password2):
            messages.info(request, 'All fields are mandatory')
            return redirect('signup')

        if password1 != password2:
            messages.info(request, 'Passwords not matching')
            return redirect('signup')

        else:
            if User.objects.filter(username=username).exists():
                messages.info(
                    request, 'Username already taken. Please select another Username.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(
                    request, 'Email already registered. Please login to continue.')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                user.profile.role = getRole(request)
                user.save()

                print('User created')
                messages.info(
                    request, 'Account created successfully. Please login to continue.')
        return redirect('login')
    else:
        # check account type, 3 types normal, rider and restaurent owner
        role = request.GET.get('type', 'normal').lower()

        if role != 'rider' and role != 'owner':
            role = 'normal'

        data['role'] = role
        return render(request, 'signup.html', processData(request, data))


def aboutTeams(request):
    data = {
        'title': 'Thông tin về nhóm!'
    }
    return render(request, 'teams.html', processData(request, data))


def specials(request):
    data = {
        'title': 'Special deals'
    }
    return render(request, 'specials.html', processData(request, data))


def offers(request):
    data = {
        'title': 'New offers'
    }
    return render(request, 'offers.html', processData(request, data))


def support(request):
    data = {
        'title': 'Customer support page'
    }
    return render(request, 'support.html', processData(request, data))


def cart(request):
    data = {
        'title': 'Đơn đặt'
    }
    return render(request, 'cart.html', processData(request, data))

@login_required
def addToCart(request):
    id = request.GET.get('id', None)

    if id:
        try:
            items = request.session.get('items', [])
            itemToAdd = MenuItem.objects.filter(active=True, id=id)

            if itemToAdd and itemToAdd.values() and itemToAdd.values()[0]:
                items = addItemToCart(items, itemToAdd.values()[0])
                request.session['items'] = items
                newItem = itemToAdd.values()[0]
                messages.error(
                    request, newItem['name'] + " đã được thêm vào đơn!")

            else:
                messages.error(request, "Không tìm thấy sản phẩm.")

        except Exception as e:
            print(e)
            messages.error(request, "Đã xảy ra lỗi. Vui lòng thử lại!")
    else:
        messages.error(request, "Hãy chọn sản phẩm và thêm vào đơn.")

    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required
def removeFromCart(request):
    data = {
        'title': 'Xóa sản phẩm'
    }
    id = toId(request.GET.get('id', -1))
    if not id:
        messages.error(request, 'Hãy chọn sản phẩm cần xóa.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    items = request.session.get('items', [])
    itemToRemove = None

    for item in items:
        if item["id"] == id:
            itemToRemove = item
            break

    if not itemToRemove:
        messages.info(request, "Không thể tìm thấy sản phẩm trong đơn.")

    else:
        newItems = [i for i in items if not (i['id'] == itemToRemove["id"])]
        request.session['items'] = newItems
        messages.info(request, itemToRemove["name"] + ' đã được bỏ chọn khỏi đơn!')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def profile(request):
    data = {
        'title': 'Thông tin'
    }
    return render(request, 'user/profile.html', processData(request, data))


@login_required
def dashboard(request):
    data = {
        'title': 'Trang chủ'
    }
    return render(request, 'user/profile.html', processData(request, data))


def partnerWithUs(request):
    data = {
        'title': 'Partner with us'
    }
    return render(request, 'partner/select.html', processData(request, data))

