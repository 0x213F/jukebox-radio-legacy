from django.shortcuts import render


def handler_500(request):
    return render(request, "500.html", status=404)
