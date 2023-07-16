from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail

# Create your views here.


def contact(request):
    contact_form = ContactForm()
    context = {"contact_form": contact_form}

    return render(request, 'contact.html', context)


def send_message(request):
    if request.method =='POST':
        # get all form data
        form = ContactForm(data=request.POST)
        if form.is_valid():
            # If form is valid get all data
            name, subject, email, message = request.POST.get('name'), request.POST.get(
                'subject'), request.POST.get('email'), request.POST.get('message')
            # send email with proper data
            send_mail(subject=subject, message=message+'. {}'.format(name),
                      from_email=email, recipient_list=['dragntsu37@gmail.com'])
            # redirect to contact page
            return redirect("/Contact/?success")
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})