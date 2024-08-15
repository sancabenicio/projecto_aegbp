from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import (Photo, Video, Event, Document, BlogPost, Comment, VolunteerOpportunity, ContactMessage, 
                     Testimonial, FAQ, Project, Donation, Sponsor, ContactInfo, About, Volunteer, GeneralSettings, 
                     Member, PrivacyPolicy, SocialMedia)

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(_("O título deve ter pelo menos 5 caracteres."))
        return value

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def validate_url(self, value):
        if not value.startswith('https://'):
            raise serializers.ValidationError(_("A URL do vídeo deve começar com 'https://'."))
        return value

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(_("A data do evento não pode estar no passado."))
        return value

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def validate_file(self, value):
        if value.size > 5 * 1024 * 1024:  # 5 MB
            raise serializers.ValidationError(_("O tamanho do documento não pode exceder 5MB."))
        return value


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'image', 'author_name', 'author_username', 'formatted_date']

    def get_author_name(self, obj):
        return obj.author.get_full_name()

    def get_author_username(self, obj):
        return obj.author.username

    def get_formatted_date(self, obj):
        return obj.updated_at.strftime('%d/%m/%Y')

    def validate_content(self, value):
        if len(value) < 50:
            raise serializers.ValidationError(_("O conteúdo deve ter pelo menos 50 caracteres."))
        return value

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author', write_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'post', 'created_at']

    def create(self, validated_data):
        author_name = validated_data.pop('author')
        comment = Comment.objects.create(author=author_name, **validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author_name'] = instance.author
        return representation

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(_("O conteúdo do comentário deve ter pelo menos 10 caracteres."))
        return value

class VolunteerOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerOpportunity
        fields = '__all__'

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(_("O prazo não pode estar no passado."))
        return value

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError(_("Os voluntários devem ter pelo menos 18 anos de idade."))
        return value

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError(_("Digite um endereço de email válido."))
        return value

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

    def validate_question(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(_("A pergunta deve ter pelo menos 5 caracteres."))
        return value

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("O orçamento deve ser maior que zero."))
        return value

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("O valor da doação deve ser maior que zero."))
        return value

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'

class GeneralSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSettings
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def validate_email(self, value):
        if Member.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Já existe um membro com este email."))
        return value

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

    def validate_url(self, value):
        if not value.startswith('https://'):
            raise serializers.ValidationError(_("A URL da rede social deve começar com 'https://'."))
        return value
