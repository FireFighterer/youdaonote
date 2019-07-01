from django.shortcuts import render


def startpage(request):
    loged=0
    username=""
    if 'userinfo' in request.session:
        loged=1
        username = request.session["userinfo"]["username"]

    return render(request,"startpage.html",locals())