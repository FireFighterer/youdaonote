from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.db.models import Model
from . import  models
# Create your views here.
from django.http import HttpResponseRedirect
from django.db.models import F
from django.core.paginator import Paginator
from userinfo import models as usermodels
import os,sys

from django.conf import settings



def add_note(request):

     if 'userinfo' not in request.session:
        return Http404
     username = request.session["userinfo"]["username"]
     if request.method == "GET":
         return  render(request,"add_note.html",locals())
     elif request.method == "POST":
         title=request.POST.get("title")
         content=request.POST.get("content")
         file=None
         try:
            file=request.FILES["file"]
            print("文件名是",file)
         except:
             pass
         else:
             #creat user'dir if it not exist'
             userfiles=settings.USER_FILE+"/"+request.session['userinfo']["username"]
             if not os.path.exists(userfiles):
                       os.makedirs(userfiles)

             useraccessoryfiles=userfiles+"/"+str(len(models.Note.objects.filter(owner_id=request.session["userinfo"]["id"]))+1)
             if not os.path.exists(useraccessoryfiles):
                       os.makedirs(useraccessoryfiles)
             # create same name file to save upload file
             with open(useraccessoryfiles+"/"+file.name,"wb") as f:
                 f.write(file.file.read())

         models.Note.objects.create(
                                    title=title,
                                    content=content.encode(),
                                    owner=usermodels.User.objects.get(name=request.session["userinfo"]["username"]),
                                    accessory_file=None if file==None else file.name,
                                    accessory_id=None if file==None else len(models.Note.objects.filter(owner_id=request.session["userinfo"]["id"]))+1
         )

         return HttpResponseRedirect("list_note")

def look_note(request,id):
    if 'userinfo' not in request.session:
        return Http404
    username = request.session["userinfo"]["username"]
    if request.method=="GET":
        note=models.Note.objects.get(id=id)
        title =note.title
        content = note.content
        accessory_file=note.accessory_file
        is_exit=0 if not accessory_file else 1
        accessory_id=note.accessory_id
        username = request.COOKIES.get("username", "")
        print("username",username)
        # # 复原STATICFILES_DIRS
        # settings.STATICFILES_DIRS=[os.path.join(settings.BASE_DIR,'static')]
        # 将当前用户的附件所在的文件夹动态添加到静态文件路径里
        # settings.STATICFILES_DIRS.append(settings.USER_FILE+"/"+username+"/"+str(note.accessory_id))
        # print(settings.STATICFILES_DIRS)

        return render(request,"look_note.html",locals())

# def accessory(request):
#     if 'userinfo' not in request.session:
#         return Http404
#     accessory_file=request.GET.get("accessory_file","")
#     username=request.COOKIES.get("username","")
#
#     # 将当前用户的附件所在的文件夹动态添加到静态文件路径里
#     settings.STATICFILES_DIRS.append(settings.USER_FILE+"/"+username)
#     print(settings.USER_FILE+"/"+username+"/"+accessory_file)
#
#     return HttpResponseRedirect(accessory_file)


def modify_note(request,id):
    if 'userinfo' not in request.session:
        return Http404
    username = request.session["userinfo"]["username"]
    if request.method=="GET":
        note=models.Note.objects.get(id=id)
        title =note.title
        content = note.content
        accessory_file = note.accessory_file
        accessory_id = note.accessory_id
        is_exit = 0 if not accessory_file else 1
        # # 复原STATICFILES_DIRS
        # settings.STATICFILES_DIRS = [os.path.join(settings.BASE_DIR, 'static')]
        # # 将当前用户的附件所在的文件夹动态添加到静态文件路径里
        # settings.STATICFILES_DIRS.append(settings.USER_FILE + "/" + username + "/" + str(note.accessory_id))
        # print(settings.STATICFILES_DIRS)
        return render(request,"modify_note.html",locals())
    elif request.method=="POST":
        file = None
        try:
            file = request.FILES["upfile"]
            print("文件名是", file)
        except:
            pass
        else:
            # creat user'dir if it not exist'
            userfiles = settings.USER_FILE + "/" + request.session['userinfo']["username"]
            if not os.path.exists(userfiles):
                os.makedirs(userfiles)

            useraccessoryfiles = userfiles + "/" + str(
                len(models.Note.objects.filter(owner_id=request.session["userinfo"]["id"])) + 1)
            if not os.path.exists(useraccessoryfiles):
                os.makedirs(useraccessoryfiles)
            # create same name file to save upload file
            with open(useraccessoryfiles + "/" + file.name, "wb") as f:
                f.write(file.file.read())
        note=models.Note.objects.get(id=id)
        note.content=request.POST.get("content").encode()
        note.accessory_file=file
        note.accessory_id=len(models.Note.objects.filter(owner_id=request.session["userinfo"]["id"])) + 1
        note.save()
        return HttpResponseRedirect("/note/list_note")

def delete_accessory(request,id):
    username = request.session["userinfo"]["username"]
    note = models.Note.objects.get(id=id)
    accessory_file = note.accessory_file

    if not accessory_file==None:
        os.remove(settings.USER_FILE+"/"+username+"/"+str(note.accessory_id)+"/"+str(accessory_file))
        if  note.accessory_id:
            os.rmdir(settings.USER_FILE + "/" + username + "/" + str(note.accessory_id))
    note.accessory_file=None
    note.accessory_id=None
    note.save()
    return HttpResponseRedirect("/note/look_note/%d"%(note.id))

def delete_note(request,id):
    if 'userinfo' not in request.session:
        return Http404
    note = models.Note.objects.get(id=id)
    if note.accessory_id:
        delete_accessory(request, id)
    note.delete()
    return HttpResponseRedirect("/note/list_note")

def list_note(request):
      if 'userinfo' not in request.session:
        return Http404
      username=request.session["userinfo"]["username"]

      notes=models.Note.objects.filter(owner_id=request.session["userinfo"]["id"])
      paginator=Paginator(notes,5)

      cur_page=request.GET.get("page",1)

      page=paginator.page(cur_page)
      return render(request,"list_note.html",locals())

def search_note(request):
    if 'userinfo' not in request.session:
        return Http404
    username = request.session["userinfo"]["username"]
    if request.method=="GET":
        return render(request,"search_note.html")
    elif request.method=="POST":
        name=request.POST.get("name")
        notes=models.Note.objects.filter(name__contains=name)
        return render(request,"search_note.html",locals())

