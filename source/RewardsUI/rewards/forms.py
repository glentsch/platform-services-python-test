from django import forms

class Rewards_Form(forms.Form):
    email = forms.EmailField(label="E-mail")

    def process(self):
        return self.cleaned_data

