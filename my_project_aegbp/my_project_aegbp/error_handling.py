from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
import logging
import traceback

logger = logging.getLogger(__name__)

def handle_404(request, exception):
    """
    Handle 404 errors.
    """
    context = {'error_code': 404, 'error_message': 'Page not found'}
    return render(request, 'errors/404.html', context)

def handle_500(request):
    """
    Handle 500 errors.
    """
    context = {'error_code': 500, 'error_message': 'Internal server error'}
    log_error(request, context['error_message'])
    return render(request, 'errors/500.html', context)

def handle_permission_denied(request, exception):
    """
    Handle 403 errors.
    """
    context = {'error_code': 403, 'error_message': 'Permission denied'}
    return render(request, 'errors/403.html', context)

def handle_bad_request(request, exception):
    """
    Handle 400 errors.
    """
    context = {'error_code': 400, 'error_message': 'Bad request'}
    return render(request, 'errors/400.html', context)

def log_error(request, error_message):
    """
    Log errors and notify admins.
    """
    exception_info = traceback.format_exc()
    request_info = f"Path: {request.path}\nMethod: {request.method}\nGET: {request.GET}\nPOST: {request.POST}"
    full_message = f"{error_message}\n\nException Information:\n{exception_info}\n\nRequest Information:\n{request_info}"

    # Log the error
    logger.error(full_message)

    # Send email to admins
    if settings.DEBUG is False:  # Only send emails if DEBUG is False
        send_mail(
            subject=f"Error Notification: {error_message}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin[1] for admin in settings.ADMINS],
            fail_silently=False,
        )
