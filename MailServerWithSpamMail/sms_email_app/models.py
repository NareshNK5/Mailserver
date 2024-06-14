from django.db import models

class tbluser(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    otp = models.CharField(max_length=10,null=True)
    vender_id=models.CharField(max_length=10,null=True)
    product_id=models.CharField(max_length=10,null=True)
    status=models.BooleanField(default=0)
    def __str__(self):
        self.username

class tblemail(models.Model):
    frm = models.ForeignKey(tbluser,on_delete=models.CASCADE,related_name="from_email")
    to = models.ForeignKey(tbluser,on_delete=models.CASCADE,related_name="to_email")
    subject = models.CharField(max_length=50,null=True)
    secretkey = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    message = models.TextField(max_length=500)
    on_delete = models.BooleanField(default=0)
    on_spam = models.BooleanField(default=0)
    def __str__(self):
        self.frm

class tblspam(models.Model):
    user = models.ForeignKey(tbluser,on_delete=models.CASCADE,related_name="user_email",null=True)
    spamword = models.CharField(max_length=50,null=True)
    on_delete = models.BooleanField(default=0)
    def __str__(self):
        self.spamword