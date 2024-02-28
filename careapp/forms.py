from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.IntegerField()
    address = forms.CharField(max_length=300)
    password = forms.CharField(max_length=50)
    confirm_password = forms.CharField(max_length=50)


class adminform(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20)    

    


