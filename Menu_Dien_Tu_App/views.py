from django.shortcuts import render
# from sqlserverconnect.models import sqlserverconn
import pyodbc
# Create your views here.
def index(request):
    connect = pyodbc.connect('Driver={sql server};'
                            'Server=DESKTOP-AJ7H4HH\MSSQLSERVER2019;'
                            'Database=Menu_PhucVuThucUong;'
                            'Trusted_Connection=yes;')
    cursor=connect.cursor()
    cursor.execute("SELECT * FROM Drinks")
    drinks=cursor.fetchall()

    cursor.execute("SELECT * FROM Toppings")
    toppings=cursor.fetchall()

    print(drinks)
    context = {
        'title':"Hệ thống menu điện tử",
        'drinks':drinks,
        'toppings':toppings
    }
    return render(request, 'index.html', context=context)