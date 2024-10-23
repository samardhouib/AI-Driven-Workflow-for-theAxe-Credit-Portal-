from django import forms

class InstructionForm(forms.Form):
    instruction = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your requirements here...'}), label='', required=False)
    excel_file = forms.FileField(label='Upload Excel File', required=False)
    text_file = forms.FileField(label='Upload Text File', required=False)
