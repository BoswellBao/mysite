from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    '''
    使用不同的字段类型让Django有依据来对字段进行验证
    '''

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)   # CharField默认对应HTML的<input>,通过widget属性可以改为其他，例如<textarea>

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')