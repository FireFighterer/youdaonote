from django import forms

class RegForm(forms.Form):
    username=forms.CharField(label="用户名:",initial="无名氏",required=False)
    password=forms.CharField(label="密码:",widget=forms.PasswordInput)
    password2=forms.CharField(label="密码确认:")

    def clean_username(self):
        username=self.cleaned_data['username']
        if len(username)<6:
            raise forms.ValidationError("用户名太短")
        return username
    def clean(self):
        pwd1=self.cleaned_data['password']
        pwd2=self.cleaned_data['password2']

        if pwd1!=pwd2:
            raise forms.ValidationError("两次密码不一致")
        return self.cleaned_data
