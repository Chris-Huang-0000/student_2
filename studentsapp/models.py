from django.db import models

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=20,null=False)
    sex = models.CharField(max_length=2,default='M',null=False)
    birthday = models.DateField(null=False)
    email = models.EmailField(max_length=100,blank=True,default='')
    phone = models.CharField(max_length=50,blank=True,default='')
    address = models.CharField(max_length=255,blank=True,default='')

    def __str__(self):
        return self.name
    