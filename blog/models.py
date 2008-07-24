import datetime
from django.db import models
from django.conf import settings

class BlogPost(models.Model):

	timecreated = models.DateTimeField(auto_now_add=True)
	timemodified = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length = 255)
	slug = models.SlugField(max_length = 255, prepopulate_from = ('title',))
	content = models.TextField()
	allowcomments = models.BooleanField('Allow Comments')
	uid = models.CharField("Permanent Unique ID", max_length=255)

	def __str__(self):
		return self.title

	def get_absolute_url(self):

		# wordpress (pre-2008) created wacky URLs damnit
		timecreated = self.timecreated
		if timecreated < datetime.datetime(2008, 1, 1):
			timecreated += datetime.timedelta(hours = 10)


		return "/articles/%04d/%02d/%02d/%s" % (
			timecreated.year,
			timecreated.month,
			timecreated.day,
			self.slug,
		)

	def get_unique_id(self):
		return self.uid

	class Admin:
		pass

	class Meta:
		ordering = ('-timecreated', 'title')


class BlogPostComment(models.Model):

	blogpost = models.ForeignKey(BlogPost)
	timecreated = models.DateTimeField(auto_now_add=True)
	timemodified = models.DateTimeField(auto_now=True)
	authorname = models.CharField("Authors Name", max_length = 128)
	authoremail = models.EmailField("Authors Email")
	authorurl = models.URLField("Authors URL", blank=True)
	authorip = models.IPAddressField("IP Address", blank=True, null=True)
	authoruseragent = models.CharField("User-Agent", blank=True, null=True, max_length=255)
	content = models.TextField("Comment Content")
	approved = models.BooleanField()

	def __str__(self):
		return "Comment #%s on '%s' by %s" % (self.id, self.blogpost.title, self.authorname)

	def get_absolute_url(self):
		return u"%s#comment%d" % (
			self.blogpost.get_absolute_url(),
			self.id
		)

	def get_unique_id(self):
		return self.get_absolute_url()

	class Admin:
		pass

	class Meta:
		ordering = ('-timecreated', )

