import os
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import pdawebsite.blog.views, pdawebsite.blog.feedviews

admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/(.*)', admin.site.root),
	(r'^$', pdawebsite.blog.views.frontpage),
	(r'^about$', pdawebsite.blog.views.about),
	(r'^articles$', pdawebsite.blog.views.archive),
	(r'^feed/?$', pdawebsite.blog.feedviews.feed), # legacy wordpress url
	(r'^feed/atom/?$', pdawebsite.blog.feedviews.feed), # legacy wordpress url
	(r'^articles/feed/?$', pdawebsite.blog.feedviews.feed),
	(r'^articles/comments/feed$', pdawebsite.blog.feedviews.comment_feed),
	(r'^articles/\d+/\d+/\d+/(?P<slug>[\w-]+)$', pdawebsite.blog.views.article),
	(r'^articles/\d+/\d+/\d+/(?P<slug>[\w-]+)/comment$', pdawebsite.blog.views.comment),
)

# serve statics during development
if not settings.PRODUCTION:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.OUR_ROOT, 'static')}),
	)

