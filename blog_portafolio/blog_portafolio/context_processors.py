from django.contrib.auth.models import User


def project_context(request):
    context = {
        'yo': User.objects.first(),
    }

    return context
