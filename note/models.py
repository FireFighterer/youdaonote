from django.db import models

from userinfo  import models as usermodels
# Create your models here.

class Note(models.Model):
    title=models.CharField("标题",max_length=100,null=False)
    content=models.BinaryField("内容")
    owner=models.ForeignKey(usermodels.User)
    accessory_file=models.CharField("附件",max_length=120,null=True)
    accessory_id=models.IntegerField("附件id",null=True)



