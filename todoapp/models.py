from django.db import models

# Create your models here.
class List(models.Model):
	list_name = models.CharField(max_length=200)
	created_date = models.DateTimeField()
	
	def __str__(self):
		return self.list_name

class Item(models.Model):
	list = models.ForeignKey(List, on_delete=models.CASCADE)
	item_name = models.CharField(max_length=200)
	effort = models.IntegerField(default=10)
	value = models.IntegerField(default=10)

	def score(self):
		return self.value / self.effort

	def __str__(self):
		return self.item_name