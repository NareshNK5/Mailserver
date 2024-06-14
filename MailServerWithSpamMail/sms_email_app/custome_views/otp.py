import random,math
import http.client
import json
from django.http import HttpResponse,HttpResponseRedirect

def otp_gen():
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTP = ""
    for i in range(8) :
        OTP = OTP+string[math.floor(random.random() * len(string))]
    sms_otp,email_otp = OTP[0:4],OTP[4:]
    print(sms_otp+email_otp)
    print(OTP)

def send_sms(message, to):
  conn = http.client.HTTPConnection("sms.simsys.in")
  payload = { "sender": "kicetp", "route": "4", "country": "91", "sms": [ { "message":message, "to":to }] }
  payload = json.dumps(payload) 
  headers = {
      'authkey': "315666AxCOLU94oJt5e318659",
      'content-type': "application/json"
      }
  conn.request("POST","/api/sendhttp.php?authkey=315666AxCOLU94oJt5e318659&mobiles=918675456387&message=Your%20Register%20No%3A%7B%23var%23%7Dpassword%3A%7B%23var%23%7DKongu%20Institute%20of%20Computer%20Education&sender=KICETP&route=4&country=91&DLT_TE_ID=1207161597665362120")
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))
  for i in to:
    data={
        "message":message,
        "to":i,
        }
  print(data)
send_sms("test","9843545424")