from django import forms

class QueryForm(forms.Form):
    query_name = forms.CharField(label="Query", max_length=50)