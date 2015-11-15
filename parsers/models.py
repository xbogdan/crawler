from django.db import models

# Create your models here.
class OnedenCategory(models.Model):
	name = models.CharField(max_length=100)


class OnedenAliment(models.Model):
	category = models.ForeignKey(OnedenCategory, null=False, blank=False)
	name = models.CharField(max_length=250)
	calories = models.DecimalField(max_digits=7, decimal_places=2)
	proteins = models.DecimalField(max_digits=7, decimal_places=2)
	fats = models.DecimalField(max_digits=7, decimal_places=2)
	carbohydrates = models.DecimalField(max_digits=7, decimal_places=2)
	fibres = models.DecimalField(max_digits=7, decimal_places=2)
	unit_quantity = models.DecimalField(max_digits=7, decimal_places=2)
	additional = models.TextField()

	class Meta:
		unique_together = (('category', 'name'),)

