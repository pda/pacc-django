import os
from django.conf.urls.defaults import *
from django.conf import settings
import pdawebsite.blog.views

urlpatterns = patterns('',
	(r'^admin/', include('django.contrib.admin.urls')),
	(r'^$', pdawebsite.blog.views.frontpage),
	(r'^articles$', pdawebsite.blog.views.archive),
	(r'^feed/?$', pdawebsite.blog.views.feed), # legacy wordpress url
	(r'^feed/atom/?$', pdawebsite.blog.views.feed), # legacy wordpress url
	(r'^articles/feed/?$', pdawebsite.blog.views.feed),
	(r'^articles/comments/feed$', pdawebsite.blog.views.comment_feed),
	(r'^articles/\d+/\d+/\d+/(?P<slug>[\w-]+)$', pdawebsite.blog.views.article),
	(r'^articles/\d+/\d+/\d+/(?P<slug>[\w-]+)/comment$', pdawebsite.blog.views.comment),
)

# serve statics during development
if not settings.PRODUCTION:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.OUR_ROOT, 'static')}),
	)

