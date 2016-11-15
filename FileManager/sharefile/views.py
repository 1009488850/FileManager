from sharefile import models
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth import logout
from sharefile.forms.account import LoginForm
from sharefile.perm_conf import check_permission
from sharefile.forms.account import ChangepwdForm
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from sharefile.models import UpDownFile
from django.contrib.auth.models import User
from sharefile.forms import account as AccountObj
from bootstrap_toolkit.widgets import BootstrapUneditableInput
import os




def AddUserInfo(request):
    pass
    return render(request,'app/admin.html')

def return500(request):
    pass
    return render(request,"app/error500.html")

def show_home(request):
    pass
    return render(request,"app/home.html")

# @check_permission
def show_tables(request):
    try:
        del_fileable = request.user.has_perm('sharefile.del_fileable')
        download_fileable = request.user.has_perm('sharefile.download_fileable')
        upload_fileable = request.user.has_perm('sharefile.upload_fileable')
        perm_dic_ret = [
                    del_fileable,
                    download_fileable,
                    upload_fileable,
                    ]
        if request.method == "POST":
            upload_img_obj = request.FILES.get("f1")
            remove_img_obj = request.POST.get("RemoveImg")
            if upload_img_obj is not None :   # 如果前台页面上传数据非空则进行如下操作；
                if upload_fileable:           # 如果有权限则上传，否则返回无权限页面；
                    return upload_img(request,upload_img_obj)
                else:
                    return render(request,"app/error403.html")
            if remove_img_obj is not None:    # 如果前台上传数据非空且有权限则删除否则返回无权限页面；
                if del_fileable:
                    remove_img(request,remove_img_obj)
                else:
                    return render(request,"app/error403.html")
        file_data = models.UpDownFile.objects.all()
        return render(request,"app/datatables.html",{'filedata':file_data,'perm_dic_ret':perm_dic_ret,})
    except Exception:
        return render(request,"app/error500.html")

def upload_img(request,img_arg):
    file_name, file_size, login_id = img_arg.name, img_arg.__sizeof__(), request.user.userprofile.id
    dic = {'upload_file':file_name, 'upload_user_id':login_id, 'size':file_size}
    # 如果上传文件不重名则创建数据并保存文件，如果重名则执行except；
    try:
        with open("statics/img_dir/%s" %img_arg,'wb') as f:
            for line in img_arg.chunks():
                f.write(line)
        models.UpDownFile.objects.create(**dic)   # 向数据库中创建数据；
        file_data = models.UpDownFile.objects.all()
        return HttpResponseRedirect('/index',RequestContext(file_data))
    except Exception:
        return render(request,"app/error404.html")


def remove_img(request,img_arg):
    img_dir = "statics/img_dir"
    img_dir_arg = img_dir+"//"+img_arg
    os.remove(img_dir_arg)
    models.UpDownFile.objects.filter(upload_file=img_arg).delete()
    file_data = models.UpDownFile.objects.all()
    return render(request,"app/datatables.html",{'filedata':file_data})



def acc_logout(request):
    logout(request)
    file_data = models.UpDownFile.objects.all()
    return render(request,"app/datatables.html",{'filedata':file_data})

def acc_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,"app/signin.html", {'form': form,})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/", RequestContext(request))
            else:
                return render(request,"app/signin.html", {'form': form, 'password_is_wrong':True})
        else:
            return render(request,"app/signin.html", {'form': form,})



@login_required
def changepwd(request):
    if request.method == 'GET':
        form = ChangepwdForm()
        return render(request,"app/changepwd.html",{'form': form,})
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return HttpResponseRedirect("/", RequestContext(request,{'changepwd_success':True}))
            else:
                return render(request,"app/changepwd.html",{'form': form,'oldpassword_is_wrong':True})
        else:
            return render(request,"app/changepwd.html", {'form': form,})






