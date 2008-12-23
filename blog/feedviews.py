from django.utils.feedgenerator import Atom1Feed
from django.http import HttpResponse

def feed(request):

	# everyone but feedburner and feedvalidator should go via feedburner
	if __redirectFeed(request):
		return HttpResponseRedirect('http://feeds.feedburner.com/paulannesley')

	feed = Atom1Feed(
		title = u"paul.annesley.cc",
		link = request.build_absolute_uri('/'),
		description = u"Paul Annesley on all things web",
		subtitle = u"Paul Annesley on all things web",
		language = u"en",
		author_name = u"Paul Annesley",
		author_link = u"http://paul.annesley.cc/",
		feed_url = request.build_absolute_uri()
	)

	posts = BlogPost.objects.all()

	for post in posts:
		feed.add_item(
			unique_id = post.get_unique_id(),
			link = request.build_absolute_uri(post.get_absolute_url()),
			title = post.title,
			description = post.content,
			pubdate = post.timecreated,
			# TODO: move these into the BlogPost model
			author_name = u"Paul Annesley",
			author_link = request.build_absolute_uri('/')
		)

	return HttpResponse(
		feed.writeString('utf-8'),
		'application/atom+xml; charset=utf-8'
		# let FireFox view source properly during development
		#'text/xml; charset=utf-8'
	)


def comment_feed(request):

	feed = Atom1Feed(
		title = u"paul.annesley.cc comments",
		link = request.build_absolute_uri('/'),
		description = u"All comments at paul.annesley.cc",
		language = u"en",
		author_name = u"Paul Annesley",
		author_link = u"http://paul.annesley.cc/",
		feed_url = request.build_absolute_uri()
	)

	comments = BlogPostComment.objects.filter(approved=1)

	for comment in comments:
		feed.add_item(
			unique_id = comment.get_unique_id(),
			link = request.build_absolute_uri(comment.get_absolute_url()),
			title = comment,
			description = comment.content,
			pubdate = comment.timecreated,
			author_name = comment.authorname,
			author_link = comment.authorurl
		)

	return HttpResponse(
		feed.writeString('utf-8'),
		'application/atom+xml; charset=utf-8'
		# let FireFox view source properly during development
		#'text/xml; charset=utf-8'
	)

def __redirectFeed(request):
	return not re.search(
		r'(feedburner|feedvalidator)',
		request.META['HTTP_USER_AGENT'], re.I
	)

