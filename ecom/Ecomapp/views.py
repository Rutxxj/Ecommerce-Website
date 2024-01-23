import random
from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Cart,Order
from django.db.models import Q
from . forms import CreateUserForm,Addproduct
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import razorpay



# Create your views here.
def index(req):
    data= Product.objects.all()
    context ={'data':data}
    return render(req,"index.html",context)

def details(req,pid):
    products= Product.objects.get(id=pid)
    context = {'products': products}
    return render(req,"details.html",context)

def cart(req):
    if req.user.is_authenticated:
        allproducts = Cart.objects.filter(user = req.user)
    else:
        return redirect("/login")
    context={}
    context['cart_items']= allproducts
    total_price=0
    for x in allproducts:
            total_price += (x.product.price * x.quantity)
            print(total_price)
    context['total'] = total_price
    length = len(allproducts)
    context['items']= length
    return render(req,"cart.html",context)

def add_cart(req,pid):
    products= Product.objects.get(id=pid)
    user = req.user if req.user.is_authenticated else None
    print(products)
    if user:
        cart_item,created=Cart.objects.get_or_create(product=products,user=user)
        print(cart_item,created)
    else:
        return redirect("/login")
        #cart_item,created=Cart.objects.get_or_create(product=products , user= None)
    
    if not created:
            cart_item.quantity +=1
    else:
            cart_item.quantity =1
    cart_item.save()
    return redirect("/cart")

def delete(req,pid):
    #print("ID to be deleted",pid)
    #return HttpResponse("ID to be deleted" + rid)
    m= Cart.objects.filter(id=pid)
    m.delete()
    return redirect("/cart")

def search(req):
    query = req.POST['q']
    #print(f"recieved Query is {query}")
    if not query:
        result = Product.objects.all()
    else:
        result = Product.objects.filter(
            Q(name__icontains = query)|
            Q(category__icontains = query)|
            Q(price__icontains = query)
        )
    return render(req,'index.html',{'results':result,'query':query})

def range(req):
    if req.method == "GET":
        return redirect("/")
    else:
        r1 = req.POST.get("min")
        r2 = req.POST.get("max")
        #print(r1,r2)
        if r1 is not None and r2 is not None and r1 !="" and r2 !="":
            queryset = Product.prod.get_price_range(r1,r2)
            context={'data':queryset}
            return render(req,'index.html',context)
        else:
            queryset = Product.objects.all()
            context = {'data': queryset}
            return render (req,"index.html",context)

def watchList(req):
    queryset=Product.prod.watch_list()
    context={'data':queryset}
    return render(req,"index.html",context)  

def mobileList(req):
    queryset=Product.prod.mobile_list()
    context={'data':queryset}
    return render(req,"index.html",context) 

def sort(req):
    queryset = Product.objects.all().order_by("price")
    context={'data':queryset}

    return render(req,"index.html",context)

def HightoLow(req):
    queryset = Product.prod.price_order()
    context={'data':queryset}
    return render(req,"index.html",context) 

def updateqty(req,uval,pid):
    products= Product.objects.get(id=pid)
    user= req.user
    c = Cart.objects.filter(product=products,user=user)
    print(c)
    print(c[0])
    print(c[0].quantity)
    if uval == 1:
        a=c[0].quantity + 1
        c.update(quantity = a)
    else:
        a=c[0].quantity - 1
        c.update(quantity = a)  
    #return HttpResponse(f"uval:{uval},pid {pid}")                                                                                                                     
    return redirect("/cart")


def register_user(req):
    form = CreateUserForm()
    if req.method == "POST":
        form =CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,("User Created successfully"))
            return redirect("/login")
        else:
            messages.error(req,"Incorrect Password Format")
    context = {'form': form}
    return render(req,"register.html",context)


def login_user(req):
    if req.method== "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user)
            
            messages.success(req,("Login Successfully"))
        
            return redirect("/")
        else:
            
            messages.error(req,("error try again"))
            
            return redirect("/login")
    else:
        return render(req,"login.html")

def logout_user(req):
    logout(req)
    messages.success(req,("You have logged Out Successfully"))
    return redirect("/login")
    
def viewOrder(req):
    c = Cart.objects.filter(user= req.user)
    
    context={}
    context['cart_items']= c
    total_price=0
    for x in c:
            total_price += (x.product.price * x.quantity)
            print(total_price)
    context['total'] = total_price
    length = len(c)
    context['items']= length
    return render(req,"order.html",context)

def makePayment(req):
    c = Cart.objects.filter(user= req.user)
    oid = random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id = oid,product_id = x.product.id,user=req.user,quantity=x.quantity)
    orders= Order.objects.filter(user=req.user,is_completed=False)
    total_price=0
    for x in orders:
            total_price += (x.product.price * x.quantity)
            oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_s3994C5Pbog19d", "pEu8AOe0eI61PrpoQXnNWT3I"))
    data={
    "amount": total_price * 100,
    "currency": "INR",
    "receipt": "oid",
    }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    context['amount']=payment['amount']
    
    c.delete()
    orders.update(is_completed=True)
    return render(req,"payment.html",context)


def insertproducts(req):
    if req.user.is_authenticated:
        user=req.user
        if req.method == "GET":
            form = Addproduct()
            return render(req,"insertProd.html",{'form':form})
        else:
            form=Addproduct(req.POST,req.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(req,("Product entered"))
                return redirect("/")
            else:
                messages.error(req,"Incorrect data")
                return render(req,"insertProd.html",{'form':form})
    else:
        return redirect("/login")