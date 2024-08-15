from haystack import indexes
from .models import Photo, Video, Event, Document, BlogPost, VolunteerOpportunity, ContactMessage, Testimonial, FAQ, Project, Donation, Sponsor

class BaseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True, template_name='search/indexes/my_aegbp/text.txt')

    def get_model(self):
        raise NotImplementedError

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class PhotoIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Photo

class VideoIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Video

class EventIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Event

class DocumentIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Document

class BlogPostIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return BlogPost

class VolunteerOpportunityIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return VolunteerOpportunity

class ContactMessageIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return ContactMessage

class TestimonialIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Testimonial

class FAQIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return FAQ

class ProjectIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Project

class DonationIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Donation

class SponsorIndex(BaseIndex, indexes.Indexable):
    def get_model(self):
        return Sponsor
