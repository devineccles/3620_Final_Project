from django import forms

from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
    base_widget_attrs = {
        'class': 'form-control w-100',
    }
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                **base_widget_attrs,
                'placeholder': 'Select a date',
                'type': 'date',

            }
        )
    )

    category = forms.ChoiceField(
        choices=Expense.CATEGORIES,
        widget=forms.Select(
            attrs={
                **base_widget_attrs,
                'style': 'appearance: auto;',
            }
        )
    )

    amount = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                **base_widget_attrs,
                'placeholder': 'Enter amount',
            }
        )
    )

    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                **base_widget_attrs,
                'placeholder': 'Enter description',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'description']

        def save(self, commit=True):
            expense = super().save(commit=False)
            if self.user:
                expense.user = self.user
            if commit:
                expense.save()
            return expense


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['contact_name', 'contact_email', 'contact_message']