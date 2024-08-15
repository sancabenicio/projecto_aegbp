import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.http import HttpResponseRedirect
from django.core.exceptions import FieldError, ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail, mail_admins
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError
from haystack.query import SearchQuerySet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.translation import gettext_lazy as _
from .models import Member
from .forms import MemberForm
import pandas as pd
from .forms import (
    RegistrationForm, PhotoForm, VideoForm, EventForm, DocumentForm, 
    BlogPostForm, CommentForm, VolunteerOpportunityForm, VolunteerForm, 
    ContactForm, TestimonialForm, FAQForm, ProjectForm, DonationForm, SponsorForm,
    CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, CategoryForm,
    ResponseForm, MessageForm, PrivacyPolicyForm, ContactInfoForm, AboutForm, GeneralSettingsForm, SocialMediaForm
)
from .models import (
    Photo, Video, Event, Document, BlogPost, Comment, VolunteerOpportunity, 
    Volunteer, ContactMessage, Testimonial, FAQ, Project, Donation, Sponsor, UserProfile, Category, Registration,
    PrivacyPolicy, ContactInfo, About, GeneralSettings, SocialMedia
)

# Configuração de logging
logger = logging.getLogger(__name__)

def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url=login_url)

@admin_required(login_url='login')
def search(request):
    try:
        query = request.GET.get('q')
        results = SearchQuerySet().filter(content=query)
        return render(request, 'search/results.html', {'query': query, 'results': results})
    except Exception as e:
        logger.error(_("Erro na view de busca: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro na view de busca"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro durante a busca.')})

def get_total_notifications():
    try:
        pending_members = Member.objects.filter(status='pending', is_read=False)
        new_contacts = ContactMessage.objects.filter(status='new', is_read=False)
        return {
            'total_notifications': pending_members.count() + new_contacts.count(),
            'new_contacts': new_contacts,
            'pending_members': pending_members
        }
    except Exception as e:
        logger.error(_("Erro ao obter notificações totais: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao obter notificações totais"), str(e))
        return {
            'total_notifications': 0,
            'new_contacts': [],
            'pending_members': []
        }

def update_total_notifications():
    try:
        pending_count = Member.objects.filter(status='pending', is_read=False).count()
        contacts_count = ContactMessage.objects.filter(status='new', is_read=False).count()
        return pending_count + contacts_count
    except Exception as e:
        logger.error(_("Erro ao atualizar notificações totais: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar notificações totais"), str(e))
        return 0

@admin_required(login_url='login')
def index(request):
    try:
        notifications = get_total_notifications()
        cards = [
            {
                'title': _('Galeria de Fotos'),
                'description': _('Veja as fotos mais recentes da nossa atividade'),
                'icon': 'fa-camera',
                'color': 'text-primary',
                'btn_color': 'primary',
                'view_url': 'photo_gallery',
                'create_url': 'photo_create'
            },
            {
                'title': _('Galeria de Vídeos'),
                'description': _('Assista aos vídeos mais recentes da nossa atividade'),
                'icon': 'fa-video',
                'color': 'text-info',
                'btn_color': 'info',
                'view_url': 'video_gallery',
                'create_url': 'video_create'
            },
            {
                'title': _('Calendário de Eventos'),
                'description': _('Confira os próximos eventos e atividades.'),
                'icon': 'fa-calendar-alt',
                'color': 'text-success',
                'btn_color': 'success',
                'view_url': 'calendar_view',
                'create_url': 'event_create'
            },
            {
                'title': _('Documentos'),
                'description': _('Acesse os documentos importantes e relatórios.'),
                'icon': 'fa-file-alt',
                'color': 'text-warning',
                'btn_color': 'warning',
                'view_url': 'document_list',
                'create_url': 'document_create'
            },
            {
                'title': _('Blog'),
                'description': _('Leia os artigos e posts do nosso blog.'),
                'icon': 'fa-blog',
                'color': 'text-secondary',
                'btn_color': 'secondary',
                'view_url': 'blog_list',
                'create_url': 'blog_create'
            },
            {
                'title': _('Testemunhos'),
                'description': _('Veja os testemunhos de nossos participantes.'),
                'icon': 'fa-quote-left',
                'color': 'text-info',
                'btn_color': 'info',
                'view_url': 'testimonials',
                'create_url': 'testimonial_create'
            },
            {
                'title': _('FAQs'),
                'description': _('Respostas para perguntas frequentes.'),
                'icon': 'fa-question-circle',
                'color': 'text-dark',
                'btn_color': 'dark',
                'view_url': 'faqs',
                'create_url': 'faq_create'
            },
            {
                'title': _('Oportunidades de Voluntariado'),
                'description': _('Participe como voluntário em nossas atividades.'),
                'icon': 'fa-hands-helping',
                'color': 'text-primary',
                'btn_color': 'primary',
                'view_url': 'volunteer_opportunities',
                'create_url': 'volunteer_create'
            },
            {
                'title': _('Contato'),
                'description': _('Entre em contato conosco para mais informações.'),
                'icon': 'fa-envelope',
                'color': 'text-danger',
                'btn_color': 'danger',
                'view_url': 'contact_list',
                'create_url': 'contact_create'
            },
            {
                'title': _('Projetos'),
                'description': _('Descubra mais sobre nossas atividades.'),
                'icon': 'fa-project-diagram',
                'color': 'text-success',
                'btn_color': 'success',
                'view_url': 'projects',
                'create_url': 'project_create'
            },
            {
                'title': _('Doações'),
                'description': _('Apoie nossas atividades através de doações.'),
                'icon': 'fa-donate',
                'color': 'text-success',
                'btn_color': 'success',
                'view_url': 'donation_list',
                'create_url': 'donation_create'
            },
            {
                'title': _('Patrocinadores'),
                'description': _('Conheça nossos patrocinadores.'),
                'icon': 'fa-handshake',
                'color': 'text-info',
                'btn_color': 'info',
                'view_url': 'sponsor_list',
                'create_url': 'sponsor_create'
            },
        ]

        context = {'cards': cards}
        context.update(notifications)
        return render(request, 'index.html', context)
    except Exception as e:
        logger.error(_("Erro na view inicial: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro na view inicial"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a página inicial.')})

@login_required
def view_notification(request, type, id):
    try:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if type == 'contact':
            notification = get_object_or_404(ContactMessage, id=id)
            notification.is_read = True
            notification.save()
            total_notifications = update_total_notifications()
            if is_ajax:
                return JsonResponse({'status': 'success', 'total_notifications': total_notifications})
            return redirect('contact_conversation', id=id)
        elif type == 'member':
            notification = get_object_or_404(Member, id=id)
            notification.is_read = True
            notification.save()
            total_notifications = update_total_notifications()
            if is_ajax:
                return JsonResponse({'status': 'success', 'total_notifications': total_notifications})
            return redirect('list_pending_members')

        if is_ajax:
            return JsonResponse({'status': 'error'}, status=400)
        return redirect('index')
    except Exception as e:
        logger.error(_("Erro na view de notificação: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro na view de notificação"), str(e))
        if request.is_ajax():
            return JsonResponse({'error': _('Ocorreu um erro inesperado.')}, status=500)
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao visualizar a notificação.')})

# Galeria de Fotos
def photo_gallery(request):
    try:
        photos = Photo.objects.all()
        return render(request, 'gallery/photo_gallery.html', {'photos': photos})
    except Exception as e:
        logger.error(_("Erro na galeria de fotos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro na galeria de fotos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a galeria de fotos.')})

def photo_create(request):
    try:
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('photo_gallery')
        else:
            form = PhotoForm()
        return render(request, 'gallery/photo_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar foto: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar foto"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a foto.')})

def photo_update(request, id):
    try:
        photo = get_object_or_404(Photo, id=id)
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, instance=photo)
            if form.is_valid():
                form.save()
                return redirect('photo_gallery')
        else:
            form = PhotoForm(instance=photo)
        return render(request, 'gallery/photo_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar foto: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar foto"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a foto.')})

def photo_delete(request, id):
    try:
        photo = get_object_or_404(Photo, id=id)
        if request.method == 'POST':
            photo.delete()
            return redirect('photo_gallery')
        return render(request, 'gallery/photo_confirm_delete.html', {'photo': photo})
    except Exception as e:
        logger.error(_("Erro ao deletar foto: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar foto"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a foto.')})

# Galeria de Vídeos
def video_gallery(request):
    try:
        videos = Video.objects.all()
        return render(request, 'gallery/video_gallery.html', {'videos': videos})
    except Exception as e:
        logger.error(_("Erro na galeria de vídeos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro na galeria de vídeos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a galeria de vídeos.')})

def video_create(request):
    try:
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('video_gallery')
        else:
            form = VideoForm()
        return render(request, 'gallery/video_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar vídeo: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar vídeo"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o vídeo.')})

def video_update(request, id):
    try:
        video = get_object_or_404(Video, id=id)
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES, instance=video)
            if form.is_valid():
                form.save()
                return redirect('video_gallery')
        else:
            form = VideoForm(instance=video)
        return render(request, 'gallery/video_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar vídeo: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar vídeo"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o vídeo.')})

def video_delete(request, id):
    try:
        video = get_object_or_404(Video, id=id)
        if request.method == 'POST':
            video.delete()
            return redirect('video_gallery')
        return render(request, 'gallery/video_confirm_delete.html', {'video': video})
    except Exception as e:
        logger.error(_("Erro ao deletar vídeo: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar vídeo"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o vídeo.')})

# Calendário de Eventos
def calendar_view(request):
    try:
        events = Event.objects.all()
        return render(request, 'events/calendar.html', {'events': events})
    except Exception as e:
        logger.error(_("Erro ao carregar o calendário de eventos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar o calendário de eventos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar o calendário de eventos.')})

def event_create(request):
    try:
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('calendar_view')
        else:
            form = EventForm()
        return render(request, 'events/event_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar evento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar evento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o evento.')})

def event_update(request, id):
    try:
        event = get_object_or_404(Event, id=id)
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('calendar_view')
        else:
            form = EventForm(instance=event)
        return render(request, 'events/event_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar evento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar evento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o evento.')})

def event_delete(request, id):
    try:
        event = get_object_or_404(Event, id=id)
        if request.method == 'POST':
            event.delete()
            return redirect('calendar_view')
        return render(request, 'events/event_confirm_delete.html', {'event': event})
    except Exception as e:
        logger.error(_("Erro ao deletar evento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar evento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o evento.')})

def register_for_event(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                registration = form.save(commit=False)
                registration.event = event
                registration.save()
                return redirect('event_registrations', event_id=event.id)
        else:
            form = RegistrationForm()
        return render(request, 'events/register_for_event.html', {'form': form, 'event': event})
    except Exception as e:
        logger.error(_("Erro ao registrar-se no evento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao registrar-se no evento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao registrar-se no evento.')})

def event_registrations(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        registrations = Registration.objects.filter(event=event)
        return render(request, 'events/event_registrations.html', {'event': event, 'registrations': registrations})
    except Exception as e:
        logger.error(_("Erro ao carregar inscrições do evento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar inscrições do evento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar as inscrições do evento.')})

# Gerenciamento de Documentos
@admin_required(login_url='login')
def document_list(request):
    try:
        documents = Document.objects.all()
        return render(request, 'documents/document_list.html', {'documents': documents})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de documentos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de documentos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de documentos.')})

@login_required(login_url='login')
def document_create(request):
    try:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('document_list')
        else:
            form = DocumentForm()
        return render(request, 'documents/document_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar documento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar documento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o documento.')})

@admin_required(login_url='login')
def document_update(request, id):
    try:
        document = get_object_or_404(Document, id=id)
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES, instance=document)
            if form.is_valid():
                form.save()
                return redirect('document_list')
        else:
            form = DocumentForm(instance=document)
        return render(request, 'documents/document_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar documento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar documento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o documento.')})

@admin_required(login_url='login')
def document_delete(request, id):
    try:
        document = get_object_or_404(Document, id=id)
        if request.method == 'POST':
            document.delete()
            return redirect('document_list')
        return render(request, 'documents/document_confirm_delete.html', {'document': document})
    except Exception as e:
        logger.error(_("Erro ao deletar documento: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar documento"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o documento.')})

# Blog e Comentários
@admin_required(login_url='login')
def blog_list(request):
    try:
        posts = BlogPost.objects.all()
        return render(request, 'blog/blog_list.html', {'posts': posts})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de postagens do blog: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de postagens do blog"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de postagens do blog.')})

@admin_required(login_url='login')
def blog_post(request, post_id):
    try:
        post = get_object_or_404(BlogPost, id=post_id)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('blog_post', post_id=post.id)
        else:
            form = CommentForm()
        return render(request, 'blog/blog_post.html', {'post': post, 'form': form})
    except Exception as e:
        logger.error(_("Erro ao carregar postagem do blog: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar postagem do blog"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a postagem do blog.')})

@admin_required(login_url='login')
def blog_create(request):
    try:
        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                blog_post = form.save(commit=False)
                blog_post.author = form.cleaned_data['author']
                blog_post.save()
                return redirect('blog_list')
        else:
            form = BlogPostForm()
        return render(request, 'blog/blog_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar postagem no blog: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar postagem no blog"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a postagem no blog.')})

@admin_required(login_url='login')
def blog_update(request, id):
    try:
        post = get_object_or_404(BlogPost, id=id)
        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('blog_list')
        else:
            form = BlogPostForm(instance=post)
        return render(request, 'blog/blog_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar postagem no blog: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar postagem no blog"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a postagem no blog.')})

@admin_required(login_url='login')
def blog_delete(request, id):
    try:
        post = get_object_or_404(BlogPost, id=id)
        if request.method == 'POST':
            post.delete()
            return redirect('blog_list')
        return render(request, 'blog/blog_confirm_delete.html', {'post': post})
    except Exception as e:
        logger.error(_("Erro ao deletar postagem no blog: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar postagem no blog"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a postagem no blog.')})

# Testemunhos
@admin_required(login_url='login')
def testimonials(request):
    try:
        testimonials = Testimonial.objects.all()
        return render(request, 'testimonials/testimonials.html', {'testimonials': testimonials})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de testemunhos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de testemunhos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de testemunhos.')})

@admin_required(login_url='login')
def testimonial_create(request):
    try:
        if request.method == 'POST':
            form = TestimonialForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('testimonials')
        else:
            form = TestimonialForm()
        return render(request, 'testimonials/testimonial_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar testemunho: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar testemunho"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o testemunho.')})

@admin_required(login_url='login')
def testimonial_update(request, id):
    try:
        testimonial = get_object_or_404(Testimonial, id=id)
        if request.method == 'POST':
            form = TestimonialForm(request.POST, instance=testimonial)
            if form.is_valid():
                form.save()
                return redirect('testimonials')
        else:
            form = TestimonialForm(instance=testimonial)
        return render(request, 'testimonials/testimonial_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar testemunho: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar testemunho"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o testemunho.')})

@admin_required(login_url='login')
def testimonial_delete(request, id):
    try:
        testimonial = get_object_or_404(Testimonial, id=id)
        if request.method == 'POST':
            testimonial.delete()
            return redirect('testimonials')
        return render(request, 'testimonials/testimonial_confirm_delete.html', {'testimonial': testimonial})
    except Exception as e:
        logger.error(_("Erro ao deletar testemunho: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar testemunho"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o testemunho.')})

# FAQs
@admin_required(login_url='login')
def faqs(request):
    try:
        faqs = FAQ.objects.all()
        return render(request, 'faqs/faqs.html', {'faqs': faqs})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de FAQs: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de FAQs"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de FAQs.')})

@admin_required(login_url='login')
def faq_create(request):
    try:
        if request.method == 'POST':
            form = FAQForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('faqs')
        else:
            form = FAQForm()
        return render(request, 'faqs/faq_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar FAQ: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar FAQ"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o FAQ.')})

@admin_required(login_url='login')
def faq_update(request, id):
    try:
        faq = get_object_or_404(FAQ, id=id)
        if request.method == 'POST':
            form = FAQForm(request.POST, instance=faq)
            if form.is_valid():
                form.save()
                return redirect('faqs')
        else:
            form = FAQForm(instance=faq)
        return render(request, 'faqs/faq_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar FAQ: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar FAQ"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o FAQ.')})

@admin_required(login_url='login')
def faq_delete(request, id):
    try:
        faq = get_object_or_404(FAQ, id=id)
        if request.method == 'POST':
            faq.delete()
            return redirect('faqs')
        return render(request, 'faqs/faq_confirm_delete.html', {'faq': faq})
    except Exception as e:
        logger.error(_("Erro ao deletar FAQ: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar FAQ"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o FAQ.')})

@admin_required(login_url='login')
def category_list(request):
    try:
        categories = Category.objects.all()
        return render(request, 'categories/category_list.html', {'categories': categories})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de categorias: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de categorias"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de categorias.')})

@admin_required(login_url='login')
def category_create(request):
    try:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('category_list')
        else:
            form = CategoryForm()
        return render(request, 'categories/category_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar categoria: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar categoria"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a categoria.')})

@admin_required(login_url='login')
def category_update(request, id):
    try:
        category = get_object_or_404(Category, id=id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('category_list')
        else:
            form = CategoryForm(instance=category)
        return render(request, 'categories/category_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar categoria: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar categoria"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a categoria.')})

@admin_required(login_url='login')
def category_delete(request, id):
    try:
        category = get_object_or_404(Category, id=id)
        if request.method == 'POST':
            category.delete()
            return redirect('category_list')
        return render(request, 'categories/category_confirm_delete.html', {'category': category})
    except Exception as e:
        logger.error(_("Erro ao deletar categoria: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar categoria"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a categoria.')})

# Oportunidades de Voluntariado
@admin_required(login_url='login')
def volunteer_opportunities(request):
    try:
        opportunities = VolunteerOpportunity.objects.all()
        return render(request, 'volunteers/opportunities.html', {'opportunities': opportunities})
    except Exception as e:
        logger.error(_("Erro ao carregar oportunidades de voluntariado: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar oportunidades de voluntariado"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar as oportunidades de voluntariado.')})

@admin_required(login_url='login')
def volunteer_registrations(request, opportunity_id):
    try:
        opportunity = get_object_or_404(VolunteerOpportunity, id=opportunity_id)
        registrations = Volunteer.objects.filter(opportunity=opportunity)
        return render(request, 'volunteers/volunteer_registrations.html', {'opportunity': opportunity, 'registrations': registrations})
    except Exception as e:
        logger.error(_("Erro ao carregar inscrições de voluntariado: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar inscrições de voluntariado"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar as inscrições de voluntariado.')})

@admin_required(login_url='login')
def register_volunteer(request, opportunity_id):
    try:
        opportunity = get_object_or_404(VolunteerOpportunity, id=opportunity_id)
        if request.method == 'POST':
            form = VolunteerForm(request.POST)
            if form.is_valid():
                volunteer = form.save(commit=False)
                volunteer.opportunity = opportunity
                volunteer.save()
                return redirect('volunteer_opportunities')
        else:
            form = VolunteerForm()
        return render(request, 'volunteers/volunteer_form.html', {'form': form, 'opportunity': opportunity})
    except Exception as e:
        logger.error(_("Erro ao registrar voluntário: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao registrar voluntário"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao registrar o voluntário.')})

@admin_required(login_url='login')
def volunteer_create(request):
    try:
        if request.method == 'POST':
            form = VolunteerOpportunityForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('volunteer_opportunities')
        else:
            form = VolunteerOpportunityForm()
        return render(request, 'volunteers/volunteer_opportunity_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar oportunidade de voluntariado: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar oportunidade de voluntariado"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a oportunidade de voluntariado.')})

@admin_required(login_url='login')
def volunteer_update(request, id):
    try:
        opportunity = get_object_or_404(VolunteerOpportunity, id=id)
        if request.method == 'POST':
            form = VolunteerOpportunityForm(request.POST, instance=opportunity)
            if form.is_valid():
                form.save()
                return redirect('volunteer_opportunities')
        else:
            form = VolunteerOpportunityForm(instance=opportunity)
        return render(request, 'volunteers/volunteer_opportunity_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar oportunidade de voluntariado: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar oportunidade de voluntariado"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a oportunidade de voluntariado.')})

@admin_required(login_url='login')
def volunteer_delete(request, id):
    try:
        opportunity = get_object_or_404(VolunteerOpportunity, id=id)
        if request.method == 'POST':
            opportunity.delete()
            return redirect('volunteer_opportunities')
        return render(request, 'volunteers/volunteer_opportunity_confirm_delete.html', {'opportunity': opportunity})
    except Exception as e:
        logger.error(_("Erro ao deletar oportunidade de voluntariado: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar oportunidade de voluntariado"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a oportunidade de voluntariado.')})

@admin_required(login_url='login')
def opportunity_detail(request, id):
    try:
        opportunity = get_object_or_404(VolunteerOpportunity, id=id)
        return render(request, 'volunteers/opportunity_detail.html', {'opportunity': opportunity})
    except Exception as e:
        logger.error(_("Erro ao carregar detalhes da oportunidade de voluntariado: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar detalhes da oportunidade de voluntariado"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar os detalhes da oportunidade de voluntariado.')})

@admin_required(login_url='login')
def contact_list(request):
    try:
        contatos = ContactMessage.objects.all()
        return render(request, 'contact/contact_list.html', {'contatos': contatos})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de contatos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de contatos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de contatos.')})

@admin_required(login_url='login')
def contact_create(request):
    try:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('contact_list')
        else:
            form = ContactForm()
        return render(request, 'contact/contact_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o contato.')})

@admin_required(login_url='login')
def contact_conversation(request, id):
    try:
        contato = get_object_or_404(ContactMessage, id=id)
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.contact = contato
                message.sender = _('Admin')
                message.save()

                send_mail(
                    _('Resposta ao seu contato: {subject}').format(subject=contato.subject),
                    message.content,
                    settings.DEFAULT_FROM_EMAIL,
                    [contato.email],
                    fail_silently=False,
                )
                return redirect('contact_conversation', id=id)
        else:
            form = MessageForm()
        return render(request, 'contact/contact_conversation.html', {'contato': contato, 'form': form})
    except Exception as e:
        logger.error(_("Erro na conversa de contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro na conversa de contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao responder à mensagem de contato.')})

@admin_required(login_url='login')
def contact_respond(request, id):
    try:
        contato = get_object_or_404(ContactMessage, id=id)
        if request.method == 'POST':
            form = ResponseForm(request.POST, instance=contato)
            if form.is_valid():
                contato = form.save(commit=False)
                contato.status = 'responded'
                contato.save()

                send_mail(
                    _('Resposta ao seu contato: {subject}').format(subject=contato.subject),
                    contato.response,
                    settings.DEFAULT_FROM_EMAIL,
                    [contato.email],
                    fail_silently=False,
                )
                return redirect('contact_list')
        else:
            form = ResponseForm(instance=contato)
        return render(request, 'contact/contact_respond.html', {'form': form, 'contato': contato})
    except Exception as e:
        logger.error(_("Erro ao responder contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao responder contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao responder ao contato.')})

# Projetos
def projects(request):
    try:
        projects_list = Project.objects.all()
        return render(request, 'projects/project_list.html', {'projects': projects_list})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de projetos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de projetos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de projetos.')})

def project_list(request):
    try:
        projects = Project.objects.all()
        return render(request, 'projects/project_list.html', {'projects': projects})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de projetos: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de projetos"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de projetos.')})

def project_create(request):
    try:
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('project_list')
        else:
            form = ProjectForm()
        return render(request, 'projects/project_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar projeto: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar projeto"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o projeto.')})

def project_update(request, id):
    try:
        project = get_object_or_404(Project, id=id)
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                return redirect('projects')
        else:
            form = ProjectForm(instance=project)
        return render(request, 'projects/project_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar projeto: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar projeto"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o projeto.')})

def project_delete(request, id):
    try:
        project = get_object_or_404(Project, id=id)
        if request.method == 'POST':
            project.delete()
            return redirect('projects')
        return render(request, 'projects/project_confirm_delete.html', {'project': project})
    except Exception as e:
        logger.error(_("Erro ao deletar projeto: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar projeto"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o projeto.')})

def project_detail(request, id):
    try:
        project = get_object_or_404(Project, id=id)
        return render(request, 'projects/project_detail.html', {'project': project})
    except Exception as e:
        logger.error(_("Erro ao carregar detalhes do projeto: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar detalhes do projeto"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar os detalhes do projeto.')})

# Doações
def donation_list(request):
    try:
        donations = Donation.objects.all()
        return render(request, 'donations/donation_list.html', {'donations': donations})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de doações: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de doações"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de doações.')})

def donation_create(request):
    try:
        if request.method == 'POST':
            form = DonationForm(request.POST, request.FILES)  
            if form.is_valid():
                form.save()
                return redirect('donation_list')
        else:
            form = DonationForm()
        return render(request, 'donations/donation_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar doação: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar doação"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a doação.')})

def donation_info(request, id):
    try:
        donation = get_object_or_404(Donation, id=id)
        return render(request, 'donations/donation_info.html', {'donation': donation})
    except Exception as e:
        logger.error(_("Erro ao carregar detalhes da doação: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar detalhes da doação"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar os detalhes da doação.')})

def donation_update(request, id):
    try:
        donation = get_object_or_404(Donation, id=id)
        if request.method == 'POST':
            form = DonationForm(request.POST, request.FILES, instance=donation)  # Inclua request.FILES
            if form.is_valid():
                form.save()
                return redirect('donation_list')
        else:
            form = DonationForm(instance=donation)
        return render(request, 'donations/donation_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar doação: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar doação"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a doação.')})

def donation_delete(request, id):
    try:
        donation = get_object_or_404(Donation, id=id)
        if request.method == 'POST':
            donation.delete()
            return redirect('donation_list')
        return render(request, 'donations/donation_confirm_delete.html', {'donation': donation})
    except Exception as e:
        logger.error(_("Erro ao deletar doação: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar doação"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a doação.')})

# Fale Conosco
def contact(request):
    try:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                contact_message = form.save()
                send_mail(
                    _('Formulário de Contato'),
                    contact_message.message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                return redirect('contact_success')
        else:
            form = ContactForm()
        return render(request, 'contact/contact.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao enviar formulário de contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao enviar formulário de contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao enviar o formulário de contato.')})

def contact_success(request):
    return render(request, 'contact/contact_success.html')

def sponsor_list(request):
    try:
        sponsors = Sponsor.objects.all()
        return render(request, 'sponsors/sponsor_list.html', {'sponsors': sponsors})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de patrocinadores: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de patrocinadores"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de patrocinadores.')})

def sponsor_create(request):
    try:
        if request.method == 'POST':
            form = SponsorForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('sponsor_list')
        else:
            form = SponsorForm()
        return render(request, 'sponsors/sponsor_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar patrocinador: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar patrocinador"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o patrocinador.')})

def sponsor_update(request, id):
    try:
        sponsor = get_object_or_404(Sponsor, id=id)
        if request.method == 'POST':
            form = SponsorForm(request.POST, request.FILES, instance=sponsor)
            if form.is_valid():
                form.save()
                return redirect('sponsor_list')
        else:
            form = SponsorForm(instance=sponsor)
        return render(request, 'sponsors/sponsor_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar patrocinador: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar patrocinador"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o patrocinador.')})

def sponsor_delete(request, id):
    try:
        sponsor = get_object_or_404(Sponsor, id=id)
        if request.method == 'POST':
            sponsor.delete()
            return redirect('sponsor_list')
        return render(request, 'sponsors/sponsor_confirm_delete.html', {'sponsor': sponsor})
    except Exception as e:
        logger.error(_("Erro ao deletar patrocinador: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar patrocinador"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o patrocinador.')})

def register(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=False)
                    user.is_staff = True
                    user.save()
                    admin_group, created = Group.objects.get_or_create(name='admin')
                    user.groups.add(admin_group)
                    messages.success(request, _('Usuário registrado com sucesso!'))
                    return redirect('login')
                except IntegrityError:
                    form.add_error('email', _('Um usuário com este email já existe.'))
        else:
            form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao registrar usuário: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao registrar usuário"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao registrar o usuário.')})
    
def user_login(request):
    try:
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
        else:
            form = CustomAuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao fazer login: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao fazer login"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao fazer login.')})

def user_logout(request):
    try:
        if request.method == 'POST':
            logout(request)
            return redirect('index')
        elif request.method == 'GET':
            logout(request)
            return redirect('index')
        return redirect('index')
    except Exception as e:
        logger.error(_("Erro ao fazer logout: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao fazer logout"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao fazer logout.')})

@login_required
def user_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return render(request, 'user_profile/profile.html', {'profile': profile})
    except Exception as e:
        logger.error(_("Erro ao carregar perfil do usuário: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar perfil do usuário"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar o perfil do usuário.')})

@login_required
def edit_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = UserProfileForm(instance=profile, user=request.user)
        return render(request, 'user_profile/profile_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao editar perfil: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao editar perfil"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao editar o perfil.')})

@login_required
def delete_profile(request):
    try:
        profile = get_object_or_404(UserProfile, user=request.user)
        if request.method == 'POST':
            user = request.user
            profile.delete()
            user.delete()
            logout(request)
            return redirect('login')
        return render(request, 'user_profile/profile_confirm_delete.html', {'profile': profile})
    except Exception as e:
        logger.error(_("Erro ao deletar perfil: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar perfil"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o perfil.')})

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/custom_password_reset.html'
    email_template_name = 'registration/custom_password_reset_email.html'
    subject_template_name = 'registration/custom_password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/custom_password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/custom_password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        try:
            if form.cleaned_data['new_password1'] != form.cleaned_data['new_password2']:
                form.add_error('new_password2', _('As senhas não coincidem.'))
                return self.form_invalid(form)

            if self.request.user.is_authenticated:
                if self.request.user.check_password(form.cleaned_data['new_password1']):
                    form.add_error('new_password1', _('A nova senha não pode ser igual à senha antiga.'))
                    return self.form_invalid(form)

            return super().form_valid(form)
        except Exception as e:
            logger.error(_("Erro na confirmação de redefinição de senha: {e}").format(e=e), exc_info=True)
            mail_admins(_("Erro na confirmação de redefinição de senha"), str(e))
            return self.form_invalid(form)

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/custom_password_reset_complete.html'

def password_reset_error(request):
    return render(request, 'registration/custom_password_reset_error.html')

def send_test_email(request):
    try:
        send_mail(
            _('Email de Teste'),
            _('Este é um email de teste enviado pelo Django.'),
            settings.DEFAULT_FROM_EMAIL,
            ['beniciosanca224@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse(_("Email de teste enviado com sucesso!"))
    except Exception as e:
        logger.error(_("Erro ao enviar email de teste: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao enviar email de teste"), str(e))
        return HttpResponse(_("Falha ao enviar email de teste."))

@admin_required(login_url='login')
def register_member(request):
    try:
        if request.method == 'POST':
            form = MemberForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('list_members')
        else:
            form = MemberForm()
        return render(request, 'members/register_member.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao registrar membro: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao registrar membro"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao registrar o membro.')})

@admin_required(login_url='login')
def add_member(request):
    try:
        if request.method == 'POST':
            form = MemberForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('list_members')
        else:
            form = MemberForm()
        return render(request, 'members/register_member.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao adicionar membro: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao adicionar membro"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao adicionar o membro.')})

@admin_required(login_url='login')
def list_members(request):
    try:
        members = Member.objects.all()
        return render(request, 'members/list_members.html', {'members': members})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de membros: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de membros"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de membros.')})

@admin_required(login_url='login')
def download_members_excel(request):
    try:
        members = Member.objects.all().values(
            'full_name', 'birth_date', 'document_number', 'document_type', 'document_validity', 
            'nationality', 'gender', 'other_gender', 'address', 'postal_code', 'city', 'phone', 
            'email', 'is_student', 'school', 'education_type', 'course', 'academic_year', 
            'is_scholar', 'is_working_student', 'occupation', 'status'
        )

        df = pd.DataFrame(list(members))

        df['document_type'] = df['document_type'].map(dict(Member.DOCUMENT_TYPE_CHOICES))
        df['gender'] = df['gender'].map(dict(Member.GENDER_CHOICES))
        df['education_type'] = df['education_type'].map(dict(Member.EDUCATION_TYPE_CHOICES))
        df['status'] = df['status'].map(dict(Member.STATUS_CHOICES))

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = _('attachment; filename=membros.xlsx')

        df.to_excel(response, index=False)

        return response
    except Exception as e:
        logger.error(_("Erro ao baixar Excel de membros: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao baixar Excel de membros"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao baixar o arquivo Excel de membros.')})

@admin_required(login_url='login')
def edit_member(request, id):
    try:
        member = get_object_or_404(Member, id=id)
        if request.method == 'POST':
            form = MemberForm(request.POST, instance=member)
            if form.is_valid():
                form.save()
                return redirect('list_members')
        else:
            form = MemberForm(instance=member)
        return render(request, 'members/edit_member.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao editar membro: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao editar membro"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao editar o membro.')})

@admin_required(login_url='login')
def delete_member(request, id):
    try:
        member = get_object_or_404(Member, id=id)
        if request.method == 'POST':
            member.delete()
            return redirect('list_members')
        return render(request, 'members/confirm_delete.html', {'member': member})
    except Exception as e:
        logger.error(_("Erro ao deletar membro: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar membro"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o membro.')})

@admin_required(login_url='login')
def list_pending_members(request):
    try:
        members = Member.objects.filter(status='pending')
        return render(request, 'members/list_pending_members.html', {'members': members})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de membros pendentes: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de membros pendentes"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de membros pendentes.')})

@admin_required(login_url='login')
def approve_member(request, id):
    try:
        member = get_object_or_404(Member, id=id)
        if request.method == 'POST':
            member.status = 'approved'
            member.save()
            send_member_status_email(member, 'approved')
            return redirect('list_pending_members')
        return render(request, 'members/approve_member.html', {'member': member})
    except Exception as e:
        logger.error(_("Erro ao aprovar membro: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao aprovar membro"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao aprovar o membro.')})

@admin_required(login_url='login')
def reject_member(request, id):
    try:
        member = get_object_or_404(Member, id=id)
        if request.method == 'POST':
            send_member_status_email(member, 'rejected')
            member.delete()
            return redirect('list_pending_members')
        return render(request, 'members/reject_member.html', {'member': member})
    except Exception as e:
        logger.error(_("Erro ao rejeitar membro: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao rejeitar membro"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao rejeitar o membro.')})

@admin_required(login_url='login')
def member_detail(request, id):
    try:
        member = get_object_or_404(Member, id=id)
        return render(request, 'members/member_detail.html', {'member': member})
    except Exception as e:
        logger.error(_("Erro ao carregar detalhes do membro: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar detalhes do membro"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar os detalhes do membro.')})

@admin_required(login_url='login')
def member_detail_pend(request, id):
    try:
        member = get_object_or_404(Member, id=id)
        return render(request, 'members/member_detail_pend.html', {'member': member})
    except Exception as e:
        logger.error(_("Erro ao carregar detalhes do membro pendente: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar detalhes do membro pendente"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar os detalhes do membro pendente.')})

def send_member_status_email(member, status):
    subject = _("Status da sua inscrição: {status}").format(status=status)
    if status == 'approved':
        message = _("Olá {name},\n\nSua inscrição foi aprovada com sucesso. Parabéns e seja bem-vindo!").format(name=member.full_name)
    else:
        message = _("Olá {name},\n\nInfelizmente, sua inscrição foi rejeitada. Agradecemos pelo seu interesse.").format(name=member.full_name)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [member.email],
        fail_silently=False,
    )

@login_required
def privacy_policy_list(request):
    try:
        policies = PrivacyPolicy.objects.all().order_by('-last_updated')
        return render(request, 'privacy_policy/privacy_policy_list.html', {'policies': policies})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de políticas de privacidade: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de políticas de privacidade"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de políticas de privacidade.')})

@login_required
def privacy_policy_detail(request, id):
    try:
        policy = get_object_or_404(PrivacyPolicy, id=id)
        return render(request, 'privacy_policy/privacy_policy_detail.html', {'policy': policy})
    except Exception as e:
        logger.error(_("Erro ao carregar detalhes da política de privacidade: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar detalhes da política de privacidade"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar os detalhes da política de privacidade.')})

@login_required
def privacy_policy_create(request):
    try:
        if request.method == 'POST':
            form = PrivacyPolicyForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('privacy_policy_list')
        else:
            form = PrivacyPolicyForm()
        return render(request, 'privacy_policy/privacy_policy_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar política de privacidade: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar política de privacidade"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a política de privacidade.')})

@login_required
def privacy_policy_update(request, id):
    try:
        policy = get_object_or_404(PrivacyPolicy, id=id)
        if request.method == 'POST':
            form = PrivacyPolicyForm(request.POST, instance=policy)
            if form.is_valid():
                form.save()
                return redirect('privacy_policy_list')
        else:
            form = PrivacyPolicyForm(instance=policy)
        return render(request, 'privacy_policy/privacy_policy_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar política de privacidade: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar política de privacidade"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a política de privacidade.')})

@login_required
def privacy_policy_delete(request, id):
    try:
        policy = get_object_or_404(PrivacyPolicy, id=id)
        if request.method == 'POST':
            policy.delete()
            return redirect('privacy_policy_list')
        return render(request, 'privacy_policy/privacy_policy_confirm_delete.html', {'policy': policy})
    except Exception as e:
        logger.error(_("Erro ao deletar política de privacidade: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar política de privacidade"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a política de privacidade.')})

def custom_set_language(request):
    try:
        if request.method == 'POST':
            user_language = request.POST.get('language')
            if user_language and user_language in dict(settings.LANGUAGES).keys():
                translation.activate(user_language)
                request.session[settings.LANGUAGE_COOKIE_NAME] = user_language  # Corrigido para usar LANGUAGE_COOKIE_NAME
                messages.success(request, _("Idioma alterado com sucesso."))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        logger.error(_("Erro ao definir o idioma: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao definir o idioma"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao definir o idioma.')})


@login_required
def contact_info_list(request):
    try:
        contacts = ContactInfo.objects.all()
        return render(request, 'contact/contact_info_list.html', {'contacts': contacts})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de informações de contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de informações de contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de informações de contato.')})

@login_required
def contact_info_create(request):
    try:
        if request.method == 'POST':
            form = ContactInfoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('contact_info_list')
        else:
            form = ContactInfoForm()
        return render(request, 'contact/contact_info_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar informação de contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar informação de contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a informação de contato.')})

@login_required
def contact_info_update(request, id):
    try:
        contact_info = get_object_or_404(ContactInfo, id=id)
        if request.method == 'POST':
            form = ContactInfoForm(request.POST, instance=contact_info)
            if form.is_valid():
                form.save()
                return redirect('contact_info_list')
        else:
            form = ContactInfoForm(instance=contact_info)
        return render(request, 'contact/contact_info_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar informação de contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar informação de contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a informação de contato.')})

@login_required
def contact_info_delete(request, id):
    try:
        contact_info = get_object_or_404(ContactInfo, id=id)
        if request.method == 'POST':
            contact_info.delete()
            return redirect('contact_info_list')
        return render(request, 'contact/contact_info_confirm_delete.html', {'contact_info': contact_info})
    except Exception as e:
        logger.error(_("Erro ao deletar informação de contato: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar informação de contato"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a informação de contato.')})

@login_required
@login_required
def about_list(request):
    try:
        about_items = About.objects.all()  # Certifique-se de que essa linha corresponde ao que você espera no template.
        return render(request, 'about/about_list.html', {'about_items': about_items})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de sobre: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de sobre"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de sobre.')})

    
def about_detail(request, id):
    try:
        about_item = get_object_or_404(About, id=id)
        return render(request, 'about/about_detail.html', {'about_item': about_item})
    except Exception as e:
        logger.error(_("Erro ao carregar detalhes sobre: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar detalhes sobre"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar os detalhes sobre.')})

@login_required
def about_create(request):
    try:
        if request.method == 'POST':
            form = AboutForm(request.POST, request.FILES)  # Inclua request.FILES para capturar o upload da imagem
            if form.is_valid():
                form.save()
                return redirect('about_list')
        else:
            form = AboutForm()
        return render(request, 'about/about_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar sobre: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar sobre"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar o sobre.')})

@login_required
def about_update(request, id):
    try:
        about = get_object_or_404(About, id=id)
        if request.method == 'POST':
            form = AboutForm(request.POST, request.FILES, instance=about)  # Inclua request.FILES para capturar o upload da imagem
            if form.is_valid():
                form.save()
                return redirect('about_list')
        else:
            form = AboutForm(instance=about)
        return render(request, 'about/about_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar sobre: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar sobre"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar o sobre.')})

@login_required
def about_delete(request, id):
    try:
        about = get_object_or_404(About, id=id)
        if request.method == 'POST':
            about.delete()
            return redirect('about_list')
        return render(request, 'about/about_confirm_delete.html', {'about': about})
    except Exception as e:
        logger.error(_("Erro ao deletar sobre: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar sobre"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar o sobre.')})

def settings_list(request):
    try:
        settings = GeneralSettings.objects.all()
        return render(request, 'settings/settings_list.html', {'settings': settings})
    except Exception as e:
        logger.error(_("Erro ao carregar a lista de configurações: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar a lista de configurações"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de configurações.')})

def settings_create(request):
    try:
        if request.method == 'POST':
            form = GeneralSettingsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('settings_list')
        else:
            form = GeneralSettingsForm()
        return render(request, 'settings/settings_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar configuração: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar configuração"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a configuração.')})

def settings_update(request, id):
    try:
        setting = get_object_or_404(GeneralSettings, id=id)
        if request.method == 'POST':
            form = GeneralSettingsForm(request.POST, instance=setting)
            if form.is_valid():
                form.save()
                return redirect('settings_list')
        else:
            form = GeneralSettingsForm(instance=setting)
        return render(request, 'settings/settings_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar configuração: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar configuração"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a configuração.')})

def settings_delete(request, id):
    try:
        setting = get_object_or_404(GeneralSettings, id=id)
        if request.method == 'POST':
            setting.delete()
            return redirect('settings_list')
        return render(request, 'settings/settings_confirm_delete.html', {'setting': setting})
    except Exception as e:
        logger.error(_("Erro ao deletar configuração: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar configuração"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a configuração.')})

@login_required
def social_media_list(request):
    try:
        social_medias = SocialMedia.objects.all()
        return render(request, 'social_media/social_media_list.html', {'social_medias': social_medias})
    except Exception as e:
        logger.error(_("Erro ao carregar lista de redes sociais: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao carregar lista de redes sociais"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao carregar a lista de redes sociais.')})

@login_required
def social_media_create(request):
    try:
        if request.method == 'POST':
            form = SocialMediaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('social_media_list')
        else:
            form = SocialMediaForm()
        return render(request, 'social_media/social_media_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao criar rede social: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao criar rede social"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao criar a rede social.')})

@login_required
def social_media_update(request, id):
    try:
        social_media = get_object_or_404(SocialMedia, id=id)
        if request.method == 'POST':
            form = SocialMediaForm(request.POST, instance=social_media)
            if form.is_valid():
                form.save()
                return redirect('social_media_list')
        else:
            form = SocialMediaForm(instance=social_media)
        return render(request, 'social_media/social_media_form.html', {'form': form})
    except Exception as e:
        logger.error(_("Erro ao atualizar rede social: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao atualizar rede social"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao atualizar a rede social.')})

@login_required
def social_media_delete(request, id):
    try:
        social_media = get_object_or_404(SocialMedia, id=id)
        if request.method == 'POST':
            social_media.delete()
            return redirect('social_media_list')
        return render(request, 'social_media/social_media_confirm_delete.html', {'social_media': social_media})
    except Exception as e:
        logger.error(_("Erro ao deletar rede social: {e}").format(e=e), exc_info=True)
        mail_admins(_("Erro ao deletar rede social"), str(e))
        return render(request, 'error.html', {'message': _('Ocorreu um erro ao deletar a rede social.')})
    

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            subject = data['subject']
            message = data['message']
            
            send_mail(
                subject,
                message,
                'aegbsuporte@gmail.com',  # Coloque aqui o mesmo email configurado no settings.py
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': _('Email enviado com sucesso!')}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': _('Método não permitido')}, status=405)

def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    response = HttpResponse(document.file, content_type='application/octet-stream')
    response['Content-Disposition'] = _('attachment; filename="{filename}"').format(filename=document.file.name)
    return response
