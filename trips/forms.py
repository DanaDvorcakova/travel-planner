from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm
)

from .models import (
    Profile,
    Trip,
    ItineraryItem,
    SavedPlace,
    Review
)


# =========================
# PASSWORD RESET
# =========================
class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email address",
            "autocomplete": "email"
        })
    )

# =========================
# PROFILE FORM
# =========================
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'travel_style']


        
# =========================
# TRIP FORM
# =========================
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ['user']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    # VALIDATION: prevent invalid date ranges
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end:
            if end < start:
                self.add_error(
                    'end_date',
                    "End date must be after start date."
                )

        return cleaned_data


# =========================
# SIGNUP FORM
# =========================
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# =========================
# LOGIN FORM
# =========================
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# =========================
# ITINERARY FORM
# =========================
class ItineraryItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)
        super().__init__(*args, **kwargs)

         # 🔥 ADD THIS BLOCK
        if self.trip:
            self.fields['date'].widget.attrs.update({
                'min': self.trip.start_date,
                'max': self.trip.end_date
            })

    class Meta:
        model = ItineraryItem
        fields = ['title', 'location', 'date', 'time', 'notes']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            # 📅 Calendar picker
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            # 🕒 Time picker
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),

            # 📝 Notes
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def clean_date(self):
        date = self.cleaned_data['date']

        if self.trip and (date < self.trip.start_date or date > self.trip.end_date):
            raise forms.ValidationError(
                "Date must be within trip dates."
            )

        return date


# =========================
# SAVED PLACE FORM
# =========================
class SavedPlaceForm(forms.ModelForm):
    class Meta:
        model = SavedPlace
        fields = ['name', 'location', 'description', 'image']


# =========================
# REVIEW FORM
# =========================
RATING_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[('', 'Select rating...')] + RATING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select w-auto',
        }),
        label='Rating'
    )

    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make comment optional
        self.fields['comment'].required = False