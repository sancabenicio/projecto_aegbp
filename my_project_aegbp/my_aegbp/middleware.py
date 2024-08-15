from .views import get_total_notifications
import logging
from django.core.mail import mail_admins
from django.http import JsonResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.notifications = get_total_notifications()
        else:
            request.notifications = {'total_notifications': 0, 'new_contacts': [], 'pending_members': []}
        response = self.get_response(request)
        return response
    
class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Tratamento de erro 404 (Página não encontrada)
        if isinstance(exception, Http404):
            return render(request, 'errors/404.html', status=404)
        
        # Tratamento de erro 403 (Acesso proibido)
        if isinstance(exception, PermissionDenied):
            return render(request, 'errors/403.html', status=403)
        
        # Tratamento de erro 400 (Requisição inválida)
        if isinstance(exception, HttpResponseBadRequest):
            return render(request, 'errors/400.html', status=400)

        # Tratamento de erro 500 (Erro do servidor)
        logger.error(_("Exceção ocorreu: %(error)s") % {'error': exception}, exc_info=True)
        mail_admins(
            subject=_('Exceção ocorreu'),
            message=_('Erro: %(error)s\nURL: %(url)s') % {'error': exception, 'url': request.build_absolute_uri()},
        )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': _('Ocorreu um erro inesperado.')}, status=500)
        
        return render(request, 'errors/500.html', status=500)
