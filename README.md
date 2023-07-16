# cepyStore
## Overview:
This online store was develop to anyone who wants an ecommerce website in production quickly.

## Project Structure
	Ecommerce:
	 	|
		---AuthApp: Implements the users authentications.
	 	|
		---UserApp: Implemented to extend the User fields.
	        |	
		---ContactApp: Allows the user to send an email to the owner
		|
		---StoreApp: Show products cards and implement filters for category and prices as the status of products(available or not)
			  |
			  ---DetailsApp: Detailed view of each product showing description and reviews.
	  		  |		|
			  |		---ReviewsApp: Reviews and rating from users. Users can comment only if they are logged in.
			  |	
	  		  ---CartApp: ShopCart where user can update quantity, see their import and go to checkout
			  |
			  ---CheckoutApp: Checkout where user gives their bill address and more information need.

## Some features:
	* in_stock attribute of products reduced when admin changes the order status to delivered.
	* Category and price filtering(Union(U) filtering), search bar is integreted as a filter.
	* star system in Reviews rating implemented with Jquery
	* Ajax requests for add products to the cart, delete products from the cart or update quantity products in the cart. Also when posting a review.
	* Pop up message to alert if the product was successfully added to the cart or there was a problem adding it.
## In progress feature:
	* Dashboard with statistics results of sells and demand of products to show to the client and to the owner.

## Configuration
Create a file to set enviroment variables. Here is how to setup your email config and generate a password for the email app from your google account: [abstractapi.com](https://abstractapi.com/guides/django-send-email)
```python
ALLOWED_HOSTS = ['your allowed hosts']
DEBUG = True or False //depending of your enviroment

# SECURITY WARNING: keep the secret key used in production secret!
def secret_key():
    SECRET_KEY = 'secret_key'
    return SECRET_KEY

def databases():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.backend_you_are_using',
            'NAME': 'name_of_your_database',
            'USER': 'username',
            'PASSWORD': 'password',
            'HOST': 'host',
            'DATABASE_PORT': 'port',
        }
    }
    return DATABASES

def set_email_config():
    # Email config
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend" # Im using smtp protocol
    EMAIL_HOST="smtp.gmail.com"
    EMAIL_USE_TLS=True
    EMAIL_PORT='email port'
    EMAIL_HOST_USER="email"
    EMAIL_HOST_PASSWORD="password"
    return EMAIL_BACKEND, EMAIL_HOST, EMAIL_USE_TLS, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
```
### in settings.py
```python
from . import secure_info
ALLOWED_HOSTS = secure_info.ALLOWED_HOSTS
DEBUG = secure_info.DEBUG

SECRET_KEY = secure_info.secret_key()

DATABASES = secure_info.databases()

EMAIL_BACKEND, EMAIL_HOST, EMAIL_USE_TLS, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = secure_info.set_email_config()
```
## License
#### Template Design by [HTML Codex](https://htmlcodex.com) and [CeGomezPy](https://linkedin.com/in/cegomezpy). Distributed by [ThemeWagon](https://themewagon.com)
#### Backend developed by: [CeGomezPy](https://linkedin.com/in/cegomezpy)
#### [MIT](https://choosealicense.com/licenses/mit/) License
