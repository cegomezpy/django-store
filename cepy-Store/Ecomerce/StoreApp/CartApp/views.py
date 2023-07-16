# Import necessary modules
from decimal import Decimal
from django.shortcuts import render, redirect
from ..models import Product
from .forms import quantityForm
from django.http import JsonResponse


# Define the cart view
def cart(request):
    # Create instance of the quantity form
    quantity_form = quantityForm()

    # Check if a cart exists in the session
    if "cart" in request.session:
        print("The cart exists")
        # Get the cart from the session
        cart = request.session["cart"]
        print(cart)
        # Get the products that are in the cart
        products = Product.objects.filter(id__in=cart.keys())
        # Add the quantity and subtotal for each product to the product instance
        for product in products:
            product.quantity = cart[str(product.id)]["quantity"]
            product.subtotal = cart[str(product.id)]["subtotal"]
            print(product.quantity)

        # Create the context dictionary with the products, cart attributes, forms, and total
        context = {
            "products": products,
            "cart_attr": request.session["cart"],
            "quantity_form": quantity_form,
            "total": total_import(request),
        }
    else:
        # Create the context dictionary with a message and the quantity form
        context = {"message": "There are no products in the cart",
                   "quantity_form": quantity_form}
    # Render the cart template with the context dictionary
    return render(request, "cart.html", context)


# Define the add-to-cart view
def add_to_cart(request):
    if request.method == "POST":
        # Set response dict
        data = {'in_stock':0}
        # Get the product reference from database
        print(request.POST.get("product_id"))
        product = Product.objects.get(id=request.POST.get("product_id"))
        # Get the price variable
        price = (product.discount_price if product.discount_price else product.price)
        # Set message variable
        message = "The product was added to the cart"
        # Get session cart
        cart = request.session.get("cart", {})
        # If product is in cart and no quantity passed display Product already in cart
        quantity_form = quantityForm(request.POST)
        if quantity_form.is_valid():
            # Get quantity variable
            quantity = int(request.POST["quantity"])
            if str(product.id) in cart:
                message = "The product is already in the cart"
            # If product quantity is passed add product quantity to the cart
            elif product.in_stock < quantity:
                message = "There are only " + \
                    str(product.in_stock) + " products left"
                data['in_stock'] = product.in_stock
            elif str(product.id) not in cart:
                message = str(quantity) + " " + product.name + \
                    " added to the cart"
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
        print(request.POST)
        for product_id, quantity in request.POST.items():
            # Get the quantity form from the request data
            quantity_form = quantityForm({'quantity': quantity})
            print(product_id, quantity)
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
                print(request.session["cart"])
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
            request.session.modified = True
            # Set the data for the delete-product response
            data = {"message": "Product deleted",
                    "total": total_import(request)}
            return JsonResponse(data)
        else:
            return JsonResponse("There is no product to delete")


# Define the total_import function to calculate the total cost of the items in the cart
def total_import(request):
    # Set the initial total to 0
    total_import = Decimal(0.0)
    # Check if there is a cart in the session
    if "cart" in request.session:
        # Loop through each product in the cart and add its subtotal to the total
        for subtotal in request.session["cart"].values():
            total_import += Decimal(subtotal["subtotal"])
    # Convert the total to a string and return it
    total_import = str(total_import)
    return total_import