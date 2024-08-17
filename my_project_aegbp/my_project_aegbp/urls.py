from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500, handler403, handler400
from my_aegbp import views
from rest_framework.routers import DefaultRouter
from my_aegbp.views_react import (PhotoViewSet, VideoViewSet, EventViewSet, DocumentViewSet, 
                          BlogPostViewSet, CommentViewSet, VolunteerOpportunityViewSet, ContactMessageViewSet,
                            TestimonialViewSet, FAQViewSet, ProjectViewSet, DonationViewSet, SponsorViewSet, ContactInfoViewSet,
                              AboutViewSet, VolunteerViewSet, GeneralSettingsViewSet, MemberViewSet, PrivacyPolicyViewSet, SocialMediaViewsSet)



router = DefaultRouter()
router.register(r'photos', PhotoViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'events', EventViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'blogposts', BlogPostViewSet)
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'volunteer-opportunities', VolunteerOpportunityViewSet)
router.register(r'contact-messages', ContactMessageViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'contact-info', ContactInfoViewSet)
router.register(r'about', AboutViewSet)
router.register(r'volunteers', VolunteerViewSet)
router.register(r'general-settings', GeneralSettingsViewSet)
router.register(r'members', MemberViewSet)
router.register(r'Privacy', PrivacyPolicyViewSet)
router.register(r'Social', SocialMediaViewsSet)


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # URL para configuração de idiomas
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # URL raiz configurada para a view 'index'
    path('', include('my_aegbp.urls')),  # Inclua as URLs do seu aplicativo principal
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('api/', include(router.urls)),
)
    

handler404 = 'my_project_aegbp.error_handling.handle_404'
handler500 = 'my_project_aegbp.error_handling.handle_500'
handler403 = 'my_project_aegbp.error_handling.handle_permission_denied'
handler400 = 'my_project_aegbp.error_handling.handle_bad_request'
