from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from loginapp.models import User,Employee
import random,string
from loginapp.captcha.image import ImageCaptcha
import uuid,os,json
# Create your views here.

#进入注册页面
def regist(request):
    msg=request.POST.get('msg')
    if msg:
        return render(request,'ems/regist.html',{'msg':msg})
    else:
        return render(request,'ems/regist.html')

def user(request):
    # 获取用户名
    username=request.POST.get('name')
    if len(username)!=0:
        # 数据库中查找
        us = User.objects.filter(user=username)
        if us:
            # 用户名存在
            return HttpResponse('用户名已存在')
        # 用户不存在
        else:
            return HttpResponse("用户名合法")
    else:
        return HttpResponse('用户名不能为空')

# 生成验证码
def getcaptcha(request):
    # 为验证码设置字体，默认获取当前目录下的segoesc.ttf文件
    image=ImageCaptcha()
    # 获取随机码
    #字母大小写+数字，随机抽取5位作为验证码['x','x','x','x','x']
    code=random.sample(string.ascii_letters+string.digits,5)
    #将获得的验证码拼接在一起
    code=''.join(code)
    print(code)
    #将验证码存入session，以备后继判断使用
    request.session['code']=code
    #将生成的随机字符拼接成字符串，作为验证码图片中的文本
    data=image.generate(code)
    #写出验证码图片，给客户端
    return HttpResponse(data,'image/png')

def captchalogic(request):
    # 获取用户输入的验证码
    code = request.POST.get('num')
    # 将存入session的验证码取出
    session_code = request.session.get('code')
    if code.lower() == session_code.lower():
        return HttpResponse('验证码正确')
    else:
        return HttpResponse('验证码不正确')


#进入注册页面，获取用户名、姓名、密码、性别
def registlogic(request):
    # 获取用户名
    username=request.POST.get('name')
    # # 数据库中查找
    us = User.objects.filter(user=username)
    if us:
    #     # 用户名存在
        return redirect('loginapp:regist')
    # # 用户不存在
    else:
        # 获取用户名
        username=request.POST.get('name')
        name = request.POST.get('name')
        password1 = request.POST.get('pwd1')
        password2 = request.POST.get('pwd2')
        sex = request.POST.get('sex')
        # 获取用户输入的验证码
        code = request.POST.get('number')
        # 将存入session的验证码取出
        session_code = request.session.get('code')
        # 进入数据库中查询：用户名是否存在
        # 判断验证码是否输入有误
        if password2==password1:
            if code.lower() == session_code.lower():
                User.objects.create(user=username, name=name, password=password1, sex=sex)
                return redirect('loginapp:login')
            else:
                return redirect('loginapp:login')
        else:

            return redirect('loginapp:regist')


def login(request):
    name=request.COOKIES.get('name')
    password=request.COOKIES.get('password')
    user=User.objects.filter(name=name,password=password)
    if user:
        request.session['flag']='ok'
        return redirect('loginapp:emplist')
    else:
        return render(request,"ems/login.html")

def loginlogic(request):
    name=request.GET.get('name')
    password=request.GET.get('password')
    print(password)
    checkbox=request.GET.get('checkbox')

    res=redirect('loginapp:emplist')
    request.session['flag']='ok'
    if checkbox:
        res.set_cookie('name',name,max_age=600)
        res.set_cookie('password',password,max_age=600)
    return res

def logincheck(request):
    name = request.POST.get('name')
    password = request.POST.get('pwd')
    checkbox = request.POST.get('checkbox')
    user = User.objects.filter(name=name, password=password)
    if user:
        return HttpResponse('成功')

    else:
        return HttpResponse('用户名或密码错误！')





#职工列表
def emplist(request):
    number = request.GET.get('num')

    print(number)
    if number == None:
        number = 1
    # 查询数据库中所有的职工信息,分页
    pagtor = Paginator(Employee.objects.all(), per_page=3)
    page = pagtor.page(number)  # 某一页的page对象
    # #将查询到的职工信息全部显示在浏览器页面上，通过{ }进行传参
    return render(request, 'ems/emplist.html', {'page': page})

def check(request):
    return render(request,'ems/check.html')

def checkname(request):
    def mydefault(u):
        if isinstance(u,Employee):
            return {'id':u.id,'name':u.name,'salary':str(u.salary),'age':u.age,'pic':u.pic.url}

    name=request.GET.get('name')
    print(name)
    users=Employee.objects.filter(name__contains=name)
    print(users)
    # json序列化
    json_str=json.dumps(list(users),default=mydefault)
    print(json_str)
    # return HttpResponse(json_str)
    return JsonResponse({'users':list(users)},json_dumps_params={'default':mydefault})

# 添加员工信息页面
def addemp(request):
    # 获取页面页数
    num=request.GET.get('num')

    return render(request,'ems/addEmp.html',{'num':num})

#创建唯一的文件名
def generateUUID(filename):
    id=str(uuid.uuid4())
    extend=os.path.splitext(filename)[1]
    return id+extend

# 添加员工信息
def addlogic(request):
    # 获取页面页数
    num=request.GET.get('num')

    # 获取新加的员工姓名、薪水、年龄
    name=request.POST.get('name')
    print(name)
    salary=request.POST.get('salary')
    age = request.POST.get('age')

    # 获取头像照片
    file=request.FILES.get('pic')
    # print(file)
    # 调用自定义的generateUUID生成唯一文件名
    # file.name=generateUUID(file.name)
    file.name=generateUUID(file.name)

    # 将员工信息添加到数据库中
    Employee.objects.create(name=name,salary=salary,age=age,pic=file)
    return redirect('/hello/emplist/?num=%s'%(num))



# 删除员工信息
def delete(request):
    num=request.GET.get('num')
    # 获取要删除员工的id
    id=request.GET.get('id')
    # 通过id来删除员工
    Employee.objects.filter(id=id).delete()
    return redirect('/hello/emplist/?num=%s'%(num))

# 更新员工信息页面
def updateemp(request):
    # 获取要修改员工的id来获得员工的信息，最终显示在浏览器上
    num=request.GET.get('num')
    id=request.GET.get('id')
    user=Employee.objects.get(id=id)
    #通过{ }将要修改的员工信息传到更新页面上
    # return render(request,'ems/updateEmp.html',{'id':id,'name':name,'salary':salary,'age':age})
    return render(request,'ems/updateEmp.html',{'user':user,'id':id,'num':num})
# 更新员工信息
def updalogic(request):
    # 获取要修改员工的信息
    num=request.GET.get('num')
    id=request.GET.get('id')
    # 获取头像照片
    file = request.FILES.get('source')
    name=request.POST.get('name')
    salary=request.POST.get('salary')
    age=request.POST.get('age')
    # 通过id查询数据库，获取员工信息并修改保存
    user = Employee.objects.get(id=id)
    if not file:
        user.name=name
        user.age=age
        user.salary=salary
    else:
        # 调用自定义的generateUUID生成唯一文件名
        file.name=generateUUID(file.name)
        user.pic=file
        user.name=name
        user.age=age
        user.salary=salary
    user.save()
    return redirect('/hello/emplist/?num=%s'%(num))



