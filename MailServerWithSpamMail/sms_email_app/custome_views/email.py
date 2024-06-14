from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from sms_email_app.models import *
from django.db.models import Q
from base64 import urlsafe_b64decode,urlsafe_b64encode
from cryptography.fernet import Fernet
from django.conf import settings
import logging
import traceback

def inbox(request):
    if request.session.has_key("user"):
        frm=request.session["user"]
        frm=tbluser.objects.get(username=frm)
        msg=tblemail.objects.filter(to=frm.id,on_spam=0)
        spam=tblspam.objects.filter(user=frm.id,on_delete=0)
        if spam.count()>=0:
            pass
        else:
            for i in spam:
                queryset = tblemail.objects.filter( ~Q(subject__icontains=i.spamword) & ~Q(message__icontains=i.spamword))
                for j in queryset:
                    j.on_spam=1
                    j.save()
        msg=tblemail.objects.filter(to=frm.id,on_spam=0)
    return render(request,'email/inbox.html',{'frm':frm,'msg':msg,'spam':spam,'email':frm.email})

def sendmail(request):
    if request.session.has_key("user"):
        if request.method=="POST":
            frm=request.POST["frmemail"]
            frm=tbluser.objects.get(email=frm)
            to=request.POST["toemail"]
            to=tbluser.objects.get(email=to)
            msg=request.POST["message"]
            sub=request.POST["subject"]
            sk=request.POST["secretkey"]
            #message was encode here only
            try:
                cipher_suite = Fernet(settings.ENCRYPT_KEY)
                print("cipher_suite key",cipher_suite)
                encrypted_text = cipher_suite.encrypt(msg.encode('ascii'))
                encrypted_text = urlsafe_b64encode(encrypted_text).decode("ascii")# encode to urlsafe base64 format
            except Exception as e:
                # log the error if any
                logging.getLogger("error_logger").error(traceback.format_exc()) 

            obj=tblemail()
            obj.frm=frm
            obj.to=to
            obj.subject=sub
            obj.message=encrypted_text
            obj.secretkey=sk
            obj.save()
            return render(request,'email/inbox.html')

def secretotp(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            otp=request.POST["otp"]
            frm=request.session["user"]
            frm=tbluser.objects.get(username=frm)
            msg=tblemail.objects.get(to=frm,secretkey=otp)
            ms=msg.message
            print(ms)
            try:
                # base64 decode
                cipher_suite = Fernet(settings.ENCRYPT_KEY)
                m = urlsafe_b64decode(ms)
                decoded_text = cipher_suite.decrypt(m).decode("ascii")
                # decoded_text = cipher_suite.decrypt(base64.urlsafe_b64decode(ms)).decode("ascii")
            except Exception as e:
                # log the error
                logging.getLogger("error_logger").error(traceback.format_exc())
                decoded_text = "Error %s:"%e 
                 
        return render(request,"email/viewemail.html",{'d_msg':decoded_text,'i':msg})

def send(request):
    if request.session.has_key("user"):
        frm=request.session["user"]
        frm=tbluser.objects.get(username=frm)
        msg=tblemail.objects.filter(frm=frm.id)
    return render(request,'email/send.html',{'frm':msg,'email':frm.email})
    
def emailview(request,id):
    if request.session.has_key("user"):
        obj = tblemail.objects.get(id=id)
        return render(request,"email/viewemail.html",{'i':obj})
    
def emaildelete(request,id):
    if request.session.has_key("user"):
        obj = tblemail.objects.get(id=id)
        obj.on_delete=1
        obj.save()
        print("deleted")
        return HttpResponseRedirect('/login/index')
    
def emailspam(request,id):
    if request.session.has_key("user"):
        obj = tblemail.objects.get(id=id)
        obj.on_spam=1
        obj.save()
        print("send to spam")
        return HttpResponseRedirect('/login/index')
def bin(request):
    if request.session.has_key("user"):
        un=request.session['user']
        user= tbluser.objects.get(username=un)
        obj = tblemail.objects.filter(to=user,on_delete=1)
        return render(request,"email/bin.html",{'msg':obj,'email':user.email})
# -----------------------Spam word---------------------------
def spam(request):
    if request.session.has_key("user"):
        un=request.session["user"]
        frm=tbluser.objects.get(username=un)
        sw=tblspam.objects.filter(user=frm.id,on_delete=0)
        msg=tblemail.objects.filter(to=frm.id,on_spam=1,on_delete=0)
    return render(request,'email/spam.html',{'sw':sw,'frm':msg,'email':frm.email})

def spamadd(request):
    if request.session.has_key("user"):
        un=request.session["user"]
        frm=tbluser.objects.get(username=un)
        if request.method == 'POST':
            spamword=request.POST['spamword']
            obj = tblspam()
            obj.user=frm
            obj.spamword=spamword
            obj.save()
            return HttpResponseRedirect('/login/spam')
    
def spamdelete(request,id):
    if request.session.has_key("user"):
        print("test")
        obj = tblspam.objects.get(id=id)
        obj.on_delete=1
        obj.save()
        print("deleted")
        return HttpResponseRedirect('/login/spam')

    
# -----------------------Spam mail---------------------------
