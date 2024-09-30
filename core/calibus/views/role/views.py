from django.shortcuts import render


def role_list(request):
    data = {

    }
    return render(request, 'role/list.html', data)
