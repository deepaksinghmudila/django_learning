import math
import json
from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Contact, Order, OrderUpdate

from django.template import RequestContext

# Create your views here.
def index(request):
    # print(Product.product_name)
    # for name in Product.product_name:
    #     print(name)
    # products = Product.objects.all()
    # for p in Product.objects.all():
    #     # print(p.product_id)
    #     print(p.product_name)
    #     print(p.category)
    #     print(p.subcategory)
    #     print(p.price)
    #     print(p.desc)
    #     print(p.pub_date)
    #     print("\n")

    # context = {
    #     'product': product,
    #     'n': range(3)
    # }
    # print(products)
    # n = len(products)
    # nSlides = n//4 + math.ceil((n/4) - (n//4))
    # params = {'product': products,'no_of_slides': nSlides,'range': range(nSlides)}
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats=  {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1,nSlides), nSlides])
     
    params = {'allProds': allProds}
    print('allProds:', params);
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):     
    
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        alert = True
        return render(request, 'shop/contact.html', {'alert': alert, 'id': id})
    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        # return HttpResponse(f"{orderId} and {email}")
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')         
    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):    
    product = Product.objects.filter(id=myid)     
    return render(request, 'shop/prodView.html', {'product': product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)        
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        thank=  True
        id = order.order_id         
        # print('Order_id:', id)
        # order.save()
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
