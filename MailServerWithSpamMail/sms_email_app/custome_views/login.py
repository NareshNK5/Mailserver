from django.shortcuts import render
from sms_email_app.models import tbluser
import random,math
import http.client
import json
import smtplib
import sys
import usb.core
from django.http import HttpResponse,HttpResponseRedirect


def login(request):
    return render(request,"login/login.html")

def logout(request):
    del request.session['user']
    return HttpResponseRedirect('login')

def register(request):
    return render(request,"login/register.html")

def register_user(request):
    if request.method=="POST":
        
        dev = usb.core.find(find_all=True)
        if dev is None:
            print("No USB devices found.")
            sys.exit(1)
        for cfg in dev:
            vender_id = cfg.idVendor
            product_id = cfg.idProduct
            print('vender_id:',vender_id,'\nproduct_id:',product_id)
            
        un = request.POST["username"]
        request.session["user"]=un
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        ps = request.POST["password"]
        otp = otp_gen()
        print(otp)
        obj = tbluser()
        obj.username = un
        obj.email = email
        obj.mobile = mobile
        obj.password = ps
        obj.vender_id = vender_id
        obj.product_id = product_id
        obj.otp = otp
        obj.save()
        send_email(otp,email)
        # send_sms(otp,mobile)
        # return render(request,"login/otp.html",{"msg":"Check Your Email or Mobile For Your Verication OTP"})
        return HttpResponseRedirect('otp')
    # -----------------------OTP----------------------------------------------------- 
def otp_gen():
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTP = ""
    for i in range(5) :
        OTP = OTP+string[math.floor(random.random() * len(string))]
    return OTP

def send_sms(sms_otp,mobile):
  conn = http.client.HTTPSConnection("sms.simsys.in")
  payload = ""
  headers = {
        'authkey': "315666AxCOLU94oJt5e318659",
        'content-type': "application/json"
  }
  conn.request("POST","http://sms.simsys.in/api/sendhttp.php?authkey=315666AxCOLU94oJt5e318659&mobiles=9843545424&message=Your User Registration OTP is%3A%7B%23var%23%7DKongu Institute of Computer Education &sender=KICETP&route=4&country=91&DLT_TE_ID=1207161597599026870", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))
  for i in mobile:
    data={
        "message":sms_otp,
        "to":i,
        }
  print(data,"OTP sended successfully")
  return data

def send_email(email_otp,email):
    
    fmail="nareshkaruna23@gmail.com"
    pwd='wmwtewhsouwfsfid'
    msg ="OTP="+email_otp+".This is for Educational Purpose Only.KICE INFO SYSTEM"
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo()
    server_ssl.login(fmail, pwd) 
    server_ssl.sendmail(fmail, email, msg)
    server_ssl.close()
    print ("successfully sent the mail")
# -----------------------end OTP----------------------------------------------------- 

def log_user(request):
    if request.method=="POST":
        un = request.POST["username"]
        ps = request.POST["password"]
        dev = usb.core.find(find_all=True)
        if dev is None:
            print("No USB devices found.")
            sys.exit(1)
        for cfg in dev:
            vender_id = cfg.idVendor
            product_id = cfg.idProduct
            print('vender_id:',vender_id,'\nproduct_id:',product_id)
        
        try:
            if tbluser.objects.filter(username=un,password=ps,status=1,vender_id=vender_id,product_id=product_id).exists():
                request.session["user"]=un
                msg="Login Successfully"
                return HttpResponseRedirect('inbox')
            else:
                msg="Invalied Login"
                return render(request,"login/login.html",{"msg":msg})
        except Exception:
                return render(request,"login/login.html",{"msg":"Insert Physical Key"})
            

# -------------------------validation-----------------------------------------
def val_email(request):
    if request.method == "POST":
        e = request.POST["emailotp"]
        if tbluser.objects.filter(email_otp=e).exists():
            return render(request,"login/sms.html")
        else:
            msg = "Invalied Email OTP"
            return render(request,"login/email.html",{"msg":msg})

def val_sms(request):
    if request.method == "POST":
        e = request.POST["smsotp"]
        if tbluser.objects.filter(sms_otp=e).exists():
            msg = "OTP Successfully Valiedated"
            return render(request,"home.html",{"msg":msg})
        else:
            msg = "Invalied Mobile OTP"
            return render(request,"login/sms.html",{"msg":msg})

def otp(request):
    # print("test")
    if request.session.has_key('user'):
        un=request.session['user']
        print(un)
        return render(request,"login/otp.html",{'un':un,"msg":"Check Your Email or Mobile For Your Verication OTP"})

def otp_verification(request):
    if request.session.has_key('user'):
        if request.method=="POST":
            un=request.session['user']
            otp=request.POST["otp"]
                
            if tbluser.objects.filter(username=un,otp=otp).exists():
                obj=tbluser.objects.get(username=un)
                obj.status=1
                obj.save()
                return HttpResponseRedirect('login')
            return HttpResponseRedirect('otp')