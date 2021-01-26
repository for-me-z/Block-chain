from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from .models import CCITUser, AClass, AStudent

# Create your views here.

def index(request):
    return render(request, 'login_js.html')

def userLogin(request):
    result = {'status':'error',"content":"请求过来了"}
    if request.method == "POST":

        post_data = request.POST
        print(post_data)
        if post_data:
            user = queryUser(post_data)
            if user:
                if user.upwd == post_data['upwd']:
                    result['isUser'] = True
                    result['msg'] = '欢迎登陆'
                    result['user'] = {
                        'uid': user.uID
                    }
                    # 设置绘画 session
                    request.session['userStatus'] = True
                    # 设置当前 key 有效期
                    request.session.set_expiry(3600)
                else:
                    result['isUser'] = False
                    result['msg'] = '密码错误'
            else:
                result['isUser'] = False
                result['msg'] = '用户名不存在，请联系系统管理员'           
    else:
        result['msg'] = '请求Method不正确，请使用POST请求'
        result['content'] = '服务器响应' 

    return JsonResponse(result)

def homePage(request, uid):
    print('uid:', uid)
    
    # 验证会话是否合法
    isUser = request.session.get('userStatus')
    if isUser == None:
        return render(request, '404.html', {'msg': u'要不要脸，登nm呢'})
    
    #获取班级
    try:
        #做正确的事情
        # 拿到所有班级
        citems = CCITUser.objects.get(uID=uid).cls.all()
        print(citems)
    except:
        #做错误的事情
        print(u'用户不存在')
        return render(request, '404.html', {'msg':u'班级管理员账号异常，不存在'})

# 获取所有学生
    all_student = []
    for citem in citems:
        try:
            stus = AClass.objects.get(cID=citem.cID).stu.all()
            print(stus)
        except:
            return render(request, '404.html', {'msg': u'当前班级学生信息有误,请联系管理员'})
        

    data = {
        'citems': citems,
        'uid': uid
    }    
    return render(request, 'index.html', data)


def queryUser(user):
    try:
        find_user = CCITUser.objects.get(uID=user['uname'])
        return find_user
    except CCITUser.DoesNotExist:
        print(u'用户不存在')
    return None           

def getAllUser():
    all_users = CCITUser.objects.all()
    datas = []
    if all_users:
        for item in all_users:
            obj = {}
            obj['uID'] = item.uID
            obj['uname'] = item.uname
            obj['uemail'] = item.uemail

            obj['regtime'] = dateToString(item.uregisteredtime)
            obj['ustatus'] = item.ustatus
            datas.append(obj)
        return datas
    else:
        return None

def dateToString(date):
    ds = date.strftime('%Y-%m-%d %H:%M:%S')
    return ds

import datetime
def stringToDate(string):
    dt = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S+00:00")
    return dt                

def querySetsUser(user):
    sets = dict()
    sets['uID'] = user['uname']
    sets['upwd'] = user['upwd']
    find_user = CCITUser.objects.filter(**sets)
    if find_user:
        return find_user
    else:
        return None