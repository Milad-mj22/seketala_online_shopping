from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'phone', 'email', 'order_id', 'subject', 'message']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 3:
            raise forms.ValidationError('نام باید حداقل ۳ کاراکتر باشد.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise forms.ValidationError('شماره تماس معتبر نیست (۱۰ تا ۱۵ رقم).')
        return phone

    def clean_message(self):
        msg = self.cleaned_data.get('message', '').strip()
        if len(msg) < 5:
            raise forms.ValidationError('متن شکایت باید حداقل ۵ کاراکتر باشد.')
        if len(msg) > 5000:
            raise forms.ValidationError('متن شکایت خیلی طولانی است (حداکثر ۵۰۰۰ کاراکتر).')
        return msg