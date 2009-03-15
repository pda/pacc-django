import os
import feedparser
import random
import urllib
from forms import CommentForm
from urlparse import urlparse
from datetime import datetime
from calendar import timegm
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from blog.models import *
import secrets

def article(request, slug):

	#post = BlogPost.objects.get(slug=slug)
	post = get_object_or_404(BlogPost, slug=slug)

	if request.path != post.get_absolute_url():
		raise Http404('Article not found')

	comments = post.blogpostcomment_set.order_by('timecreated').filter(approved=1)
	commentCount = len(comments)
	hasComments = commentCount > 0
	title = post.title

	form = CommentForm()

	# TODO: reverse lookup from urls.py
	commenturl = request.path + '/comment'

	feeds = __getFeeds((
		(
			'bookmarks',
			'http://del.icio.us/rss/paul.annesley',
			6,
			10
		),
	))

	return render_to_response('article.html', locals())


def comment(request, slug):

	post = BlogPost.objects.get(slug=slug)

	if not post.allowcomments:
		raise PermissionDenied('This post does not allow comments.')

	if request.method == 'POST':

		form = CommentForm(request.POST)

		if form.is_valid():

			data = form.cleaned_data

			comment = BlogPostComment()
			comment.blogpost = post
			comment.authorname = data['name']
			comment.authoremail = data['email']
			comment.authorurl = data['url']
			comment.content = data['content']
			comment.approved = not __isCommentSpam(comment)
			comment.save()

			return HttpResponseRedirect(post.get_absolute_url())

		else:
			# TODO: handle this
			assert(False)

	else:
		raise PermissionDenied('Method not supported')


def frontpage(request):
	feeds = __getAllFeeds()
	posts = BlogPost.objects.all()[:5]
	return render_to_response('frontpage.html', locals())


def archive(request):
	# TODO: filter and sort posts
	posts = BlogPost.objects.all()
	feeds = __getAllFeeds()
	title = u'Archive'
	return render_to_response('archive.html', locals())

def about(request):
	feeds = __getAllFeeds()
	title = u'About Paul Annesley and This Site'
	return render_to_response('about.html', locals())

###################
# helper functions

def __getAllFeeds():

	feeds = __getFeeds((
		(
			'announcements',
			'http://www.google.com/reader/public/atom/user/01919883411298058200/label/annoucement',
			10,
			20
		),
		(
			'authoredelsewhere',
			'http://www.google.com/reader/public/atom/user/01919883411298058200/label/authored',
			10,
			60
		),
		(
			'commented',
			'http://www.google.com/reader/public/atom/user/01919883411298058200/label/commented',
			10,
			20
		),
		(
			'bookmarks',
			'http://del.icio.us/rss/paul.annesley',
			6,
			10
		),
	))

	# add a sitename attribute to each commented entry
	for entry in feeds['commented']['entries']:
		# python 2.4 doesn't support attribute access to urlparse result
		#entry['sitename'] = urlparse(entry['link']).hostname
		entry['sitename'] = urlparse(entry['link'])[1]

	# add a django-compatible date to each announcement
	for entry in feeds['announcements']['entries']:
		entry['date'] = datetime.datetime.utcfromtimestamp(timegm(entry['date_parsed']))

	return feeds


def __randomizeCacheMinutes(minutes):
	'''Randomizes cache expiry time to help prevent all objects expiring at once'''
	seconds = minutes * 60
	return random.randint(seconds, seconds * 2)


def __getFeeds(feedinfo):
	'''Takes a list of lists describing feed information, and
	returns a dictionary of feedparser feeds. Uses Django caching.
	Format: ((name, uri, limit, cacheMinutes), ...)'''

	feeds = {}

	for (name, uri, limit, cacheMinutes) in feedinfo:

		# try cache
		cacheKey = 'feed-' + name
		feeds[name] = cache.get(cacheKey)

		# check for cache miss
		if not feeds[name]:

			# grab and parse feed
			feed = feedparser.parse(uri)

			# reduce entries to specified limit
			if len(feed.entries) > limit:
				feed.entries = feed.entries[0:limit]

			# add to feeds, cache for later
			feeds[name] = feed
			cache.set(cacheKey, feed, __randomizeCacheMinutes(cacheMinutes))

	return feeds

def __isCommentSpam(comment):

	# most or all of this should be defined elsewhere.
	# also, all this akismet stuff should be encapsulated and error handled.
	# meh.
	apikey = secrets.AKISMET_API_KEY
	url_verify = 'http://rest.akismet.com/1.1/verify-key'
	url_check = 'http://%s.rest.akismet.com/1.1/comment-check' % apikey
	postdata_verify = urllib.urlencode({'key': apikey, 'blog': 'http://paul.annesley.cc/'}, True)

	if urllib.urlopen(url_verify, postdata_verify).read() == 'valid':

		postdata_comment = urllib.urlencode({
			'blog': 'paul.annesley.cc',
			'user_ip': comment.authorip,
			'user_agent': comment.authoruseragent,
			'comment_author': comment.authorname,
			'comment_author_email': comment.authoremail,
			'comment_author_url': comment.authorurl,
			'comment_content': comment.content
		}, True)

		return urllib.urlopen(url_check, postdata_comment).read() != 'false'

