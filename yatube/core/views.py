from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def permission_denied_view(request, reason=''):
    return render(request, 'core/403csrf.html')


def internal_server_error_view(request):
    return render(request, 'core/500.html', status=500)
