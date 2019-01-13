
from django.template.response import TemplateResponse


def privacy_policy_view(request):
    return TemplateResponse(request, 'privacy_policy.html')
