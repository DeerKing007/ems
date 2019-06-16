from django.db import models

# Create your models here.

class User(models.Model):
    user=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    sex=models.CharField(max_length=1)

    class Meta:
        db_table='User'


class Employee(models.Model):
    name=models.CharField(max_length=20)
    salary=models.DecimalField(max_digits=7,decimal_places=2)
    age = models.IntegerField()
    pic = models.ImageField(upload_to='pics')

    class Meta:
        db_table='Employee'

