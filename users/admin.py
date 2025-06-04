from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Gender)
admin.site.register(MaritalStatus)
admin.site.register(Occupation)
admin.site.register(SourceOfWealth)
admin.site.register(IncomeRange)
admin.site.register(Country)
admin.site.register(AddressNature)
admin.site.register(BelongsTo)
# admin.site.register(CommunicationPhone)
# admin.site.register(CommunicationEmail)
admin.site.register(CommunicationDetails)
admin.site.register(Relationship)
admin.site.register(Guardian)
admin.site.register(Nominee)
admin.site.register(BankAccountType)
admin.site.register(PayoutBankAccount)


class NomineeInline(admin.TabularInline):
    model = Nominee
    extra = 1  # how many empty slots to show

class PayoutBankAccountInline(admin.TabularInline):
    model = PayoutBankAccount
    extra = 1

class CommunicationPhoneInline(admin.TabularInline):
    model = CommunicationPhone
    extra = 1

class CommunicationEmailInline(admin.TabularInline):
    model = CommunicationEmail
    extra = 1


class CommunicationDetailsInline(admin.TabularInline):
    model = CommunicationDetails
    extra = 1

@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    inlines = [
        NomineeInline,
        PayoutBankAccountInline,
        CommunicationPhoneInline,
        CommunicationEmailInline,
        CommunicationDetailsInline,
    ]


from django.contrib import admin
from django import forms
from .models import CommunicationEmail, CommunicationPhone

class CommunicationEmailForm(forms.ModelForm):
    class Meta:
        model = CommunicationEmail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # Optional: hide the user field
        if self.request and not self.request.user.is_superuser:
            self.fields['user'].widget = forms.HiddenInput()

class CommunicationEmailAdmin(admin.ModelAdmin):
    form = CommunicationEmailForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def save_model(self, request, obj, form, change):
        if not change or not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class CommunicationPhoneForm(forms.ModelForm):
    class Meta:
        model = CommunicationPhone
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and not self.request.user.is_superuser:
            self.fields['user'].widget = forms.HiddenInput()

class CommunicationPhoneAdmin(admin.ModelAdmin):
    form = CommunicationPhoneForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def save_model(self, request, obj, form, change):
        if not change or not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(CommunicationEmail, CommunicationEmailAdmin)
admin.site.register(CommunicationPhone, CommunicationPhoneAdmin)
