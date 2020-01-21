from django.db import models


# Create your models here.
class Batch(models.Model):
    id = models.IntegerField(primary_key=True)
    batch_name = models.CharField(max_length=100)


class Students(models.Model):
    first_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, primary_key=True)
    email_id = models.CharField(max_length=50)
    batch_name = models.ForeignKey(Batch, on_delete=models.CASCADE)


