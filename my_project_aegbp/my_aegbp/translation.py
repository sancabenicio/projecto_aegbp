from modeltranslation.translator import translator, TranslationOptions
from .models import Event, Registration, Photo, Video, Document, Sponsor, BlogPost, Comment, VolunteerOpportunity, Volunteer, Project, ProjectImpact, Testimonial, Category, FAQ, ContactMessage, Message, ContactInfo, Donation, GeneralSettings, UserProfile, Member, PrivacyPolicy, About, SocialMedia

class EventTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class RegistrationTranslationOptions(TranslationOptions):
    fields = ('name',)

class PhotoTranslationOptions(TranslationOptions):
    fields = ('caption',)

class VideoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class DocumentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class SponsorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

class CommentTranslationOptions(TranslationOptions):
    fields = ('content',)

class VolunteerOpportunityTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'location')

class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class TestimonialTranslationOptions(TranslationOptions):
    fields = ('name', 'content')

class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

class ContactMessageTranslationOptions(TranslationOptions):
    fields = ('name', 'subject', 'message')

class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('address', 'phone1', 'phone2', 'days_of_week', 'hours')

class DonationTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class SocialMediaTranslationOptions(TranslationOptions):
    fields = ('profile_name',)

translator.register(Event, EventTranslationOptions)
translator.register(Registration, RegistrationTranslationOptions)
translator.register(Photo, PhotoTranslationOptions)
translator.register(Video, VideoTranslationOptions)
translator.register(Document, DocumentTranslationOptions)
translator.register(Sponsor, SponsorTranslationOptions)
translator.register(BlogPost, BlogPostTranslationOptions)
translator.register(Comment, CommentTranslationOptions)
translator.register(VolunteerOpportunity, VolunteerOpportunityTranslationOptions)
translator.register(Project, ProjectTranslationOptions)
translator.register(Testimonial, TestimonialTranslationOptions)
translator.register(FAQ, FAQTranslationOptions)
translator.register(ContactMessage, ContactMessageTranslationOptions)
translator.register(ContactInfo, ContactInfoTranslationOptions)
translator.register(Donation, DonationTranslationOptions)
translator.register(About, AboutTranslationOptions)
translator.register(SocialMedia, SocialMediaTranslationOptions)
