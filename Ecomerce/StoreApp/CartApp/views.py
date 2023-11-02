# Import necessary modules
from decimal import Decimal
from django.shortcuts import render, redirect
from ..models import Product
from .forms import quantityForm
from django.http import JsonResponse, HttpResponseBadRequest


# Define the cart view
def cart(request):
    # Create instance of the quantity form
    quantity_form = quantityForm()
    shipping_places = get_shipping_places()
    # Check if a cart exists in the session
    if "cart" in request.session:
        # Get the cart from the session
        cart = request.session["cart"]
        # Get the products that are in the cart
        products = Product.objects.filter(id__in=cart.keys())
        # Add the quantity and subtotal for each product to the product instance
        for product in products:
            product.quantity = cart[str(product.id)]["quantity"]
            product.subtotal = cart[str(product.id)]["subtotal"]

        # Create the context dictionary with the products, cart attributes, forms, and total
        context = {
            "products": products,
            "cart_attr": request.session["cart"],
            "quantity_form": quantity_form,
            "total": total_import(request),
        }
    else:
        # Create the context dictionary with a message and the quantity form
        context = {"message": "No hay productos en el carrito",
                   "quantity_form": quantity_form}

    context.update({"shipping_places":shipping_places})
    # Render the cart template with the context dictionary
    return render(request, "cart.html", context)


# Define the add-to-cart view
def add_to_cart(request):
    if request.method == "POST":
        # Set response dict
        data = {'in_stock': 0}
        # Get the product reference from database
        product = Product.objects.get(id=request.POST.get("product_id"))
        # Get the price variable
        price = (product.discount_price if product.discount_price else product.price)
        # Set message variable
        message = "Producto añadido al carrito"
        # Get session cart
        cart = request.session.get("cart", {})
        # If product is in cart and no quantity passed display Product already in cart
        quantity_form = quantityForm(request.POST)
        if quantity_form.is_valid():
            # Get quantity variable
            quantity = int(request.POST["quantity"])
            if str(product.id) in cart:
                message = "El producto ya está en el carrito"
            # If product quantity is passed add product quantity to the cart
            elif product.in_stock < quantity:
                message = "Solo quedan " + \
                    str(product.in_stock) + " productos"
                data['in_stock'] = product.in_stock
            elif str(product.id) not in cart:
                message = str(quantity) + " " + product.name + \
                    " añadido al carrito"
                subtotal = price * quantity
                cart[str(product.id)] = {"subtotal": str(subtotal),
                                         "quantity": quantity,
                                         "price": str(price),
                                         }
        else:
            message = "Quantity must be a number"
        # Save the session cart variable
        request.session["cart"] = cart
        # Set the data for the add-to-cart response
        data['message'] = message
        return JsonResponse(data)


# Define the update-cart view
def update_cart(request):
    if request.method == "POST":
        for product_id, quantity in request.POST.items():
            # Get the quantity form from the request data
            quantity_form = quantityForm({'quantity': quantity})
            # Check if the form is valid
            if quantity_form.is_valid():
                # Get the cart dictionary from the session for the current product ID
                cart = request.session["cart"]

                # Get the price of the product from the cart dictionary as a Decimal object
                price = Decimal(cart[str(product_id)]["price"])

                # Calculate the subtotal and total for the updated products
                subtotal = str(price * int(quantity))

                # Update the quantity and subtotal values in the cart dictionary for the current product ID
                cart[str(product_id)]["quantity"] = quantity
                cart[str(product_id)]["subtotal"] = subtotal

                # Store the updated cart dictionary back in the session for the current product ID
                request.session["cart"] = cart
                # Construct a JSON response containing the new subtotal value
                data = {
                    "subtotal": subtotal,
                    "total": total_import(request),
                }
                return JsonResponse(data)
        else:
            return redirect('Cart')


# Define the delete-product view
def delete_product(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        if product_id in request.session['cart']:
            # Delete the product from the cart dictionary and set the session as modified
            del request.session["cart"][product_id]
            if len(request.session["cart"]) == 0:
                del request.session["cart"]
            request.session.modified = True
            # Set the data for the delete-product response
            data = {"message": "Producto eliminado",
                    "total": total_import(request)}
            return JsonResponse(data)
        else:
            return JsonResponse("No hay productos a eliminar")


# Define the total_import function to calculate the total cost of the items in the cart
def total_import(request):
    # Set the initial total to 0
    total_import = Decimal(0.0)
    # Sum the shipping_price if exists
    if "shipping" in request.session:
        shipping_price = [i for i in request.session["shipping"].values()]
        total_import += shipping_price[0]
    # Check if there is a cart in the session
    if "cart" in request.session:
        # Loop through each product in the cart and add its subtotal to the total
        for subtotal in request.session["cart"].values():
            total_import += Decimal(subtotal["subtotal"])
    # Convert the total to a string and return it
    total_import = str(total_import)
    return total_import

def set_shipping(request):
    if request.POST:
        session = request.session.get("shipping", {})
        shipping_places = get_shipping_places()
        key = request.POST['shippingKey']
        for i, j in shipping_places.items():
            if type(j) == int and key == i:
                shipping_price = shipping_places[key]
                data = {"key":key, "shipping_price":shipping_price}
                break
            elif type(j) == dict and key in j.keys():
                shipping_price = j[key]
                data = {"key":key, "shipping_price":shipping_price}
                break
        else:
            data = {"key":"Elige Domicilio", "shipping_price":0}
        session["shipping"] = {data["key"]:data["shipping_price"]}
        request.session["shipping"] = session["shipping"]
        data.update({"total":total_import(request)})
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest()

def get_shipping_places():
    shipping_places = {
        "Elige domicilio":0,
        "10 de octubre":{
            "Lawton": 375,
            "Luyano": 375,
            "10/10(Otros)": 350,},
        "Arroyo Naranjo":{
            "Mantilla": 450,
            "Calvario": 450,
            "Párraga": 450,
            "Reparto Eléctrico": 500,
            "Guásimas": 550,
            "Arroyo Naranjo(Otros)":400,},
        "Boyeros":{
            "Wajay-Mulgoba": 450,
            "Calabazar": 500,
            "Fortuna": 500,
            "Santiago de las Vegas": 500,
            "Managua": 600,
            "Sierra":550,
            "El Chico":550,
            "El Cano":550,
            "Rincón": 550,
            "Boyeros(Otros)": 400,},
        "Centro Habana": 325,
        "Cerro": 350,
        "Cotorro":{
            "Cuatro Camino": 600,
            "Cotorro(Otros)":550,},
        "Guanabacoa":{
            "Puente de Santa Fé": 500,
            "Barreras":550,
            "Minas":550,
            "Campo":550,
            "Peñalver": 550,
            "Guanabacoa(Otros)": 450,},
        "Habana Vieja": 350,
        "Habana del Este":{
            "Playas del Este": 550,
            "Peñas Altas": 600,
            "Habana del Este(Otros)": 500,},
        "Lisa":{
            "hasta 250": 350,
            "Arroyo Arena": 400,
            "Novia": 400,
            "Cano": 550,
            "Valle Grande": 550,
            "Gutao": 550,
            "Punta Brava": 550,
            "UCI": 600,},
        "Marianao":{
            "Hasta 114": 275,
            "Marianao(114 en adelante)": 325,},
        "Playa":{
            "(hasta el paradero)": 250,
            "Siboney": 325,
            "Atabey": 325,
            "Flores": 325,
            "Náutico": 325,
            "Jaimanita": 400,
            "Santa Fe": 425,
            "Barbosa": 450,
            "Baracoa ELAM": 550,},
        "Regla":{
            "Casablanca": 500,
            "Regla(Otros)":450,},
        "San Miguel": 450,
        "Vedado": 300,
    }
    return shipping_places