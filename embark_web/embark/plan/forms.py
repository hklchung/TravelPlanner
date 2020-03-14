from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class InputForm(forms.Form):
    Your_name = forms.CharField(required = True)
    Your_email = forms.EmailField(label='E-mail')
    Trip_day = forms.ChoiceField(choices=[(1,'Monday'), (2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'),(7, 'Sunday')])
    Trip_start_hour = forms.ChoiceField(choices=[(6,'6'),
                                            (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
                                            (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
                                            (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')])

    Trip_end_hour = forms.ChoiceField(choices=[(8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
                                            (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
                                            (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')])

    Number_of_locations_to_visit = forms.ChoiceField(choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')])
    Total_transportation_hours = forms.ChoiceField(choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')])
    Travel_distance_to_first_location = forms.ChoiceField(choices=[(1,'Not too far'), (2,"I don't mind travelling"), (3,'Take me to the edge of the world!')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(
            'Your_name',
            'Your_email',
            'Trip_day',
            'Trip_start_hour',
            'Trip_end_hour',
            'Number_of_locations_to_visit',
            'Total_transportation_hours',
            'Travel_distance_to_first_location',
            Submit('submit', 'Explore', css_class='btn-sucess')

        )


