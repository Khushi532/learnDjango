from django.db import models

# Create your models here.
class sd(models.Model):
    values = models.CharField(max_length=255)  # Store the values as a comma-separated string
    subgroup_size = models.IntegerField()

    def __str__(self):
        return f"DataModel #{self.pk}"
