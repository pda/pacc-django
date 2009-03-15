from urllib import urlencode, urlopen

class Akismet:

	def __init__(self, blog, apikey):
		self.blog = blog
		self.apikey = apikey


	def is_spam(self, ip, useragent, author, email, url, content):
		# TODO: log a warning if verification fails
		if not self.__verify():
			return false

		url = 'http://%s.rest.akismet.com/1.1/comment-check' % self.apikey
		postdata = {
			'blog': 'paul.annesley.cc',
			'user_ip': ip,
			'user_agent': useragent,
			'comment_author': author,
			'comment_author_email': email,
			'comment_author_url': url,
			'comment_content': content
			}

		return self.__post(url, postdata) != 'false'

	def __verify(self):
		url = 'http://rest.akismet.com/1.1/verify-key'
		postdata = {'key': self.apikey, 'blog': self.blog}
		return self.__post(url, postdata) == 'valid'

	def __post(self, url, data):
		encoded_data = urlencode(data, True)
		return urlopen(url, encoded_data).read()
