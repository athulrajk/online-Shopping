from django.shortcuts import render
import json 
from app.models import Product,User,Cart,Order
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Sum

# Create your views here.

def landing(request):
    if request.session:
       
        products_first_ten =Product.objects.filter(status=False)
        context = {
            'products_first_ten' : products_first_ten,
        }
        return render(request,'index.html',context)
   

def singlepage(request,id):
    product_single = Product.objects.get(id=id,status=False)
    context = {
        'product_single' : product_single,
    }
    return render(request,'single.html',context)


@csrf_exempt
def add_cart(request):
  
    data_set={}
    try:
        userId = request.POST['user_id']
        productId = request.POST['product_id']
        quantity = request.POST['quantity']
        price = request.POST['price']
        total_price = int(quantity)*float(price)
        obj,cart = Cart.objects.update_or_create(user_id=User.objects.get(id=userId),
                                    product_id=Product.objects.get(id=productId),
                                    product_count=int(quantity),tottal_price=total_price,status=True)
        cart_count = Cart.objects.filter(user_id=User.objects.get(id=userId)).count()
        data_set['cart_count']=cart_count
        data_set['status']= True
    except Exception as e:
        print("EX::::",e)
        data_set['cart_count']=0
        data_set['status']= False
      
    return HttpResponse(json.dumps(data_set), content_type="application/json")


def checkout(request,user_id):
    orders = Cart.objects.filter(status =True ,user_id = User.objects.get(id=user_id))
    print('orders',orders)
    product_total_amount = Cart.objects.filter(user_id = User.objects.get(id=user_id),status=True).aggregate(total_price=Sum('tottal_price'))
    print(product_total_amount)
    if product_total_amount['total_price'] == None:
        total_amount = 0
    else:
        total_amount = product_total_amount['total_price']
    
    context={
        'orders':orders,
        'total_amount':total_amount,
        'user_id':user_id
    }
   
    return render(request,'checkout.html',context)

@csrf_exempt    
def placeorder(request):
    userid =request.POST['user_id']
    total_amount =request.POST['total_amount']
    obj,order = Order.objects.update_or_create(user_id=User.objects.get(id=userid),is_paid = True,order_status = True,total_amount=total_amount)
    data_set={
        'status':True
    }
    return HttpResponse(json.dumps(data_set),content_type="application/json") 

def invoice(request,userid):
    order = Order.objects.filter(user_id=User.objects.get(id=userid),is_paid = True,order_status = True).first()
    cart=Cart.objects.filter(user_id=User.objects.get(id=userid),status=True)
    invoice_id ="ORD"+str(userid)
    context = {
        'order':order,
        'cart' :cart,
        'user_id':userid,
        'invoice_id':invoice_id
    }
    return render(request,'invoice.html',context)
    


