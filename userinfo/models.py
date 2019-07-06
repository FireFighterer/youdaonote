from django.db import models

# Create your models here.

class User(models.Model):
    name=models.CharField("用户名",max_length=50,unique=True)
    password=models.CharField("密码",max_length=50)
    reg_time=models.DateTimeField("注册时间",auto_now_add=True,null=True)
    def __str__(self):
        return "用户名"+self.name