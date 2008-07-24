from django import newforms as forms

class CommentForm(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()
	url = forms.URLField(required=False)
	content = forms.CharField(widget=forms.widgets.Textarea())
