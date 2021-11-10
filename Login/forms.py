from django.forms import Form, PasswordInput, CharField

class LoginForm(Form):
    Username = CharField(max_length=100)
    Password = CharField(max_length=100, widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Login Fields", self.fields)

        self.fields["Username"].widget.attrs.update({"class": "form-control", "placeholder": "Username"})
        self.fields["Password"].widget.attrs.update({"class": "form-control", "placeholder": "Username"})