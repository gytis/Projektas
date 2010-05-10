
from django import forms


class LoginForm(forms.Form):
    Vartotojo_vardas = forms.CharField(max_length=30)
    Slaptazodis = forms.CharField(
                    widget = forms.PasswordInput(render_value=False))


class RegistrationForm(forms.Form):
    Vartotojo_vardas = forms.CharField(max_length=30)
    Vardas = forms.CharField(max_length=30)
    Pavarde = forms.CharField(max_length=30)
    Gimtadienis = forms.DateField(required=False)
    El_pastas = forms.EmailField(max_length=75)
    Slaptazodis = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))        
    Pakartoti_slaptazodi = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))    
    Nuotrauka = forms.ImageField(required=False)    
    
    Salis = forms.CharField(max_length=30, required=False)
    Miestas = forms.CharField(max_length=30, required=False)
    Adresas = forms.CharField(max_length=40, required=False)    
    
    Vidurine_mokykla = forms.CharField(max_length=30, required=False)
    Vid_mokyklos_baigimo_metai = forms.IntegerField(required=False, 
                                                    min_value=1900, 
                                                    max_value=2020)    
    Aukstoji_mokykla = forms.CharField(max_length=30, required=False)
    Aukst_mokyklos_baigimo_metai = forms.IntegerField(required=False,
                                                        min_value=1900,
                                                        max_value=2020)


class LaiskoForma(forms.Form):
    Gavejo_vartotojo_vardas = forms.CharField(max_length=30)
    Antraste = forms.CharField(max_length=100, required=False)
    Tekstas = forms.CharField(max_length=1000, widget=forms.Textarea)


class DuomenuKeitimoForma(forms.Form):
    Vardas = forms.CharField(max_length=30)
    Pavarde = forms.CharField(max_length=30)
    Gimtadienis = forms.DateField(required=False)
    El_pastas = forms.EmailField(max_length=75)
    Slaptazodis = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))        
    Pakartoti_slaptazodi = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))   
    
    Salis = forms.CharField(max_length=30, required=False)
    Miestas = forms.CharField(max_length=30, required=False)
    Adresas = forms.CharField(max_length=40, required=False)    
    
    Vidurine_mokykla = forms.CharField(max_length=30, required=False)
    Vid_mokyklos_baigimo_metai = forms.IntegerField(required=False, 
                                                    min_value=1900, 
                                                    max_value=2020)    
    Aukstoji_mokykla = forms.CharField(max_length=30, required=False)
    Aukst_mokyklos_baigimo_metai = forms.IntegerField(required=False,
                                                        min_value=1900,
                                                        max_value=2020)


class SlaptazodzioKeitimoForma(forms.Form):
    Senas_slaptazodis = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))
    Naujas_slaptazodis = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))
    Pakartoti_nauja_slaptazodi = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))


class PagrFotoKeitimoForma(forms.Form):
    Nuotrauka = forms.ImageField(required=False)
    Slaptazodis = forms.CharField(
                    widget=forms.PasswordInput(render_value=False))

