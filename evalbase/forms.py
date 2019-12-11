from django import forms
from .models import *

class SubmitFormForm(forms.Form):
    conf = forms.CharField(widget=forms.HiddenInput())
    task = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, context, *args, **kwargs):
        super(SubmitFormForm, self).__init__(*args, **kwargs)

        # Set up standard fields
        self.fields['user'] = forms.CharField(label='User name',
                                              widget=forms.TextInput(attrs={'value': context['user'].username,
                                                                            'readonly': 'readonly',
                                                                            'class': 'form-control-plaintext'}))
        self.fields['email'] = forms.EmailField(label='Email',
                                                widget=forms.EmailInput(attrs={'value': context['user'].email,
                                                                               'readonly': 'readonly',
                                                                               'class': 'form-control-plaintext'}))
        org_choices = list(map(lambda x: (x.shortname, x.longname), context['orgs']))
        self.fields['org'] = forms.ChoiceField(label='Organization', choices=org_choices)

        self.fields['runfile'] = forms.FileField(label='Submission file')
        
        # Set up custom fields
        fields = SubmitFormField.objects.filter(submit_form=context['form']).order_by('sequence')
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

            elif field.question_type == SubmitFormField.QuestionType.YESNO:
                self.fields[field.meta_key] = forms.ChoiceField(label=field.question,
                                                                choices=[('yes', 'Yes'), ('no', 'No')])

    def check_runtag(value):
        pass


                
            
