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
        return redirect('category/' + query)
    response1 = requests.get('https://dummyjson.com/products/category-list')
    data1 = response1.json()
    response2 = requests.get('https://dummyjson.com/products?limit=8&skip=20')
    
    if response2.status_code == 200:
        data2 = response2.json().get('products', []) 
    else:
        data2 = []

    processed_data = []
    
    for product in data2:
        product_price = product['price'] 
        discount_percentage = product.get('discountPercentage', 0)

        total_price = product_price * (1 - discount_percentage / 100)
        product['total_price'] = total_price
        
        processed_data.append(product)

    return render(request, 'index.html', context={"categoryList": data1, "categoryProduct": processed_data})

def cart(request):
    userId = request.session.get('currentUser')
    if userId:
        user = UserTable.objects.get(id=userId)
    else:
        print("Please Login")

    cart_data = user.cart or '[]'
    try:
        cartList = json.loads(cart_data)
    except json.JSONDecodeError:
        return render(request, 'cart.html', context={'error': 'Invalid cart data.'})

    data = []
    subtotal = 0
    shipping_charge = 10

    for item in cartList:
        product_id, quantity = item  
        resp = requests.get(f'https://dummyjson.com/products/{product_id}')
        
        if resp.status_code == 200:
            product_data = resp.json()
            product_price = product_data['price']
            discount_percentage = product_data.get('discountPercentage', 0)
            discountedPrice = product_price * (1 - discount_percentage / 100)

            total_price = discountedPrice * quantity
            product_data['quantity'] = quantity
            product_data['total_price'] = total_price
            product_data['discountedprice'] = discountedPrice

            data.append(product_data)
            subtotal += total_price
        else:
            print(f"Error fetching product {product_id}: {resp.status_code}")

    if subtotal >= 10:
        sum = subtotal + shipping_charge
    else:
        sum = subtotal

    return render(request, 'cart.html', context={'cartList': data, 'subtotal': subtotal, 'sum': sum, 'shipping_charge': shipping_charge})

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
    userId = request.session.get('currentUser')
    user = UserTable.objects.get(id=userId)

    cart_data = user.cart or '[]'  
    try:
        cartList = json.loads(cart_data)
    except json.JSONDecodeError:
        return render(request, 'checkout.html', context={'error': 'Invalid cart data.'})

    data = []
    subtotal = 0
    shipping_charge = 10  

    for item in cartList:
        product_id, quantity = item  
        resp = requests.get(f'https://dummyjson.com/products/{product_id}')
        
        if resp.status_code == 200:
            product_data = resp.json()
            product_price = product_data['price']
            discount_percentage = product_data.get('discountPercentage', 0)
            discountedPrice = product_price * (1 - discount_percentage / 100)

            total_price = discountedPrice * quantity 
            product_data['quantity'] = quantity
            product_data['total_price'] = total_price 
            product_data['discountedprice'] = discountedPrice

            data.append(product_data)
            subtotal += total_price  
        else:
            print(f"Error fetching product {product_id}: {resp.status_code}")

    if subtotal >= 10:
        sum = subtotal + shipping_charge 
    else:
        sum = subtotal 

    return render(request, 'checkout.html', context={'cartList': data, 'subtotal': subtotal, 'sum': sum, 'shipping_charge': shipping_charge})

def details(request,id):
    resp = requests.get('https://dummyjson.com/products/'+str(id))
    if resp.status_code == 200:
            product_data = resp.json()
            product_price = product_data['price']  
            discount_percentage = product_data.get('discountPercentage',0)
            discountedPrice = product_price * (1 - discount_percentage/ 100 )
            print(discountedPrice)
            product_data['discountedprice'] = discountedPrice
    return render(request, 'detail.html',context={'cartList':product_data})

def shop(request):
    response = requests.get('https://dummyjson.com/products?limit=12')
    
    if response.status_code == 200:
        data = response.json().get('products', [])
    else:
        data = []
    
    processed_data = []
    
    for product in data:
        product_price = product['price'] 
        discount_percentage = product['discountPercentage'] 
        
        total_price = (product_price * (1 - discount_percentage / 100))
        product['total_price'] = total_price
        
        processed_data.append(product)
    
    return render(request, 'shop.html', context={"categoryProduct": processed_data})

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
    if response.status_code == 200:
        data = response.json().get('products', []) 
    else:
        data = []

    processed_data = []
    for product in data:
        product_price = product['price'] 
        discount_percentage = product.get('discountPercentage', 0)
        

        total_price = product_price * (1 - discount_percentage / 100)
        product['total_price'] = total_price
        
        processed_data.append(product)

    return render(req,'category.html',context={"categoryProduct":processed_data})

def search(req):
    response = requests.get('https://dummyjson.com/products/search?q=phone/')
    data = response.json()

    return render(req,'category.html',context={"categoryProduct":data})

def addToCart(req, id):
    userId = req.session.get('currentUser')
    user = UserTable.objects.get(id=userId)

    cart_data = user.cart or '[]'
    try:
        cartList = json.loads(cart_data)
    except json.JSONDecodeError:
        cartList = []

    found = False
    for i, (product_id, quantity) in enumerate(cartList):
        if product_id == id:
            cartList[i] = (product_id, quantity + 1)
            found = True
            break

    if not found:
        cartList.append((id, 1))

    user.cart = json.dumps(cartList)
    user.save()

    return redirect('/cart')

def remove_from_cart(req, id):
    userId = req.session.__getitem__('currentUser')
    user = UserTable.objects.get(id=userId)
    cartList = json.loads(user.cart)

    cartList = [item for item in cartList if item[0] != id]

    user.cart = str(cartList)
    user.save()
    return redirect('/cart')
    # cartList = [item for item in cartList if item['id'] != id]
    # request.session['cartList'] = cartList
    # return redirect(reverse('cartList'))

def Add_New_Product(req, product):

    userId = req.session.get('currentUser')  
    user = UserTable.objects.get(id=userId) 

    cartList = json.loads(user.cart) 
    cartList.append(product)
    user.cart = json.dumps(cartList)
    user.save()

    response = requests.post('https://dummyjson.com/products/add', 
                         headers={'Content-Type': 'application/json'}, 
                         data=json.dumps({
                            'title': 'iPad Mini 2021 Starlight',    
                            'discountPercentage': '₹19.48',
                         }))

    print(response.json())

    product = {
        'title': 'iPad Mini 2021 Starlight',
        'discountPercentage': '₹19.48',
    }
    Add_New_Product(product)
    return redirect('/cart')

def changeQty(req):
    userId = req.session.get('currentUser')
    user = UserTable.objects.get(id=userId)

    cart_data = user.cart or '[]' 
    try:
        cartList = json.loads(cart_data)
    except json.JSONDecodeError:
        cartList = []

    product_id = req.GET.get('product_id')
    quantity = req.GET.get('qty')

    product_id = int(product_id)
    quantity = int(quantity)

    print("AAA", product_id, quantity)

    for i, item in enumerate(cartList):
        p_id, q = item 
        if p_id == product_id:
            q += quantity 
            if q < 0:  
                q = 0
            cartList[i] = (p_id, q)
            break

    user.cart = json.dumps(cartList)
    user.save()
    
    return redirect('/cart')

def Wishlist(req):
    userId = req.session.get('currentUser')
    user = UserTable.objects.get(id=userId)

    cart_data = user.cart or '[]'
    try:
        cartList = json.loads(cart_data)
    except json.JSONDecodeError:
        return render(req, 'wishList.html', context={'error': 'Invalid data.'})

    data = []
    subtotal = 0

    for item in cartList:
        product_id, quantity = item  
        resp = requests.get(f'https://dummyjson.com/products/{product_id}')
        
        if resp.status_code == 200:
            product_data = resp.json()
            product_price = product_data['price']
            discount_percentage = product_data.get('discountPercentage', 0)
            discountedPrice = product_price * (1 - discount_percentage / 100)

            total_price = discountedPrice * quantity
            product_data['quantity'] = quantity
            product_data['total_price'] = total_price
            product_data['discountedprice'] = discountedPrice

            data.append(product_data)
            subtotal += total_price
        else:
            print(f"Error fetching product {product_id}: {resp.status_code}")
    return render(req, 'wishList.html', context={'cartList': data})

def addToWishList(req,id):
    userId = req.session.get('currentUser')
    user = UserTable.objects.get(id=userId)

    cart_data = user.cart or '[]'
    try:
        cartList = json.loads(cart_data)
    except json.JSONDecodeError:
        cartList = []

    found = False
    for i, (product_id, quantity) in enumerate(cartList):
        if product_id == id:
            cartList[i] = (product_id, quantity + 1)
            found = True
            break

    if not found:
        cartList.append((id, 1))

    user.cart = json.dumps(cartList)
    user.save()

    return redirect('/wishList/')