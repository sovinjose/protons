import sha
import random
import hashlib
import datetime
from django.utils import timezone
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.generic import View
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import RegistrationForm


class UserWelcomePage(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('/accounts/login/')
        return render(request, 'user_welcome.html')


class UserAccountConformation(View):
    def get(self, request):
        return render(request, 'account_activate.html')



class UserRegistration(View):

    form_class = RegistrationForm

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/')
        context = {
            'form' : self.form_class()
        }
        return render(request, 'registration.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            datas={}
            datas['username']=request.POST['username']
            datas['email']=request.POST['email']
            datas['password1']=request.POST['password1']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]

            usernamesalt = datas['username']
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

            datas['email_path']="/ActivationEmail.txt"
            datas['email_subject']="Activation de votre compte yourdomain"

            form.sendEmail(datas) #Send validation email
            form.save(datas) #Save the user and his profile

            request.session['registered']=True #For display purposes
            
            return render(request, 'account_activate.html', {'name': datas['username']})
        context = {
            'form' : form
        }
        return render(request, 'registration.html', context)


class UserActivation(View):

    def get(self, request, key):
        print "??????????????????????????????/", request.META.get('HTTP_HOST')
        activation_expired = False
        already_active = False
        profil = get_object_or_404(UserProfile, activation_key=key)
        print '%s/new-activation-link/%s' % (request.META.get('HTTP_HOST'), profil.user.id)
        if profil.user.is_active == False:
            if timezone.now() > profil.key_expires:
                activation_expired = '%s/new-activation-link/%s' % (request.META.get('HTTP_HOST'), request.user.id)
            else: #Activation successful
                profil.user.is_active = True
                profil.user.save()
                return redirect('/accounts/login/')

        #If user is already active, simply display error message
        else:
            already_active = True #Display : error message

        context = {
            'activation_expired' : activation_expired,
            'already_active' : already_active,
            'name': profil.user
        }
        return redirect('/accounts/login/')


class UserNewActivationLink(View):

    def get(self, request, user_id):
        form = RegistrationForm()
        datas={}
        user = User.objects.get(id=user_id)
        if user is not None and not user.is_active:
            datas['username']=user.username
            datas['email']=user.email
            datas['email_path']="/ResendEmail.txt"
            datas['email_subject']="Nouveau lien d'activation yourdomain"

            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = datas['username']
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()
            profil = Profil.objects.get(user=user)
            profil.activation_key = datas['activation_key']
            profil.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
            profil.save()
            form.sendEmail(datas)
            request.session['new_link']=True #Display : new link send

        return redirect('/gg/')
