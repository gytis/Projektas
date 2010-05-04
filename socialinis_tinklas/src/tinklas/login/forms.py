
# login forms

from django import forms

class LoginForm(forms.Form):
    Vartotojo_vardas = forms.CharField(max_length = 30)
    Slaptazodis = forms.CharField(
        widget = forms.PasswordInput(render_value = False))