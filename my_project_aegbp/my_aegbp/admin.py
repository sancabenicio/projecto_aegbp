from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import (
    Photo, Video, Event, Document, Sponsor, BlogPost, Comment, VolunteerOpportunity, 
    Volunteer, Project, ProjectImpact, Testimonial, FAQ, ContactMessage, UserProfile, PrivacyPolicy, About
)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('event', 'image_preview', 'caption')
    list_filter = ('event',)
    search_fields = ('caption',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" width="100" />' % obj.image.url)
        return 'No image'
    image_preview.short_description = _('Image Preview')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'video_url', 'description')
    list_filter = ('event',)
    search_fields = ('description',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'start_time', 'end_time', 'description')
    search_fields = ('name', 'description')
    list_filter = ('date',)
    date_hierarchy = 'date'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'description')
    search_fields = ('title',)

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'description')
    search_fields = ('name',)
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe('<img src="%s" width="100" />' % obj.logo.url)
        return 'No logo'
    logo_preview.short_description = _('Logo Preview')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('author', 'content')
    list_filter = ('post', 'created_at')

@admin.register(VolunteerOpportunity)
class VolunteerOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'description')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'opportunity', 'registration_date')
    readonly_fields = ('registration_date',)
    list_filter = ('opportunity',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'description')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')
    date_hierarchy = 'start_date'

@admin.register(ProjectImpact)
class ProjectImpactAdmin(admin.ModelAdmin):
    list_display = ('project', 'date', 'report')
    search_fields = ('report',)
    list_filter = ('project', 'date')
    date_hierarchy = 'date'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'content')
    search_fields = ('name', 'content')
    list_filter = ('date',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    search_fields = ('question', 'answer')
    list_filter = ('category',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent')
    search_fields = ('name', 'subject')
    list_filter = ('date_sent',)
    date_hierarchy = 'date_sent'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'address', 'city', 'state', 'zip_code', 'description')

admin.site.register(PrivacyPolicy)

class AboutAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and About.objects.exists():
            raise ValidationError(_("Apenas uma seção 'Sobre' é permitida."))
        super().save_model(request, obj, form, change)

admin.site.register(About, AboutAdmin)
