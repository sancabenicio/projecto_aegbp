from .models import SocialMedia
from django.utils.translation import gettext_lazy as _

def dashboard_cards(request):
    cards = [
        {"icon": "fa-camera", "color": "text-primary", "btn_color": "primary", "title": _("Galeria de Fotos"), "description": _("Veja as fotos mais recentes da nossa atividade."), "view_url": "photo_gallery", "create_url": "photo_create"},
        {"icon": "fa-video", "color": "text-info", "btn_color": "info", "title": _("Galeria de Vídeos"), "description": _("Assista aos vídeos mais recentes da nossa atividade."), "view_url": "video_gallery", "create_url": "video_create"},
        {"icon": "fa-calendar-alt", "color": "text-success", "btn_color": "success", "title": _("Calendário"), "description": _("Confira os próximos eventos e atividades."), "view_url": "calendar_view", "create_url": "event_create"},
        {"icon": "fa-file-alt", "color": "text-warning", "btn_color": "warning", "title": _("Documentos"), "description": _("Acesse os documentos importantes e relatórios."), "view_url": "document_list", "create_url": "document_create"},
        {"icon": "fa-blog", "color": "text-secondary", "btn_color": "secondary", "title": _("Blog"), "description": _("Leia as últimas postagens no nosso blog."), "view_url": "blog_list", "create_url": "blog_create"},
        {"icon": "fa-comments", "color": "text-teal", "btn_color": "teal", "title": _("Testemunhos"), "description": _("Leia os testemunhos de nossos membros."), "view_url": "testimonials", "create_url": "testimonial_create"},
        {"icon": "fa-question-circle", "color": "text-purple", "btn_color": "purple", "title": _("FAQs"), "description": _("Respostas para as perguntas mais frequentes."), "view_url": "faqs", "create_url": "faq_create"},
        {"icon": "fa-hands-helping", "color": "text-orange", "btn_color": "orange", "title": _("Oportunidades de Voluntariado"), "description": _("Participe como voluntário em nossos projetos."), "view_url": "volunteer_opportunities", "create_url": "volunteer_create"},
        {"icon": "fa-tasks", "color": "text-blue", "btn_color": "blue", "title": _("Projetos"), "description": _("Conheça os projetos que estamos desenvolvendo."), "view_url": "project_list", "create_url": "project_create"},
        {"icon": "fa-donate", "color": "text-pink", "btn_color": "pink", "title": _("Doações"), "description": _("Apoie nossa atividade com sua doação."), "view_url": "donation_list", "create_url": "donation_create"},
        {"icon": "fa-handshake", "color": "text-brown", "btn_color": "brown", "title": _("Patrocinadores"), "description": _("Conheça nossos patrocinadores."), "view_url": "sponsor_list", "create_url": "sponsor_create"},
    ]
    return {"cards": cards}

def base_context(request):
    social_medias = SocialMedia.objects.all()
    return {
        'social_medias': social_medias,
    }
