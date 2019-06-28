from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import *
import bcrypt
import datetime

def admin_page(request):
    if not 'user_id' in request.session or request.session['user_id'] != 3:
        return redirect('/')
    context = {
        'all_users': User.objects.all(),
        'all_products': Product.objects.all().order_by('category', '-id')
    }
    return render(request, 'store/admin.html', context)

def index(request):
    context = {
        'latest_products': Product.objects.filter(created_at__gte=datetime.date(2019, 5, 30),created_at__lte=datetime.date(2019, 6, 30)).order_by('-created_at'),
        'top_products': Product.objects.filter(sub_category = 'Driver', brand = "Taylormade" )
    }
    return render(request, 'store/index.html', context)

def product_page(request, product_id):
    product = Product.objects.get(id = product_id) 
    context = {
        'product': product,
        'related_products': Product.objects.filter(sub_category = product.sub_category),
    }
    return render(request, 'store/product.html', context)

def category_page(request):
    context = {
        'all_products': Product.objects.all().order_by('name'),
    }
    return render(request, 'store/category.html', context)

def cart_page(request):
    user = User.objects.get(id = request.session['user_id'])
    order = Order.objects.filter(user = user)
    if len(order) == 0:
        order = Order.objects.create(user = user)
        cart = Order.objects.get(user = user).products.values()
    else: 
        cart = Order.objects.get(user = user).products.values()
    total_price = 0
    print(cart)
    for product in cart:
        total_price += product['price']
    context = {
        'cart': cart,
        'total_price': total_price,
    }
    print(total_price)
    return render(request, 'store/cart.html', context)

def checkout_page(request):
    user = User.objects.get(id = request.session['user_id'])
    order = Order.objects.filter(user = user)
    if len(order) == 0:
        order = Order.objects.create(user = user)
        cart = Order.objects.get(user = user).products.values()
    else: 
        cart = Order.objects.get(user = user).products.values()
    total_price = 0
    print(cart)
    for product in cart:
        total_price += product['price']
    context = {
        'cart': cart,
        'total_price': total_price,
        'total_price100' : total_price *100,
    }
    print(total_price)
    return render(request, 'store/checkout.html', context)

def checkout(request):
    Checkout.objects.create(email = request.POST['stripeEmail'], token = request.POST['stripeToken'])
    user = User.objects.get(id = request.session['user_id'])
    cart = Order.objects.get(user = user)
    print(cart)
    cart.delete()    
    return redirect("/checkout_page")

def contact_page(request):
    return render(request, 'store/contact.html')

def login_register_page(request):
    return render(request, 'store/login_register.html')

def register_user(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/login_register_page')
    hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashpw)
    request.session['logged_in'] = True
    request.session['user_id'] = user.id
    return redirect('/')

def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/login_register_page')
    user = User.objects.filter(email = request.POST['email'])
    request.session['logged_in'] = True
    request.session['user_id'] = user[0].id
    if user[0].id == 3:
        return redirect('/admin_page')
    return redirect('/')

def add_to_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    user = User.objects.get(id = request.session['user_id'])
    order = Order.objects.filter(user = user)
    if len(order) == 0:
        order = Order.objects.create(user = user)
        order.products.add(product)
    else:
        order[0].products.add(product)
    return redirect('/cart_page')

def log_out(request):
    del request.session['user_id']
    del request.session['logged_in']
    return redirect('/login_register_page')

# Admin Page

def add_product(request):
    errors = Product.objects.product_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/admin_page')
    uploaded_file = request.FILES['photo']
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name, uploaded_file)
    url = fs.url(name)
    product = Product.objects.create(name = request.POST['name'], price = request.POST['price'], description = request.POST['description'],category = request.POST['category'], sub_category = request.POST['sub_category'], brand = request.POST['brand'], availability = request.POST['availability'] )
    Image.objects.create(image = uploaded_file, product = product)
    return redirect('/admin_page')

def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('/admin_page')

def edit_user_page(request, user_id):
    context = {
        'user': User.objects.get(id = user_id)
    }
    return render(request, 'store/edituser.html', context)

def edit_user(request, user_id):
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/edit_user_page/'+str(user_id))
    user = User.objects.get(id = user_id)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('/admin_page')

def delete_product(request, product_id):
    Product.objects.get(id=product_id).delete()
    return redirect('/admin_page')

def edit_product_page(request, product_id):
    context = {
        'product': Product.objects.get(id = product_id)
    }
    return render(request, 'store/editproduct.html', context)

def edit_product(request, product_id):
    errors = Product.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/edit_product_page/'+str(product_id))
    product = Product.objects.get(id = product_id)
    product.name = request.POST['name']
    product.price = request.POST['price']
    product.brand = request.POST['brand']
    product.category = request.POST['category']
    product.sub_category = request.POST['sub_category']
    product.availability = request.POST['availability']
    product.description = request.POST['description']
    product.save()
    return redirect('/admin_page')

# Category Page

def category(request, product_category):
    print(product_category)
    context = {
        'all_products': Product.objects.filter(category= product_category).order_by('name'),
    }
    print(context['all_products'])
    return HttpResponse(render(request,'store/categorize.html', context))

def sub_category(request, product_category, product_sub_category):
    context = {
        'sub_products': Product.objects.filter(category= product_category).filter(sub_category= product_sub_category).order_by('name'),
    }
    return HttpResponse(render(request,'store/sub_categorize.html', context))

def brand(request, product_brand):
    context = {
        'brand_products': Product.objects.filter(brand = product_brand).order_by('name'),
    }
    return HttpResponse(render(request,'store/brand.html', context))

def categorypg(request, product_category):
    context = {
        'all_products': Product.objects.filter(category= product_category).order_by('name'),
    }
    return render(request,'store/category.html', context)

def sub_categorypg(request, product_category, product_sub_category):
    context = {
        'all_products': Product.objects.filter(category= product_category).filter(sub_category= product_sub_category).order_by('name'),
    }
    return render(request,'store/category.html', context)

def review_product(request, product_id):
    is_valid = True
    if len(request.POST['review']) < 3:
    	is_valid = False
    if not is_valid:    # if any of the fields switched our is_valid toggle to False
        return redirect("/product_page/"+str(product_id))
    else:
        product = Product.objects.get(id = product_id)
        Review.objects.create(user = User.objects.get(id = request.session['user_id']), product = Product.objects.get(id = product_id), review = request.POST['review'], rating = request.POST['rating'])
        return redirect("/product_page/"+str(product_id))



