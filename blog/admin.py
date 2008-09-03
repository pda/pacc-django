from django.contrib import admin
from pdawebsite.blog.models import *

class BlogPostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(BlogPost)
admin.site.register(BlogPostComment)
