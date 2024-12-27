from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.contrib.auth.hashers import make_password
import time 

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                auth_login(request, user)
                messages.success(request, "connextion reussie")
                print(messages.success)
                return redirect ('profile')
            else :
                return  HttpResponseRedirect('erreur de username ou mot de passe')
                
    else : 
        form = AuthenticationForm()
    return render (request, 'login.html', {'form':form})

#stock temporairement les codes de réinitialisation

def request_reset_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        try :
            user = User.objects.get(email=email)
            #Génère un code aléatoire*
            code = random.randint(100000,999999)
            request.session['reset_code'] = code  #stocke le code avec email
            request.session['reset_email'] = email
            send_mail(
                "code de rénitialisation", f" votre code de réinitialisation est : {code} ", "therryconsu@gmail.com", [email],
                fail_silently=False
            )
            messages.success(request, "Un code de réinitialisation a été envoyé à votre adresse e-mail")
            return redirect ("verify_reset_code")
        except User.DoesNotExist :
            messages.error(request, "Aucun utilisateur trouvé avec cet e-mail")
    return render (request, "request_reset_password.html")

EXPIRATION_TIME = 5 * 60

def verify_reset_code(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        code = request.POST.get("code")
        print({request.session.get('reset_email')})
        print({request.session.get('reset_code')})
        print(f" code entré {code} ")
        if email == request.session.get("reset_email") and str(code) == str(request.session.get("reset_code")): 
            return redirect ('reset_password')
        
        else :
            messages.error(request,"code invalide ou expiré")
    return render (request, "verify_reset_code.html")

def reset_password(request):
    if "reset_email" not in request.session :
        return redirect ('request_reset_password')
    if request.method == 'POST' : 
        password = request.POST.get('password')
        email = request.session['reset_email']
        try : 
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            del request.session["reset_email"] #nettoie la session
            messages.success(request, "Mot de passe réinitialisé avec succès")
            return redirect ("login")
        except User.DoesNotExist :
            messages.error(request, "aucun utilisateur trouvé avec cet email")
            return redirect('request_reset_password')
    return render (request, 'reset_password.html')