from django.db import models
from global_vars import measures, currency_names
# Create your models here.
from django.contrib.auth import get_user_model

class Materials(models.Model):
    material_csr_code = models.CharField(max_length=20, verbose_name='Materialning klassifikatordagi kodi', primary_key=True)
    material_name = models.CharField(max_length=1500, verbose_name='Material nomi')
    material_measure = models.CharField(max_length=25, verbose_name='Material o‘lchov birligi', choices=measures, default='kg')


    def __str__(self):
        return self.material_name

    class Meta:
        db_table = "material_resources"
        ordering = ['material_name', 'material_csr_code']


class Materials_customer(models.Model):
    material_csr_code = models.CharField(max_length=20, verbose_name='Materialning klassifikatordagi kodi', primary_key=True)
    material_name = models.CharField(max_length=1500, verbose_name='Material nomi')
    material_measure = models.CharField(max_length=25, verbose_name='Material o‘lchov birligi', choices=measures, default='kg')
    customer =  models.CharField(max_length=50)
    date =  models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.material_name

    class Meta:
        db_table = "material_resources_customer"
        ordering = ['material_name', 'material_csr_code']


