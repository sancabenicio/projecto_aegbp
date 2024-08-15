from django.urls import path, include
from django.conf.urls.i18n import set_language
from .views import search
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    password_reset_error, contact_list,list_members, add_member, edit_member, 
    delete_member, download_members_excel, view_notification, privacy_policy_list,
    privacy_policy_detail, privacy_policy_create, privacy_policy_update, privacy_policy_delete,
    settings_list, settings_create, settings_update, settings_delete, 
    social_media_list, social_media_create, social_media_update, social_media_delete, send_email
    

)


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', search, name='search'),
    path('photos/', views.photo_gallery, name='photo_gallery'),
    path('photos/create/', views.photo_create, name='photo_create'),
    path('photos/<int:id>/update/', views.photo_update, name='photo_update'),
    path('photos/<int:id>/delete/', views.photo_delete, name='photo_delete'),
    path('videos/', views.video_gallery, name='video_gallery'),
    path('videos/create/', views.video_create, name='video_create'),
    path('videos/<int:id>/update/', views.video_update, name='video_update'),
    path('videos/<int:id>/delete/', views.video_delete, name='video_delete'),
    path('events/', views.calendar_view, name='calendar_view'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:id>/update/', views.event_update, name='event_update'),
    path('events/<int:id>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('events/<int:event_id>/registrations/', views.event_registrations, name='event_registrations'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/<int:id>/update/', views.document_update, name='document_update'),
    path('documents/<int:id>/delete/', views.document_delete, name='document_delete'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:post_id>/', views.blog_post, name='blog_post'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:id>/update/', views.blog_update, name='blog_update'),
    path('blog/<int:id>/delete/', views.blog_delete, name='blog_delete'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/create/', views.testimonial_create, name='testimonial_create'),
    path('testimonials/<int:id>/update/', views.testimonial_update, name='testimonial_update'),
    path('testimonials/<int:id>/delete/', views.testimonial_delete, name='testimonial_delete'),
    path('faqs/', views.faqs, name='faqs'),
    path('faqs/create/', views.faq_create, name='faq_create'),
    path('faqs/<int:id>/update/', views.faq_update, name='faq_update'),
    path('faqs/<int:id>/delete/', views.faq_delete, name='faq_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:id>/', views.category_update, name='category_update'),
    path('categories/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('volunteers/', views.volunteer_opportunities, name='volunteer_opportunities'),
    path('volunteers/<int:opportunity_id>/register/', views.register_volunteer, name='register_volunteer'),
    path('volunteers/create/', views.volunteer_create, name='volunteer_create'),
    path('volunteers/<int:id>/update/', views.volunteer_update, name='volunteer_update'),
    path('volunteers/<int:id>/delete/', views.volunteer_delete, name='volunteer_delete'),
    path('volunteers/<int:id>/', views.opportunity_detail, name='opportunity_detail'),
    path('volunteers/<int:opportunity_id>/registrations/', views.volunteer_registrations, name='volunteer_registrations'),

    #contact
    path('contact/', contact_list, name='contact_list'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('contact/create/', views.contact_create, name='contact_create'),
    path('contacts/respond/<int:id>/', views.contact_respond, name='contact_respond'),
    path('contact/conversation/<int:id>/', views.contact_conversation, name='contact_conversation'),

    path('projects/', views.projects, name='projects'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:id>/update/', views.project_update, name='project_update'),
    path('projects/<int:id>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:id>/', views.project_detail, name='project_detail'),
    path('donations/', views.donation_list, name='donation_list'),
    path('donations/<int:id>/', views.donation_info, name='donation_info'),
    path('donations/create/', views.donation_create, name='donation_create'),
    path('donations/<int:id>/update/', views.donation_update, name='donation_update'),
    path('donations/<int:id>/delete/', views.donation_delete, name='donation_delete'),
    path('sponsors/', views.sponsor_list, name='sponsor_list'),
path('sponsors/create/', views.sponsor_create, name='sponsor_create'),
path('sponsors/<int:id>/update/', views.sponsor_update, name='sponsor_update'),
path('sponsors/<int:id>/delete/', views.sponsor_delete, name='sponsor_delete'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),

    path('set_language/', views.custom_set_language, name='custom_set_language'),

     # URLs de redefinição de senha
   path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/error/', password_reset_error, name='password_reset_error'),

    path('members/', views.list_members, name='list_members'),
    path('members/add/', views.add_member, name='add_member'),
    path('members/<int:id>/edit/', views.edit_member, name='edit_member'),
    path('members/<int:id>/delete/', views.delete_member, name='delete_member'),
    path('members/download/', views.download_members_excel, name='download_members_excel'),
    path('members/<int:id>/', views.member_detail, name='member_detail'), 
    path('list_pending_members/', views.list_pending_members, name='list_pending_members'),
    path('approve_member/<int:id>/', views.approve_member, name='approve_member'),
    path('reject_member/<int:id>/', views.reject_member, name='reject_member'),
    path('member_detail_pend/<int:id>/', views.member_detail_pend, name='member_detail_pend'),
    #path('notification/<str:type>/<int:id>/', views.view_notification, name='view_notification'),
    path('view_notification/<str:type>/<int:id>/', view_notification, name='view_notification'),

    path('privacy-policy/', privacy_policy_list, name='privacy_policy_list'),
    path('privacy-policy/<int:id>/', privacy_policy_detail, name='privacy_policy_detail'),
    path('privacy-policy/new/', privacy_policy_create, name='privacy_policy_create'),
    path('privacy-policy/<int:id>/edit/', privacy_policy_update, name='privacy_policy_update'),
    path('privacy-policy/<int:id>/delete/', privacy_policy_delete, name='privacy_policy_delete'),
    path('tinymce/', include('tinymce.urls')),

    path('contact-info/', views.contact_info_list, name='contact_info_list'),  # Atualização aqui
    path('contact-info/create/', views.contact_info_create, name='contact_info_create'),
    path('contact-info/update/<int:id>/', views.contact_info_update, name='contact_info_update'),
    path('contact-info/delete/<int:id>/', views.contact_info_delete, name='contact_info_delete'),

    path('about/', views.about_list, name='about_list'),
    path('about/<int:id>/', views.about_detail, name='about_detail'),
    path('about/new/', views.about_create, name='about_create'),
    path('about/edit/<int:id>/', views.about_update, name='about_update'),
    path('about/delete/<int:id>/', views.about_delete, name='about_delete'),

    path('settings/', settings_list, name='settings_list'),
    path('settings/new/', settings_create, name='settings_create'),
    path('settings/<int:id>/edit/', settings_update, name='settings_update'),
    path('settings/<int:id>/delete/', settings_delete, name='settings_delete'),

    path('social/', social_media_list, name='social_media_list'),
    path('social/create/', social_media_create, name='social_media_create'),
    path('social/<int:id>/edit/', social_media_update, name='social_media_update'),
    path('social/<int:id>/delete/', social_media_delete, name='social_media_delete'),

    path('register/', views.register, name='register'),
    path('api/send-email/', send_email, name='send_email'),
    path('download-document/<int:document_id>/', views.download_document, name='download_document'),

]
