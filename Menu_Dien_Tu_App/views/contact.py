from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Menu_Dien_Tu_App.forms import *
from templates import *
from django.contrib import messages
from django.template.loader import get_template


@login_required
def contactView(request):
    Contact_Form = ContactForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': Contact_Form})
    else:
        form = Contact_Form
        if form.is_valid():
            
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_content = request.POST.get('content')

            # template = get_template('templates/contact_form.txt')

            # context = {
            #     'contact_name': contact_name,
            #     'contact_email': contact_email,
            #     'contact_content': contact_content,
            # }
            
            # content = template.render(context)
            content = "- Contact name: " + contact_name + "\n\n" + "- Contact email: " + contact_email + "\n\n" + "- Contact content: " + "\n\t" + contact_content
            

            email = EmailMessage(
                "Just For Food In University",
                content,
                "Groups Team THTH" + '',
                ['grteam.tht131417@gmail.com'],
            )
        email.send()
        return redirect('success-send')


@login_required
def successView(request):
    messages.info(request, "Success! Thank you for your message.")
    return redirect('home')
