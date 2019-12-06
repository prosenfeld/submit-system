from django import forms
from .models import *

class SubmitFormForm(forms.Form):
    conf = forms.CharField(widget=forms.HiddenInput())
    task = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, submit_form, *args, **kwargs):
        super(SubmitFormForm, self).__init__(*args, **kwargs)
        fields = SubmitFormField.objects.filter(submit_form=submit_form).order_by('sequence')
        for field in fields:
            if field.question_type == SubmitFormField.QuestionType.TEXT:
                self.fields[field.meta_key] = forms.CharField(label=field.question)

            elif field.question_type == SubmitFormField.QuestionType.NUMBER:
                self.fields[field.meta_key] = forms.IntegerField(label=field.question)

            elif field.question_type == SubmitFormField.QuestionType.RADIO:
                choices = list(map(lambda x: (x,x), field.choices.split(',')))
                self.fields[field.meta_key] = forms.ChoiceField(label=field.question, choices=choices)

            elif field.question_type == SubmitFormField.QuestionType.CHECKBOX:
                choices = list(map(lambda x: (x,x), field.choices.split(',')))
                self.fields[field.meta_key] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                        choices=choices)

            elif field.question_type == SubmitFormField.QuestionType.EMAIL:
                self.fields[field.meta_key] = forms.EmailField(label=field.question)

            elif field.question_type == SubmitFormField.QuestionType.COMMENT:
                self.fields[field.meta_key] = forms.CharField(label=field.question,
                                                              widget=forms.Textarea)

            elif field.question_type == SubmitFormField.QuestionType.RUNTAG:
                self.fields[field.meta_key] = forms.CharField(label=field.question,
                                                              validators=[check_runtag])

        if 'has_file' in kwargs and kwargs['has_file'] == True:
            self.fields['run'] = forms.FileField(label="Submission file")

    def check_runtag(value):
        pass


                
            
