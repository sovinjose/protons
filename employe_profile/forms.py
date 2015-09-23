import datetime
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import UserProfile


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class':'form-control'}),max_length=30,min_length=3)
    email = forms.EmailField( widget=forms.EmailInput(
                              attrs={'placeholder': 'Email','class':'form-control input-perso'}),
                              max_length=100,error_messages={'invalid': ("Email invalide.")})
    password1 = forms.CharField(max_length=50,
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control'}))
    password2 = forms.CharField(max_length=50,
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class':'form-control'}))

    #recaptcha = ReCaptchaField()

    #Override of clean method for password check
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = "passwords are not matching"

        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            self._errors['username'] = "User name is already taken"
        except User.DoesNotExist:
            return username

        return self.cleaned_data

    #Override of save method for saving both User and Profil objects
    def save(self, datas):
        u = User.objects.create_user(datas['username'],
                                     datas['email'],
                                     datas['password1'])
        u.is_active = False
        u.save()
        profil=UserProfile()
        profil.user=u
        profil.activation_key=datas['activation_key']
        profil.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profil.save()
        return u

    #Handling of activation email sending ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #I am using a text file to write the email (I write my email in the text file with templatetags and then populate it with the method below)
    def sendEmail(self, datas):
        link="http://127.0.0.1:8000/activate/"+datas['activation_key']
        subject = '[USER ALERT] Your Account has been created'
        mail_context_variables = Context({
            'username': datas['username'],
            'first_name': datas['username'],
            'link': link
        })
        html_content = render_to_string('user_registration_mail_template.html', mail_context_variables)
        print ">>>>>>>>>>>>>>", settings.EMAIL_HOST_USER, datas['email']


        msg = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        to=[datas['email']],
        from_email=settings.EMAIL_HOST_USER,
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

    def clean_Username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise validators.ValidationError('The username "%s" is already taken.' % username)



