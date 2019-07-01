from django.db import models

# Create your models here.

class User(models.Model):
    name=models.CharField("用户名",max_length=50,unique=True)
    password=models.CharField("密码",max_length=50)
    def __str__(self):
        return "用户名"+self.name