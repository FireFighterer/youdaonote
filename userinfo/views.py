from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from . import models

def mylogin(request):
    if request.method=="GET":
        username=request.COOKIES.get("username","")
        password=request.COOKIES.get("password","")
        remember=request.COOKIES.get("remember","")
        res = render(request,"userinfo/login.html",locals())
        if remember=="":
            res.set_cookie('remember', value=0, max_age=7 * 24 * 3600)

        return res
    elif request.method == "POST":
        # 获取表单数据
        remember=request.POST.get('remember',"")
        username=request.POST.get('username',"")
        password=request.POST.get('password',"")

        # 验证用户名，密码是否正确
        try:
            user=models.User.objects.get(name=username,password=password)
            request.session['userinfo']={
                "username":user.name,
                "id":user.id
            }
        except:

            return  render(request,"userinfo/login.html",{"status":0})
        res = HttpResponseRedirect("/note/add_note")
        # 处理cookies
        if not remember=="0":
            res.set_cookie('username',value=username,max_age=7*24*3600)
            res.set_cookie('password',value=password,max_age=7*24*3600)
            res.set_cookie('remember',value=remember,max_age=7*24*3600)
        else:
            res.delete_cookie('username')
            res.delete_cookie('password')
            res.delete_cookie('remember')
        return res


def register(request):
    if request.method=="GET":
        return render(request,"userinfo/register.html")
    elif request.method=="POST":
        username=request.POST.get("username","")
        password=request.POST.get("password","")
        password_again=request.POST.get("password_again","")

        #简单演示表单验证，实际应用中是在数据表中限制的
        if username=="":
            username_error="用户名不能为空！"
            return  render(request,"userinfo/register.html",locals())
        if password=="":
            password_error = "密码不能为空！"
            return render(request, "userinfo/register.html", locals())
        if password!=password_again:
            password_again_error = "密码不一致！"
            return render(request, "userinfo/register.html", locals())

        try:
            user=models.User.objects.create(name=username,password=password)

            return HttpResponseRedirect("/userinfo/logout")
        except:
            return render(request, "userinfo/register.html", {"success":0})

def mylogout(request):
    """退出登录"""
    if 'userinfo' in request.session:
        del request.session['userinfo']
    return HttpResponseRedirect('/')

