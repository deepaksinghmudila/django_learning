from django.shortcuts import render
from django.http import HttpResponse
# from .models import Product, Contact, Order
import math

from django.template import RequestContext

# Create your views here.
def index(request):          
    return render(request, 'index.html')