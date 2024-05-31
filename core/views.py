from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.forms import ProductForm
from core.forms import BrandForm
from core.models import Product
from core.models import Supplier
from core.models import Brand
from core.models import Category
from core.forms import SupplierForm
from core.forms import CategoryForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import re
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


def home(request):
   data = {
        "title1":"Autor | TeacherCode",
        "title2":"Super Mercado Economico"
    }
   return render(request,'core/home.html',data)


def is_password_strong(password):
    # Verificar longitud mínima
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    
    # Verificar que contenga al menos una letra
    if not re.search(r"[a-zA-Z]", password):
        return False, "La contraseña debe contener al menos una letra."
    
    # Verificar que contenga al menos un número
    if not re.search(r"\d", password):
        return False, "La contraseña debe contener al menos un número."
    
    # Verificar que contenga al menos un símbolo
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>-_]", password):
        return False, "La contraseña debe contener al menos un símbolo."
    
    return True, ""

def signup(request):
    if request.method == "GET":
        return render(request, "core/signup/signup.html", {"form": UserCreationForm()})
    else:
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(
                request,
                "core/signup/signup.html",
                {"form": UserCreationForm(), "error": "Las contraseñas no coinciden."},
            )

        if password1 == username:
            return render(
                request,
                "core/signup/signup.html",
                {"form": UserCreationForm(), "error": "La contraseña no puede ser igual al nombre de usuario."},
            )

        is_strong, message = is_password_strong(password1)
        if not is_strong:
            return render(
                request,
                "core/signup/signup.html",
                {"form": UserCreationForm(), "error": message},
            )

        try:
            user = User.objects.create_user(
                username=username,
                password=password1,
            )
            user.save()
            login(request, user)
            return redirect("home")
        except IntegrityError:
            return render(
                request,
                "core/signup/signup.html",
                {"form": UserCreationForm(), "error": "El usuario ya existe."},
            )
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "core/signin/signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(request, "core/signin/signin.html", 
                          {"form": AuthenticationForm,
                           'error': 'Usuario o contraseña es incorrecta.'
                           })
        else:
            login(request, user)
            return redirect('home')
        
# productos
def product_List(request):
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos"
    }
    products = Product.objects.all() # select * from Product
    data["products"]=products
    return render(request,"core/products/list.html",data)

# crear un producto
@login_required
def product_create(request):
    data = {"title1": "Productos","title2": "Ingreso De Productos"}
    
    if request.method == "POST":
        #print(request.POST)
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("core:product_list")

    else:
        data["form"] = ProductForm() # controles formulario sin datos

    return render(request, "core/products/form.html", data)

# editar un producto
@login_required
def product_update(request,id):
    data = {"title1": "Productos","title2": ">Edicion De Productos"}
    product = Product.objects.get(pk=id)
    if request.method == "POST":
      form = ProductForm(request.POST,request.FILES, instance=product)
      if form.is_valid():
            form.save()
            return redirect("core:product_list")
    else:
        form = ProductForm(instance=product)
        data["form"]=form
    return render(request, "core/products/form.html", data)

# eliminar un producto
@login_required
def product_delete(request,id):
    product = Product.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Producto","product":product}
    if request.method == "POST":
        product.delete()
        return redirect("core:product_list")
 
    return render(request, "core/products/delete.html", data)

# ? --------------------------------------------------------------------------------------------------------------------------------------------------------

# marcas
def brand_List(request):
    data = {
        "title1": "Marcas",
        "title2": "Consulta De Marcas De Productos"
    }
    
    brands = Brand.objects.all() # select * from Product
    data["brands"] = brands
    return render(request,"core/brands/list.html",data)

# crear marcas
@login_required
def brand_create(request):
    data = {"title1": "Marcas","title2": "Ingreso de Marca"}
   
    if request.method == "POST":
        #print(request.POST)
        form = BrandForm(request.POST,request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            brand.save()
            return redirect("core:brand_list")

    else:
        data["form"] = BrandForm() # controles formulario sin datos

    return render(request, "core/brands/form.html", data)

# editar marcas
@login_required
def brand_update(request,id):         
    data = {"title1": "Marcas","title2": ">Edicion De Marcas"}
    brand = Brand.objects.get(pk=id)
    if request.method == "POST":
      form = BrandForm(request.POST,request.FILES, instance=brand)
      if form.is_valid():
            form.save()
            return redirect("core:brand_list")
    else:
        form = ProductForm(instance = brand)
        data["form"] = form
    return render(request, "core/brands/form.html", data)

# eliminar marcas
@login_required
def brand_delete(request,id):        
    brand = Brand.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Una Marca","marca":brand}
    if request.method == "POST":
        brand.delete()
        return redirect("core:brand_list")
 
    return render(request, "core/brands/delete.html", data)

# ? ----------------------------------------------------------------------------------------------------------------------------------------------

# proveedores
def supplier_List(request):
    data = {
        "title1": "Proveedores",
        "title2": "Consulta De proveedores"
    }
    
    supplier = Supplier.objects.all() # select * from Product
    data["supplier"] = supplier
    return render(request,"core/suppliers/list.html",data)

# crear proveedores
@login_required
def supplier_create(request):
    data = {"title1": "Proveedores","title2": "Añadir Proveedor"}
   
    if request.method == "POST":
        #print(request.POST)
        form = SupplierForm(request.POST,request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.save()
            return redirect("core:supplier_list")
        
    else:
        data["form"] = SupplierForm() # controles formulario sin datos

    return render(request, "core/suppliers/form.html", data)

# actualizar proveedores
@login_required
def supplier_update(request,id):         
    data = {"title1": "Proveedores","title2": ">Editar Proveedor"}
    supplier = Supplier.objects.get(pk=id)
    if request.method == "POST":
      form = SupplierForm(request.POST,request.FILES, instance=supplier)
      if form.is_valid():
            form.save()
            return redirect("core:supplier_list")
    else:
        form = SupplierForm(instance = supplier)
        data["form"] = form
    return render(request, "core/suppliers/form.html", data)

# eliminar proveedores
@login_required
def supplier_delete(request,id):        
    supplier = Supplier.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar un Proveedor","Proveedor":supplier}
    if request.method == "POST":
        supplier.delete()
        return redirect("core:supplier_list")
 
    return render(request, "core/suppliers/delete.html", data)

# ? -------------------------------------------------------------------------------------------------------------------------------------

# categorias
def category_List(request):
    data = {
        "title1": "Categorias",
        "title2": "Consulta De Categorias De Productos"
    }
    
    categories = Category.objects.all() # select * from Product
    data["categories"] = categories
    return render(request,"core/categories/list.html",data)

# creaer categorías
@login_required
def category_create(request):
    data = {"title1": "Categorias","title2": "Ingreso de Categoria"}
   
    if request.method == "POST":
        #print(request.POST)
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("core:category_list")

    else:
        data["form"] = CategoryForm() # controles formulario sin datos

    return render(request, "core/categories/form.html", data)

# actualizar categorías
@login_required
def category_update(request,id):         
    data = {"title1": "Categorias","title2": ">Edicion De Categorias"}
    category = Category.objects.get(pk=id)
    if request.method == "POST":
      form = CategoryForm(request.POST,request.FILES, instance=category)
      if form.is_valid():
            form.save()
            return redirect("core:category_list")
    else:
        form = CategoryForm(instance = category)
        data["form"] = form
    return render(request, "core/categories/form.html", data)

# eliminar categorias
@login_required
def category_delete(request,id):        
    category = Category.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Una Marca","marca":category}
    if request.method == "POST":
        category.delete()
        return redirect("core:category_list")
 
    return render(request, "core/categories/delete.html", data)