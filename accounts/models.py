from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class ConcessionData(models.Model):
	user_id = models.IntegerField(blank=True, null=True)  # just maps to the int column
	
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
	is_active = models.SmallIntegerField(blank=True, null=True)
	status = models.CharField(max_length=50, blank=True, null=True)
	email_id = models.CharField(max_length=150, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class_type = models.CharField(
		max_length=20,
		choices=[("I Class", "I Class"), ("II Class", "II Class")],
		default="II Class"   # ✅ default so migration won’t fail
	)
	class Meta:
		db_table = 'concession_data'  # Use your existing table
		managed = False  # Django will not create/migrate this table

	def __str__(self):
		return self.s_name

class User(AbstractUser):
	ROLE_CHOICES = (
		('student', 'Student'),
		('transporter', 'Transporter'),
		('admin', 'College Admin'),
	)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
	clg_id = models.IntegerField(default=0,null=True)

class VerifiedPassData(models.Model):
	concession_id = models.IntegerField(default=0)
	user_id = models.IntegerField(default=0)
	s_name = models.CharField(max_length=250, blank=True, null=True)
	b_date = models.DateTimeField(blank=True, null=True)
	age = models.IntegerField(blank=True, null=True)
	gender = models.CharField(max_length=50, blank=True, null=True)
	destination = models.CharField(max_length=250, blank=True, null=True)
	duration = models.SmallIntegerField(blank=True, null=True)
	is_active = models.IntegerField(blank=True, null=True)
	status = models.CharField(max_length=50, blank=True, null=True)
	class_type = models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	college_id = models.IntegerField(default=0)
	updated_at = models.DateTimeField(auto_now=False)

	class Meta:
		db_table = "verified_pass_data"
		managed = False
	
class CollegeMetaData(models.Model):
	clg_id = models.AutoField(primary_key=True)
	college_name = models.CharField(max_length=300, default="")
	address1 = models.CharField(max_length=300, blank=True, default="")
	address2 = models.CharField(max_length=300, blank=True, default="")
	phone_no1 = models.CharField(max_length=12, blank=True, default="0")
	phone_no2 = models.CharField(max_length=300, blank=True, default="")
	default_source = models.CharField(max_length=100, blank=True, default="")
	email_id = models.CharField(max_length=250, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	# updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "college_meta_data"
		managed = False
		
	def __str__(self):
		return self.college_name
