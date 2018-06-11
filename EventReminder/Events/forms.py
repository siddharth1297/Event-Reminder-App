from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=10, required=True)
    password = forms.CharField(label='password', max_length=8, widget=forms.PasswordInput, required=True)


class SignupForm(forms.Form):
    username = forms.CharField(label='username', max_length=10, required=True)
    password = forms.CharField(label='password', max_length=8, widget=forms.PasswordInput, required=True)
    email    = forms.EmailField(label='Email', required=True)
    phone = forms.IntegerField(required=True)
    gender_choice = [('M', 'male'),
                     ('F', 'female')]
    gender = forms.ChoiceField(label='Gender', choices=gender_choice, widget=forms.RadioSelect(), required=True)


class NewEvent(forms.Form):
    events = forms.CharField(label='Event Name', max_length=100, required=True)
    event_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Date', required=True)
    event_time =forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}), label='Time', required=True)
    sms_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Reminder Date', required=True)
    sms_time =forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}), label='Reminder Time', required=True)

