from django.urls import path
from sms_email_app import views
from sms_email_app.custome_views import login,email

urlpatterns = [
    path('',views.home),
    path('login',login.login),
    path('logout',login.logout),
    path('register',login.register),
    path('log_user',login.log_user),
    path('register_user',login.register_user),
    path('val_email',login.val_email),
    path('val_sms',login.val_sms),
    path('otp',login.otp),
    path('otp_verification',login.otp_verification),
    
    # ---------------email---------------------
    path('inbox',email.inbox),
    path('sendmail',email.sendmail),
    path('send',email.send),
    path('emailview/<int:id>/',email.emailview),
    path('emaildelete/<int:id>/',email.emaildelete),
    path('emailspam/<int:id>/',email.emailspam),
    path('bin',email.bin,name="bin"),
    path('secretotp',email.secretotp,name="secretotp"),
    # spam
    path('spam',email.spam),
    path('spamadd',email.spamadd),
    path('spamdelete/<int:id>/',email.spamdelete),
    
    
]