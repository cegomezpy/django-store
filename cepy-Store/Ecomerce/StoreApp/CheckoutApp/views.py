from django.shortcuts import render, redirect
from ..CartApp.views import total_import
from django.core.mail import send_mail
from .forms import CheckoutForm
from ..models import Product
from .models import Shipping, ShippingProducts

# Create your views here.
def checkout(request):
    # Create a CheckoutForm instance
    checkout_form = CheckoutForm()
    # Create a dictionary with the CheckoutForm instance and the total value of the cart
    context = {}
    # Check if the cart exists in the session
    if "cart" in request.session:
        # Get the cart from the session
        cart = request.session["cart"]
        # Get the products that are in the cart
        products = Product.objects.filter(id__in=cart.keys())
        # Add the quantity and subtotal of each product to the corresponding product instance
        message = []
        for product in products:
            quantity = cart[str(product.id)]["quantity"]
            subtotal = cart[str(product.id)]["subtotal"]
            if product.in_stock < int(quantity):
                message.append("There are only "+ str(product.in_stock) + " of " + product.name)
                product.quantity = product.in_stock
                product.subtotal = product.in_stock * product.discount_price
                cart[str(product.id)]['quantity'] = product.in_stock
                cart[str(product.id)]['subtotal'] = str(product.subtotal)
            else:
                product.quantity = quantity
                product.subtotal = subtotal
        # Add the products to the context dictionary
        context["message"] = message
        context["checkout_form"]=checkout_form
        context["total"]=total_import(request)
        context["products"] = products
        request.session["cart"] = cart
    return render(request, 'checkout.html', context)

def shipping(request):
    if "cart" not in request.session:
        print("redirecting")
        return redirect("/Checkout/")
    # Create a Shipping instance with the total income of the order
    shipping = Shipping(total_income = total_import(request))
    # If the user is authenticated, set the user attribute of the Shipping instance to the authenticated user
    if request.user.is_authenticated:
        shipping.user = request.user
    shipping.save()
    # Get the cart from the session
    cart = request.session.get('cart')
    # Get the products that are in the cart
    products = Product.objects.filter(id__in = cart.keys())
    shipping_products = []
    for key, value in cart.items():
        shipping_product = ShippingProducts(
            product=products.get(id=key),
            shipping=shipping,
            quantity=value['quantity'],
        )
        shipping_products.append(shipping_product)
    # Create ShippingProducts instances for each product in the cart and add them to the database
    ShippingProducts.objects.bulk_create(shipping_products)
    # Generate a message with the order information
    ship_text = make_message(request, shipping, products)
    email_ship_text = ship_text.replace("%0a", "\n")
    # Send the message to a WhatsApp number
    url = send_whatsapp(ship_text)
    # Send an email with the message to a recipient
    send_mail(message=email_ship_text, subject="Order-"+str(shipping.id), from_email= (request.user.email if request.user.is_authenticated else request.POST['email']),recipient_list=['dragntsu37@gmail.com'])
    # Redirect the user to the WhatsApp chat with the order
    return redirect(url)

def make_message(request, shipping, products):
    text = ""
    cart = request.session.get('cart')
    for i in products:
        text += f"%0a*id_producto*:{i.id}%0anombre_producto:{i.name}%0a-precio_unitario:${cart[str(i.id)]['price']}%0a-cantidad:{cart[str(i.id)]['quantity']}%0a-subtotal:{cart[str(i.id)]['subtotal']}%0a----------------"
    # If the checkout form was submitted, create a message with the form data and the order information
    if request.POST:
        checkout_form = CheckoutForm(request.POST)
        if checkout_form.is_valid:
            first_name = request.POST['first_name']
            address = request.POST['address']
            mobile_number = request.POST['phone_number']
            ship_text = f"---------Pedido{shipping.id}---------%0a*Nombre*: {first_name}%0a*Address*: {address}%0a*Mobile_number*: https://wa.me/{mobile_number} %0a*Precio Total*: ${shipping.total_income}%0a*Fecha del shipping*: {shipping.date_created}%0a....*Productos Pedidos*....{text}"
    # If the checkout form was not submitted, create a message with the user data and the order information

    else:
        ship_text = f"---------Pedido{shipping.id}---------%0a*Nombre*: {shipping.user.first_name}%0a*Address*: {shipping.user.client.address}%0a*Mobile_number*: https://wa.me/{shipping.user.client.mobile_number} %0a*Precio Total*: ${shipping.total_income}%0a*Fecha del shipping*: {shipping.date_created}%0a....*Productos Pedidos*....{text}"

    return ship_text

def send_whatsapp(ship_text):
    # Replace spaces and special characters with the corresponding
    joiner = "%20"
    mess = ship_text.replace(" ", joiner).replace("<", joiner).replace(">", "")
    # Create a URL with the WhatsApp chat API and the encoded message
    url = f"https://wa.me/5355091046?text={mess}"

    return url
