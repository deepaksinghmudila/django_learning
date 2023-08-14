import math
import json
from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Contact, Order, OrderUpdate

from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt

from PayTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

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

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request): 
    query = request.GET.get('search')   
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats=  {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
        if len(prod)!=0:
            allProds.append([prod, range(1,nSlides), nSlides])
     
    params = {'allProds': allProds, 'msg': ""}
    if len(allProds) == 0 or len(query)<4:
        params =  {'msg': 'Please make sure to enter relevent search query'}
    # print('allProds:', params);     
    return render(request, 'shop/search.html', params)


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
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitem"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')         
    return render(request, 'shop/tracker.html')


def productView(request, myid):    
    product = Product.objects.filter(id=myid)     
    return render(request, 'shop/prodView.html', {'product': product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, amount=amount, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)        
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        thank=  True
        id = order.order_id         
        # print('Order_id:', id)
        # order.save()
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        #request paytm to transfer the amount to your account after payment by user
        param_dict = {
                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,  #'acfff@paytm.com',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/'
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    #paytm will send you POST request here    
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)        
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Order Successfull')    
        else:
            print('Order was not successfull because' + response_dict['RESPMSG'])
            
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
