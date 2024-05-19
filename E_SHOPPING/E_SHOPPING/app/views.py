from django.shortcuts import render
from app.models import User,Product
from userapp import views
from django.shortcuts import redirect, render,get_object_or_404,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.forms import ProductRegistration,UserRegistrationForm, UserLoginForm
from django.views.decorators.cache import cache_page
# Create your views here.



def loginFunction(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    request.session['username'] = user.email
                    request.session['user_id'] = user.id
                    request.session['is_superuser'] = True
                    return redirect('home:productlist')
                else:
                    request.session['username'] = user.email
                    request.session['user_id'] = user.id
                    request.session['is_superuser'] = False
                    return redirect('landing')
            else:
                messages.warning(request, 'Please verify credentials you entered!')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def Reg(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            return redirect('home:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
    
@cache_page(60*1)
def Productlist(request):
    product = Product.objects.filter(status=False)
    print("product",product)
    context = {
            'product':product,
        }
    return render(request,'electronics.html',context)

def logoutView(request):
    logout(request)
    return redirect('home:login')

def addproduct(request):
    form = ProductRegistration()
    return render(request,'addproduct.html',{'forms':form})

def Saveproduct(request):
        if request.method == 'POST':
            form = ProductRegistration(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home:productlist')
            else:
               return render(request,'addproduct.html',{'forms':form})
        else:
            form = ProductRegistration()
            return render(request,'addproduct.html',{'forms':form})
        
@login_required
def Editproduct(request, id):
    context ={}
    obj = get_object_or_404(Product, id = id)
    if request.method == 'POST':
        form = ProductRegistration(request.POST , request.FILES , instance = obj)
        if form.is_valid():
            form.save()
            return redirect('home:productlist')
    else:
        form = ProductRegistration(instance=obj)
    context["form"] = form
    return render(request,'product_edit.html',context)

def DeleteProduct(request,id):
    Product.objects.filter(id=id).update(status=True)
    return redirect('home:productlist')

def updated(request):
    return render(request,'updatedlist.html')

