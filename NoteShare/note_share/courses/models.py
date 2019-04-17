import datetime
import os
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.utils.text import slugify

class CourseQuerySet(models.QuerySet):
	def published(self):
		return self.all()

class Course(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_courses')
	title = models.CharField(max_length = 255, null = False, blank = False)
	#professor = models.CharField(null = False, blank = False)
	slug = models.SlugField(max_length=255, unique=True)
	semester = models.CharField(max_length=255, null = False, blank = False) #Restrict values to Fall, Spring, Summer
	year = models.IntegerField(null = False, blank = False)

	objects = CourseQuerySet.as_manager()

	def __str__(self):
		return self.title

	def _get_unique_slug(self):
		slug = slugify(self.slug)
		unique_slug = slug
		num = 1
		while Course.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super().save(*args, **kwargs)

	class Meta:
		verbose_name = "Course"
		verbose_name_plural = "Courses"
		ordering = ["-year"]

class Document(models.Model):
	def path_and_rename(instance, filename):
		upload_to = 'documents/'+datetime.date.today().strftime('%Y')+'/'+datetime.date.today().strftime('%m')+'/'+datetime.date.today().strftime('%d')+'/'
		ext = filename.split('.')[-1]
		# get filename
		if instance.pk:
			filename = '{}.{}'.format(instance.pk, ext)
		else:
			# set filename as random string
			filename = '{}.{}'.format(uuid4().hex, ext)
		# return the whole path to the file
		return os.path.join(upload_to, filename)

	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_documents')
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_documents')
	title = models.CharField(max_length = 255, null = False, blank = False)
	category = models.CharField(max_length = 255, null = False, blank = False)
	document = models.FileField(upload_to=path_and_rename, null=False, blank=False)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
