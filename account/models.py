from __future__ import unicode_literals

import datetime
import operator

try:
    from urllib.parse import urlencode
except ImportError:  # python 2
    from urllib import urlencode

from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone, translation, six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site

import pytz

from account import signals
from account.conf import settings
from account.fields import TimeZoneField
from account.hooks import hookset
from account.managers import EmailAddressManager, EmailConfirmationManager
from account.signals import signup_code_sent, signup_code_used

from directory.models import Organisation




@python_2_unicode_compatible
class Account(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="account", verbose_name=_("user"))
    timezone = TimeZoneField(_("timezone"))
    language = models.CharField(
        _("language"),
        max_length=10,
        choices=settings.ACCOUNT_LANGUAGES,
        default=settings.LANGUAGE_CODE
    )
    theme = models.CharField(max_length=255, default='default')

    name = models.CharField(max_length=255, default='', help_text="The full name of the person")
    initials = models.CharField(max_length=16, default='', help_text="Their first and middle initials (PubMed format)")
    nickname = models.CharField(max_length=255, blank=True, help_text="Their preferred name, if applicable. Many non-American students choose to go by a different name.")
    netid = models.CharField(max_length=32, blank=True, help_text="Their netid, if available")
    phone_number = models.CharField(max_length=16, blank=True, help_text="A phone number which they will continue to be reachable at (i.e. not an office phone #)")

    # tags = tagulous.models.TagField(PersonTag, blank=True, help_text="Tags allow us to group users easily and see in what way they were involved with the CPT's research")

    orcid = models.CharField(max_length=32, blank=True, help_text="See <a href='https://orcid.org' target='_blank'>https://orcid.org</a>")
    orgs = models.ManyToManyField(Organisation, blank=True, help_text="Organisations the person is associated with. Please add an appropriate organisation if there is not one available")
    original_id = models.CharField(max_length=4, blank=True, help_text="Internal use only")

    def emails(self):
        return self.user.emailaddress_set.all()

    def primaryEmail(self):
        try:
            return self.user.emailaddress_set.get(primary=True)
        except:
            return None

    @classmethod
    def for_request(cls, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated():
            try:
                return Account._default_manager.get(user=user)
            except Account.DoesNotExist:
                pass
        return AnonymousAccount(request)

    @classmethod
    def create(cls, request=None, **kwargs):
        create_email = kwargs.pop("create_email", True)
        confirm_email = kwargs.pop("confirm_email", None)
        account = cls(**kwargs)
        if "language" not in kwargs:
            if request is None:
                account.language = settings.LANGUAGE_CODE
            else:
                account.language = translation.get_language_from_request(request, check_path=True)
        account.save()
        if create_email and account.user.email:
            kwargs = {"primary": True}
            if confirm_email is not None:
                kwargs["confirm"] = confirm_email
            EmailAddress.objects.add_email(account.user, account.user.email, **kwargs)
        return account

    def __str__(self):
        return str(self.user)

    def now(self):
        """
        Returns a timezone aware datetime localized to the account's timezone.
        """
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
        timezone = settings.TIME_ZONE if not self.timezone else self.timezone
        return now.astimezone(pytz.timezone(timezone))

    def localtime(self, value):
        """
        Given a datetime object as value convert it to the timezone of
        the account.
        """
        timezone = settings.TIME_ZONE if not self.timezone else self.timezone
        if value.tzinfo is None:
            value = pytz.timezone(settings.TIME_ZONE).localize(value)
        return value.astimezone(pytz.timezone(timezone))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, **kwargs):
    """
    After User.save is called we check to see if it was a created user. If so,
    we check if the User object wants account creation. If all passes we
    create an Account object.

    We only run on user creation to avoid having to check for existence on
    each call to User.save.
    """
    user, created = kwargs["instance"], kwargs["created"]
    disabled = getattr(user, "_disable_account_creation", not settings.ACCOUNT_CREATE_ON_SAVE)
    if created and not disabled:
        Account.create(user=user)


@python_2_unicode_compatible
class AnonymousAccount(object):

    def __init__(self, request=None):
        self.user = AnonymousUser()
        self.timezone = settings.TIME_ZONE
        if request is None:
            self.language = settings.LANGUAGE_CODE
        else:
            self.language = translation.get_language_from_request(request, check_path=True)

    def __str__(self):
        return "AnonymousAccount"


@python_2_unicode_compatible
class SignupCode(models.Model):

    class AlreadyExists(Exception):
        pass

    class InvalidCode(Exception):
        pass

    code = models.CharField(_("code"), max_length=64, unique=True)
    max_uses = models.PositiveIntegerField(_("max uses"), default=0)
    expiry = models.DateTimeField(_("expiry"), null=True, blank=True)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    notes = models.TextField(_("notes"), blank=True)
    sent = models.DateTimeField(_("sent"), null=True, blank=True)
    created = models.DateTimeField(_("created"), default=timezone.now, editable=False)
    use_count = models.PositiveIntegerField(_("use count"), editable=False, default=0)

    class Meta:
        verbose_name = _("signup code")
        verbose_name_plural = _("signup codes")

    def __str__(self):
        if self.email:
            return "{0} [{1}]".format(self.email, self.code)
        else:
            return self.code

    @classmethod
    def exists(cls, code=None, email=None):
        checks = []
        if code:
            checks.append(Q(code=code))
        if email:
            checks.append(Q(email=code))
        if not checks:
            return False
        return cls._default_manager.filter(six.moves.reduce(operator.or_, checks)).exists()

    @classmethod
    def create(cls, **kwargs):
        email, code = kwargs.get("email"), kwargs.get("code")
        if kwargs.get("check_exists", True) and cls.exists(code=code, email=email):
            raise cls.AlreadyExists()
        expiry = timezone.now() + datetime.timedelta(hours=kwargs.get("expiry", 24))
        if not code:
            code = hookset.generate_signup_code_token(email)
        params = {
            "code": code,
            "max_uses": kwargs.get("max_uses", 0),
            "expiry": expiry,
            "inviter": kwargs.get("inviter"),
            "notes": kwargs.get("notes", "")
        }
        if email:
            params["email"] = email
        return cls(**params)

    @classmethod
    def check_code(cls, code):
        try:
            signup_code = cls._default_manager.get(code=code)
        except cls.DoesNotExist:
            raise cls.InvalidCode()
        else:
            if signup_code.max_uses and signup_code.max_uses <= signup_code.use_count:
                raise cls.InvalidCode()
            else:
                if signup_code.expiry and timezone.now() > signup_code.expiry:
                    raise cls.InvalidCode()
                else:
                    return signup_code

    def calculate_use_count(self):
        self.use_count = self.signupcoderesult_set.count()
        self.save()

    def use(self, user):
        """
        Add a SignupCode result attached to the given user.
        """
        result = SignupCodeResult()
        result.signup_code = self
        result.user = user
        result.save()
        signup_code_used.send(sender=result.__class__, signup_code_result=result)

    def send(self, **kwargs):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        if "signup_url" not in kwargs:
            signup_url = "{0}://{1}{2}?{3}".format(
                protocol,
                current_site.domain,
                reverse("account_signup"),
                urlencode({"code": self.code})
            )
        else:
            signup_url = kwargs["signup_url"]
        ctx = {
            "signup_code": self,
            "current_site": current_site,
            "signup_url": signup_url,
        }
        ctx.update(kwargs.get("extra_ctx", {}))
        hookset.send_invitation_email([self.email], ctx)
        self.sent = timezone.now()
        self.save()
        signup_code_sent.send(sender=SignupCode, signup_code=self)


class SignupCodeResult(models.Model):

    signup_code = models.ForeignKey(SignupCode)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, **kwargs):
        super(SignupCodeResult, self).save(**kwargs)
        self.signup_code.calculate_use_count()


@python_2_unicode_compatible
class EmailAddress(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.EmailField(max_length=254, unique=settings.ACCOUNT_EMAIL_UNIQUE)
    verified = models.BooleanField(_("verified"), default=False)
    primary = models.BooleanField(_("primary"), default=False)

    objects = EmailAddressManager()

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        if not settings.ACCOUNT_EMAIL_UNIQUE:
            unique_together = [("user", "email")]

    def __str__(self):
        return "{0} ({1})".format(self.email, self.user)

    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        self.user.email = self.email
        self.user.save()
        return True

    def send_confirmation(self, **kwargs):
        confirmation = EmailConfirmation.create(self)
        confirmation.send(**kwargs)
        return confirmation

    def change(self, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            self.user.email = new_email
            self.user.save()
            self.email = new_email
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation()


@python_2_unicode_compatible
class EmailConfirmation(models.Model):

    email_address = models.ForeignKey(EmailAddress)
    created = models.DateTimeField(default=timezone.now)
    sent = models.DateTimeField(null=True)
    key = models.CharField(max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def __str__(self):
        return "confirmation for {0}".format(self.email_address)

    @classmethod
    def create(cls, email_address):
        key = hookset.generate_email_confirmation_token(email_address.email)
        return cls._default_manager.create(email_address=email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(days=settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def confirm(self):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()
            signals.email_confirmed.send(sender=self.__class__, email_address=email_address)
            return email_address

    def send(self, **kwargs):
        current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        activate_url = "{0}://{1}{2}".format(
            protocol,
            current_site.domain,
            reverse(settings.ACCOUNT_EMAIL_CONFIRMATION_URL, args=[self.key])
        )
        ctx = {
            "email_address": self.email_address,
            "user": self.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": self.key,
        }
        hookset.send_confirmation_email([self.email_address.email], ctx)
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__, confirmation=self)


class AccountDeletion(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(max_length=254)
    date_requested = models.DateTimeField(_("date requested"), default=timezone.now)
    date_expunged = models.DateTimeField(_("date expunged"), null=True, blank=True)

    class Meta:
        verbose_name = _("account deletion")
        verbose_name_plural = _("account deletions")

    @classmethod
    def expunge(cls, hours_ago=None):
        if hours_ago is None:
            hours_ago = settings.ACCOUNT_DELETION_EXPUNGE_HOURS
        before = timezone.now() - datetime.timedelta(hours=hours_ago)
        count = 0
        for account_deletion in cls.objects.filter(date_requested__lt=before, user__isnull=False):
            settings.ACCOUNT_DELETION_EXPUNGE_CALLBACK(account_deletion)
            account_deletion.date_expunged = timezone.now()
            account_deletion.save()
            count += 1
        return count

    @classmethod
    def mark(cls, user):
        account_deletion, created = cls.objects.get_or_create(user=user)
        account_deletion.email = user.email
        account_deletion.save()
        settings.ACCOUNT_DELETION_MARK_CALLBACK(account_deletion)
        return account_deletion
