from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin


class MyMiddleAware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        # print("init1")

    # view处理请求前执行
    def process_request(self, request):#强制登录判断
        if 'login' in request.path or 'regist' in request.path or \
                        'captcha' in request.path or 'user'in request.path:
                    return
        else:
            #获取session
            if request.session.get('flag')=="ok":
                pass
                # return redirect('loginapp:emplist')
            else:
                return redirect('loginapp:login')


    # view执行之后，响应之前执行
    def process_response(self, request, response):
        # print("response:", request, response)
        return response  # 必须返回response

