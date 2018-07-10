from django import forms

class Order_Form(forms.Form):
    email = forms.EmailField(label="E-mail")
    total = forms.FloatField(label="Order Total")

    def process(self):
        return self.cleaned_data

