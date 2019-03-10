
from django import forms

class UserForm(forms.Form):

    def __init__(self, request):
        super(UserForm, self).__init__(**request)

    def clean(self):
        cleaned_data = {
            'username': self.request.get('email', None),
            'password': self.request.get('password', None),
        }
        for (key, val) in cleaned_data.items():
            if not val:
                raise ValueError('Missing required parameter: ', key)

        contact_data = {
            'email': self.request.get('email', None),
        }
        cleaned_data.update(contact_data)
        return cleaned_data
