from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class InputForm(forms.Form):
    name = forms.CharField(required = True)
    email = forms.EmailField(label='E-mail')
    Start_Hour = forms.ChoiceField(choices=[(0,'0'), (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'),
                                            (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
                                            (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
                                            (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')])

    End_Hour = forms.ChoiceField(choices=[(0, '0'), (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'),
                                            (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
                                            (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
                                            (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')])

    loc_count = forms.ChoiceField(choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')])
    trv_time = forms.ChoiceField(choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')])
    trv_dist = forms.ChoiceField(choices=[(1,'1'), (2,'2'), (3,'3')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(
            'name',
            'email',
            'Start_Hour',
            'End_Hour',
            'loc_count',
            'trv_time',
            'trv_dist',
            Submit('submit', 'Explore', css_class='btn-sucess')

        )


