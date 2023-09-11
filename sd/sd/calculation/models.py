from django.db import models

# Create your models here.
class sd(models.Model):
    values = models.CharField(max_length=255)  # Store the values as a comma-separated string
    subgroup_size = models.IntegerField()
    result = models.FloatField()


