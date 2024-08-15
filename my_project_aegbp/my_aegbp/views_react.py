from django.utils.translation import gettext_lazy as _, activate, get_language
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import (
    Photo, ContactInfo, Video, Event, Document, BlogPost, Comment, VolunteerOpportunity, 
    ContactMessage, Testimonial, FAQ, Project, Donation, Sponsor, About, Volunteer, 
    GeneralSettings, Member, PrivacyPolicy, SocialMedia
)
from .serializers import (
    PhotoSerializer, VideoSerializer, EventSerializer, DocumentSerializer, 
    BlogPostSerializer, CommentSerializer, VolunteerOpportunitySerializer, 
    ContactMessageSerializer, TestimonialSerializer, FAQSerializer, ProjectSerializer, 
    DonationSerializer, SponsorSerializer, ContactInfoSerializer, AboutSerializer, 
    VolunteerSerializer, GeneralSettingsSerializer, MemberSerializer, 
    PrivacyPolicySerializer, SocialMediaSerializer
)

class TranslatableModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        language = self.request.query_params.get('lang', get_language())
        activate(language)
        return super().get_queryset()

class PhotoViewSet(TranslatableModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class VideoViewSet(TranslatableModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class EventViewSet(TranslatableModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class DocumentViewSet(TranslatableModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class BlogPostViewSet(TranslatableModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class CommentViewSet(TranslatableModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id is not None:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        if not BlogPost.objects.filter(id=post_id).exists():
            raise ValidationError({"post": _("O post referenciado não existe.")})
        serializer.save()

class VolunteerOpportunityViewSet(TranslatableModelViewSet):
    queryset = VolunteerOpportunity.objects.all()
    serializer_class = VolunteerOpportunitySerializer

class VolunteerViewSet(TranslatableModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

    def perform_create(self, serializer):
        if 'status' in self.request.data and self.request.data['status'] == 'rejected':
            raise ValidationError({"status": _("Não é possível criar voluntários com status rejeitado.")})
        serializer.save()

class ContactMessageViewSet(TranslatableModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        if 'email' not in self.request.data or '@' not in self.request.data['email']:
            raise ValidationError({"email": _("Um endereço de email válido é necessário.")})
        serializer.save()

class TestimonialViewSet(TranslatableModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class FAQViewSet(TranslatableModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class ProjectViewSet(TranslatableModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class DonationViewSet(TranslatableModelViewSet):  
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def perform_create(self, serializer):
        amount = self.request.data.get('amount')
        if amount is not None and float(amount) <= 0:
            raise ValidationError({"amount": _("O valor da doação deve ser maior que zero.")})
        serializer.save()

class SponsorViewSet(TranslatableModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

class ContactInfoViewSet(TranslatableModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer

    def perform_update(self, serializer):
        if self.queryset.count() > 1:
            raise ValidationError(_("Você não pode ter mais de uma entrada de informação de contato."))
        serializer.save()

class AboutViewSet(TranslatableModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

    def perform_create(self, serializer):
        if About.objects.exists():
            raise ValidationError(_("Apenas uma entrada de Sobre é permitida."))
        serializer.save()

class GeneralSettingsViewSet(TranslatableModelViewSet):
    queryset = GeneralSettings.objects.all()
    serializer_class = GeneralSettingsSerializer

    def perform_update(self, serializer):
        if GeneralSettings.objects.count() > 1:
            raise ValidationError(_("Você não pode ter mais de uma entrada de Configurações Gerais."))
        serializer.save()

class MemberViewSet(TranslatableModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        if Member.objects.filter(email=email).exists():
            raise ValidationError({"email": _("Já existe um membro com este email.")})
        serializer.save()

class PrivacyPolicyViewSet(TranslatableModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer

class SocialMediaViewsSet(TranslatableModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
