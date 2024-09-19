from django.shortcuts import render,redirect
from .models import users as UserTable
from django.core.mail import send_mail
from django.contrib import messages
import requests
import json
from django.urls import reverse


def index(request):
    if request.method == "POST":
        query = request.POST['Searchquery']
        return redirect('category/'+query)
        
    response1 = requests.get('https://dummyjson.com/products/category-list')
    data1 = response1.json()
    response2 = requests.get('https://dummyjson.com/products?limit=8&skip=20')
    data2 = response2.json()
    return render(request, 'index.html',context={"categoryList":data1,"categoryProduct":data2})

def cart(request):
    userId = request.session.__getitem__('currentUser')
    user = UserTable.objects.get(id = userId)
    cartList = json.loads(user.cart)
    data = []
    subtotal = 0
    sum = 10 
    for item in cartList:
        resp = requests.get('https://dummyjson.com/products/'+str(item))
        data.append(resp.json())
    for i in data:
        sum+=i['discountPercentage']
        subtotal+=i['discountPercentage']
    return render(request, 'cart.html',context={'cartList':data,"total":sum,"subtotal":subtotal})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email_subject = f"New Contact Form Submission: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        send_mail(email_subject, email_message, 'vaibhavgohil305@gmail.com', ['gohilvaibhav31@gmail.com'])
        messages.success(request, 'Thank you for your message. We will get back to you shortly.')
    return render(request, 'contact.html')

def checkout(request):
    userId = request.session.__getitem__('currentUser')
    user = UserTable.objects.get(id = userId)
    cartList = json.loads(user.cart)
    data = []
    subtotal = 0
    sum = 10 
    for item in cartList:
        resp = requests.get('https://dummyjson.com/products/'+str(item))
        data.append(resp.json())
    for i in data:
        sum+=i['discountPercentage']
        subtotal+=i['discountPercentage']
    return render(request, 'checkout.html',context={'cartList':data,"total":sum,"subtotal":subtotal})

def details(request,id):
    resp = requests.get('https://dummyjson.com/products/'+str(id))
    return render(request, 'detail.html',context={'cartList':resp.json()})

def shop(request):
    response = requests.get('https://dummyjson.com/products?limit=12')
    data = response.json()
    return render(request, 'shop.html',context={"categoryProduct":data})

def members(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['pwd']
        if uname.find('@') >= 0:
            s = UserTable.objects.get(email = uname,password = pwd)
        else:
            s = UserTable.objects.get(firstname = uname,password = pwd)
        if s :
            request.session['currentUser'] = s.id
            print(request.session['currentUser'])
            return redirect('/')
    return render(request, 'index1.html')

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pwd = request.POST['pwd']
        print(fname,lname,email,pwd)
        s = UserTable.objects.create(
            firstname=fname,
            lastname=lname,
            email=email,
            password=pwd
        )
        s.save()
        print("saved")
        return redirect('/members')
    return render(request, 'registration.html')

def password(req):
    return render(req, 'pass-reset.html')

def homepage(req,id):
    s = UserTable.objects.get(id = id)
    return render(req,'main.html',context={"data":s})

def categoryPage(req,category):
    # print(category)
    response = requests.get('https://dummyjson.com/products/category/'+category)
    data = response.json()

    return render(req,'category.html',context={"categoryProduct":data})

def search(req):
    response = requests.get('https://dummyjson.com/products/search?q=phone/')
    data = response.json()

    return render(req,'category.html',context={"categoryProduct":data})

def addToCart(req,id):
    userId = req.session.__getitem__('currentUser')
    user = UserTable.objects.get(id = userId)
    cartList = json.loads(user.cart)
    print("cartlist ",cartList)
    cartList.append(id)
    user.cart = str(cartList)
    user.save() 

    return redirect('/cart')

def remove_from_cart(req,id):
    userId = req.session.__getitem__('currentUser')
    user = UserTable.objects.get(id = userId)
    cartList = json.loads(user.cart)
    cartList.remove(id) 
    user.cart = str(cartList)
    user.save()
    return redirect('/cart')
    # cartList = [item for item in cartList if item['id'] != id]
    # request.session['cartList'] = cartList
    # return redirect(reverse('cartList'))

# def Add_New_Product(req, product):

    userId = req.session.get('currentUser')  
    user = UserTable.objects.get(id=userId) 

    # Load the user's cart and add the new product
    cartList = json.loads(user.cart) 
    cartList.append(product)
    user.cart = json.dumps(cartList)
    user.save()

    # Send a POST request to the external API to add the product
    response = requests.post('https://dummyjson.com/products/add', 
                         headers={'Content-Type': 'application/json'}, 
                         data=json.dumps({
                            'title': 'iPad Mini 2021 Starlight',    
                            'discountPercentage': '₹19.48',
                         }))

    print(response.json())
    # Redirect to the cart page
    return redirect('/cart')

# Example usage (this would typically be called in a view)
    product = {
        'title': 'iPad Mini 2021 Starlight',
        'discountPercentage': '₹19.48',
    }
    Add_New_Product(product)

