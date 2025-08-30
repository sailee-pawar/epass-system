from django.db import models

# Create your models here.

# models.py
from django.db import models

class ConcessionData(models.Model):
	s_name = models.CharField(max_length=250, blank=True, default='')
	b_date = models.DateTimeField(blank=True, null=True)
	age = models.IntegerField(blank=True, null=True)
	gender = models.CharField(max_length=50, blank=True, null=True)
	department = models.CharField(max_length=200, blank=True, null=True)
	address = models.TextField(blank=True, null=True)
	adhar_no = models.CharField(max_length=250, blank=True, null=True)
	phone_no = models.CharField(max_length=50,blank=True, null=True)
	destination = models.CharField(max_length=250, blank=True, null=True)
	duration = models.SmallIntegerField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'concession_data'  # Use your existing table
		managed = False  # Django will not create/migrate this table

	def __str__(self):
		return self.s_name
