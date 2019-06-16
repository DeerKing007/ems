from django.urls import path

from loginapp import views


app_name="loginapp"
urlpatterns=[
    path('regist/',views.regist,name='regist'),
    path('user/',views.user,name='user'),
    path('registlogic/',views.registlogic,name='registlogic'),
    path('captcha/',views.getcaptcha,name='getcaptcha'),
    path('captchalogic/',views.captchalogic,name='captchalogic'),
    path('login/',views.login,name='login'),
    path('loginlogic/',views.loginlogic,name='loginlogic'),
    path('logincheck/',views.logincheck,name='logincheck'),
    path('emplist/',views.emplist,name='emplist'),
    path('check/',views.check,name='check'),
    path('checkname/',views.checkname,name='checkname'),
    path('addemp/',views.addemp,name='addemp'),
    path('addlogic/',views.addlogic,name='addlogic'),
    path('delete/',views.delete,name='delete'),
    path('updateemp/',views.updateemp,name='updateemp'),
    path('updalogic/',views.updalogic,name='updalogic'),

]