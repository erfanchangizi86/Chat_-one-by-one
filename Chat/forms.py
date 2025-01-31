from django import forms

from Chat.models import profile
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer'}),
        min_length=4,
        max_length=20,
        error_messages={
            'min_length': 'رمز عبور باید حداقل ۴ کاراکتر باشد.',
            'max_length': 'رمز عبور نمی‌تواند بیشتر از ۲۰ کاراکتر باشد.',
        }
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer'}),
            'email': forms.EmailInput(attrs={'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer'}),
            'username': forms.TextInput(attrs={'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer'}),
        }
        labels = {
            "username": "نام کاربری",
            "email": "ایمیل",
            "password": "رمز عبور",
        }

        # پیام‌های خطای فارسی
        error_messages = {
            "username": {
                "required": "وارد کردن نام کاربری الزامی است.",
                "max_length": "نام کاربری نمی‌تواند بیشتر از 150 کاراکتر باشد.",
                "unique": "این نام کاربری قبلاً ثبت شده است. لطفاً یک نام کاربری دیگر انتخاب کنید.",
            },
            "email": {
                "required": "وارد کردن ایمیل الزامی است.",
                "invalid": "لطفاً یک ایمیل معتبر وارد کنید.",
                "unique": "این ایمیل قبلاً ثبت شده است. لطفاً یک ایمیل دیگر وارد کنید.",
            },
            "password": {
                "min_length": 'رمز عبور باید حداقل ۴ کاراکتر باشد.',
                "required": "رمز عبور الزامی است.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data.get("confirm_password")

        # بررسی تطابق رمز عبور و تکرار آن
        if password != password_confirm:
            raise forms.ValidationError("رمز عبور و تکرار آن مطابقت ندارند.")
        return password_confirm

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("confirm_password")

        # بررسی تطابق رمز عبور و تکرار آن
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("رمز عبور و تکرار آن مطابقت ندارند.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # هش کردن رمز عبور
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



# forms.py

class Test_form(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block w-full p-3 border border-gray-300 rounded-md'}),
                                       min_length=4, max_length=20,label=' تکرار رمز عبور' ,error_messages={
            'min_length': 'رمز عبور باید حداقل ۴ کاراکتر باشد.',
            'max_length': 'رمز عبور نمی‌تواند بیشتر از ۲۰ کاراکتر باشد.',
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'block w-full p-3 border border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'block w-full p-3 border border-gray-300 rounded-md'}),
            'username': forms.TextInput(attrs={'class': 'block w-full p-3 border border-gray-300 rounded-md'}),
        }

        labels = {
            'username': 'نام کاربری',
            'email': 'ایمیل',
            'password': 'رمز عبور',
        }
        error_messages = {
            "username": {
                "required": "وارد کردن نام کاربری الزامی است.",
                "max_length": "نام کاربری نمی‌تواند بیشتر از 150 کاراکتر باشد.",
                "unique": "این نام کاربری قبلاً ثبت شده است. لطفاً یک نام کاربری دیگر انتخاب کنید.",
            },
            "email": {
                "required": "وارد کردن ایمیل الزامی است.",
                "invalid": "لطفاً یک ایمیل معتبر وارد کنید.",
                "unique": "این ایمیل قبلاً ثبت شده است. لطفاً یک ایمیل دیگر وارد کنید.",
            },
            "password": {
                "min_length": 'رمز عبور باید حداقل ۴ کاراکتر باشد.',
                "required": "رمز عبور الزامی است.",
            },
        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data.get("confirm_password")

        if password != password_confirm:
            raise forms.ValidationError("رمز عبور و تکرار آن مطابقت ندارند.")
        return password_confirm

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("confirm_password")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("رمز عبور و تکرار آن مطابقت ندارند.")

        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        # هش کردن رمز عبور
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class edit_profile_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username':forms.TextInput(attrs={'class':'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-500 transition-all duration-200'}),
            'first_name': forms.TextInput(attrs={'class':'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-500 transition-all duration-200'}),
            'last_name': forms.TextInput(attrs={'class':'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-500 transition-all duration-200'})
        }
        labels = {
            'username':'نام کاربری',
            "first_name":"نام",
            'last_name':"نام خانوادگی"
        }
        error_messages = {
            "username": {
                "required": "وارد کردن نام کاربری الزامی است.",
                "max_length": "نام کاربری نمی‌تواند بیشتر از 150 کاراکتر باشد.",
                "unique": "این نام کاربری قبلاً ثبت شده است. لطفاً یک نام کاربری دیگر انتخاب کنید.",
            },
            "first_name": {
                "required": "وارد کردن نام کاربری الزامی است.",
                "max_length": "نام کاربری نمی‌تواند بیشتر از 150 کاراکتر باشد.",
                "unique": "این نام کاربری قبلاً ثبت شده است. لطفاً یک نام کاربری دیگر انتخاب کنید.",
            },
            "last_name": {
                "required": "وارد کردن نام کاربری الزامی است.",
                "max_length": "نام کاربری نمی‌تواند بیشتر از 150 کاراکتر باشد.",
                "unique": "این نام کاربری قبلاً ثبت شده است. لطفاً یک نام کاربری دیگر انتخاب کنید.",
            },


        }

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = profile
#         fields = ['avatar']
#         widgets = {
#             'avatar':forms.FileInput(attrs={'class': 'w-full p-2 border rounded-lg'})
#         }

class ProfileForm(forms.Form):
    avatar = forms.ImageField(label="انتخاب تصویر", required=True, widget=forms.ClearableFileInput(attrs={'class':  "block w-72 text-base text-gray-900 border border-gray-400 rounded-lg cursor-pointer bg-gray-100 \
                      dark:text-gray-300 focus:outline-none dark:bg-gray-700 dark:border-gray-500 dark:placeholder-gray-400 \
                      p-3 shadow-sm"}))
