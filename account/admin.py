from django.contrib import admin
from .models import Account, EmailConfirmation, SignupCodeResult, SignupCode, EmailAddress, AccountDeletion, AnonymousAccount

class AccountAdmin(admin.ModelAdmin):
    queryset = Account.objects.all()
    list_display = ('phone_number', 'name', 'language', 'netid', 'theme', 'original_id', 'user', 'orcid', 'timezone', 'nickname', 'id', 'initials',)

class EmailConfirmationAdmin(admin.ModelAdmin):
    queryset = EmailConfirmation.objects.all()
    list_display = ('created', 'objects', 'key', 'email_address', 'id', 'sent',)

class SignupCodeResultAdmin(admin.ModelAdmin):
    queryset = SignupCodeResult.objects.all()
    list_display = ('timestamp', 'signup_code', 'user', 'id',)

class SignupCodeAdmin(admin.ModelAdmin):
    queryset = SignupCode.objects.all()
    list_display = ('code', 'created', 'notes', 'expiry', 'use_count', 'id', 'max_uses', 'inviter', 'email', 'sent',)

class EmailAddressAdmin(admin.ModelAdmin):
    queryset = EmailAddress.objects.all()
    list_display = ('verified', 'primary', 'email', 'objects', 'user', 'id',)

class AccountDeletionAdmin(admin.ModelAdmin):
    queryset = AccountDeletion.objects.all()
    list_display = ('id', 'date_requested', 'user', 'date_expunged', 'email',)

admin.site.register(Account, AccountAdmin)
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(SignupCodeResult, SignupCodeResultAdmin)
admin.site.register(SignupCode, SignupCodeAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
admin.site.register(AccountDeletion, AccountDeletionAdmin)
