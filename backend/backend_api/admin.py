from django import forms
from django.contrib import admin
from django.template.loader import render_to_string
from django.contrib.admin.helpers import ActionForm

from aaiss_backend.settings import SKYROOM_BASE_URL
from backend_api import models
from backend_api.email import MailerThread
from backend_api.models import Discount, Presentation, PresentationParticipation, WorkshopRegistration
from backend_api.sms import SMSThread
from utils.skyroom_exporter import SkyroomCredentials, convert_credentials_to_csv_response


class TeacherAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = models.Teacher
        fields = '__all__'


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = ('__str__', 'order',)


class PresenterAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = models.Presenter
        fields = '__all__'


class PresenterAdmin(admin.ModelAdmin):
    form = PresenterAdminForm
    list_display = ('__str__', 'order',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('account',)
    actions = ['send_record_links']

    @admin.action(description='Send presentation/workshop record links')
    def send_record_links(self, request, obj):
        for user in obj:
            presentation_participation = PresentationParticipation.objects.filter(user=user,
                                                                                  status=PresentationParticipation.
                                                                                  StatusChoices.PURCHASED)
            workshop_participation = WorkshopRegistration.objects.filter(user=user,
                                                                         status=WorkshopRegistration.StatusChoices.PURCHASED)
            if len(presentation_participation) == 0 and len(workshop_participation) == 0:
                continue

            presentation_links = []
            for presentation in presentation_participation:
                presentation_links.append({
                    'url': presentation.presentation.recorded_link,
                    'name': presentation.presentation.name
                })
            for workshop in workshop_participation:
                presentation_links.append({
                    'url': workshop.workshop.recorded_link,
                    'name': workshop.workshop.name
                })
            MailerThread(f"AAISS recorded links",
                         [user.account.email],
                         render_to_string('record_links.html',
                                          {
                                              'presentations': presentation_links,
                                          })).start()


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'discount_percent', 'capacity', 'remaining_capacity', 'expiration_date')
    readonly_fields = ('participants',)

    class Meta:
        model = Discount
        fields = '__all__'


class PaymentAdmin(admin.ModelAdmin):
    rdfields = []
    for field in models.Payment._meta.get_fields():
        rdfields.append(field.__str__().split('.')[-1])

    readonly_fields = rdfields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

    class Meta:
        model = models.Payment
        fields = '__all__'


class PresentationAdmin(admin.ModelAdmin):
    class PresentationForm(ActionForm):
        _CHOISES = (('aaiss', 'aaiss'), ('aaiss2', 'aaiss2'))
        room_name = forms.ChoiceField(choices=_CHOISES, required=True)

    list_display = ('__str__', 'level', 'no_of_participants', 'year')
    readonly_fields = ('participants',)
    actions = ['export_login_credentials', 'send_registration_emails', 'send_registration_sms']
    action_form = PresentationForm

    class Meta:
        model = Presentation
        fields = '__all__'

    @admin.action(description='Export login credentials')
    def export_login_credentials(self, request, obj):
        user_credentials: list[SkyroomCredentials] = []
        for presentation in obj:
            for registration in presentation.presentationparticipation_set.filter(
                    status=PresentationParticipation.StatusChoices.PURCHASED):
                user_credentials.append(
                    SkyroomCredentials(registration.username, registration.password,
                                       registration.user.name, request.POST['room_name']))
        return convert_credentials_to_csv_response(user_credentials)

    @admin.action(description='Send registration emails')
    def send_registration_emails(self, request, obj):
        for presentation in obj:
            data = [{
                "email": registration.user.account.email,
                "subject": f"AAISS login credentials for {presentation.name}",
                "content": render_to_string('login_credentials.html',
                                          {
                                              'username': registration.username,
                                              'password': registration.password,
                                              'meeting_url': SKYROOM_BASE_URL + '/' + request.POST['room_name'],
                                              'meeting_type': 'presentation',
                                              'meeting_title': presentation.name,
                                          })
            } for registration in presentation.presentationparticipation_set.filter(
                    status=PresentationParticipation.StatusChoices.PURCHASED)]
            MailerThread(data).start()

    @admin.action(description='Send registration sms')
    def send_registration_sms(self, request, obj):
        for presentation in obj:
            mobiles = {
                str(registration.user.phone_number)
                for registration in presentation.presentationparticipation_set.filter(
                    status=PresentationParticipation.StatusChoices.PURCHASED
                )
            }

            message_text = (
                f"Dear User, this is a friendly reminder to join us for the upcoming presentation '{presentation.name}'. "
                f"We look forward to your participation! Date: {presentation.start_date}"
            )

            if mobiles:
                SMSThread(message_text, list(mobiles)).start()


class WorkshopAdmin(admin.ModelAdmin):
    class WorkshopForm(ActionForm):
        _CHOISES = (('aaiss', 'aaiss'), ('aaiss2', 'aaiss2'))
        room_name = forms.ChoiceField(choices=_CHOISES, required=True)

    list_display = ('__str__', 'capacity', 'cost', 'has_project', 'level', 'no_of_participants', 'year')
    readonly_fields = ('participants',)
    actions = ['export_login_credentials', 'send_registration_emails', 'send_registration_sms']
    action_form = WorkshopForm

    class Meta:
        model = models.Workshop
        fields = '__all__'

    @admin.action(description='Export login credentials')
    def export_login_credentials(self, request, obj):
        user_credentials: list[SkyroomCredentials] = []
        for workshop in obj:
            for registration in workshop.workshopregistration_set.filter(
                    status=WorkshopRegistration.StatusChoices.PURCHASED):
                user_credentials.append(
                    SkyroomCredentials(registration.username, registration.password,
                                       registration.user.name, request.POST['room_name']))
        return convert_credentials_to_csv_response(user_credentials)

    @admin.action(description='Send registration emails')
    def send_registration_emails(self, request, obj):
        for workshop in obj:
            data = [{
                "email": registration.user.account.email,
                "subject": f"AAISS login credentials for {workshop.name}",
                "content": render_to_string('login_credentials.html',
                                          {
                                              'username': registration.username,
                                              'password': registration.password,
                                              'meeting_url': SKYROOM_BASE_URL + '/' + request.POST['room_name'],
                                              'meeting_type': 'workshop',
                                              'meeting_title': workshop.name,
                                          })
            } for registration in workshop.workshopregistration_set.filter(
                    status=WorkshopRegistration.StatusChoices.PURCHASED)]
            MailerThread(data).start()

    @admin.action(description='Send registration sms')
    def send_registration_sms(self, request, obj):
        for workshop in obj:
            mobiles = {
                str(registration.user.phone_number)
                for registration in workshop.workshopregistration_set.filter(
                    status=WorkshopRegistration.StatusChoices.PURCHASED
                )
            }

            message_text = (
                f"Dear User, this is a friendly reminder to join us for the upcoming workshop '{workshop.name}'. "
                f"We look forward to your participation! Date: {workshop.start_date}"
            )

            if mobiles:
                SMSThread(message_text, list(mobiles)).start()


class MiscAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year')

    class Meta:
        model = models.Misc
        fields = '__all__'


admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Presenter, PresenterAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.WorkshopRegistration)
admin.site.register(models.PresentationParticipation)
admin.site.register(models.Account)
admin.site.register(models.Committee)
admin.site.register(models.FieldOfInterest)
admin.site.register(models.Staff)
admin.site.register(models.Workshop, WorkshopAdmin)
admin.site.register(models.Presentation, PresentationAdmin)
admin.site.register(models.Misc, MiscAdmin)
