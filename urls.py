import os
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import blog.views, blog.feedviews

admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/(.*)', admin.site.root),
	(r'^$', blog.views.frontpage),
	(r'^about$', blog.views.about),
	(r'^articles$', blog.views.archive),
	(r'^feed/?$', blog.feedviews.feed), # legacy wordpress url
	(r'^feed/atom/?$', blog.feedviews.feed), # legacy wordpress url
	(r'^articles/feed/?$', blog.feedviews.feed),
	(r'^articles/comments/feed$', blog.feedviews.comment_feed),
	(r'^articles/\d+/\d+/\d+/(?P<slug>[\w-]+)$', blog.views.article),
	(r'^articles/\d+/\d+/\d+/(?P<slug>[\w-]+)/comment$', blog.views.comment),
)

# serve statics during development
if not settings.PRODUCTION:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_ROOT, 'static')}),
		(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_ROOT, 'assets')}),
	)

