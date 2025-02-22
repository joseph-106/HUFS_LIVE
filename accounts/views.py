from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        if request.POST['username'] == '' or request.POST['nickname']=='' or request.POST['password1'] =='':
            return render(request, 'signup.html', {'error': '모든 항목을 필수로 입력해주셔야 합니다'})
        elif not 5<len(request.POST['username'])<16 :
            return render(request, 'signup.html', {'error': '아이디는 6자 이상 16자 미만이어야 합니다'})
        elif not 1<len(request.POST['nickname'])<12 :
            return render(request, 'signup.html', {'error': '닉네임은 2자 이상 12자 미만이어야 합니다'})
        elif not 7<len(request.POST['password1'])<12 :
            return render(request, 'signup.html', {'error': '비밀번호는 영문 or 숫자 조합으로 8자 이상 20자 미만이어야 합니다'})
        elif request.POST['password1'].isalnum() == False: #문자나 숫자가 아예 포함되어 있지 않다면
            return render(request, 'signup.html', {'error': '비밀번호는 영문 or 숫자 조합으로 8자 이상 20자 미만이어야 합니다'})
        elif request.POST['password1'] != request.POST['password2']:
            return render(request, 'signup.html', {'error': '비밀번호가 일치하지 않습니다'})
        else:
            try:
                user = User.objects.create_user( username=request.POST['username'], first_name=request.POST['nickname'], password=request.POST['password1'])
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            except:
                return render(request, 'signup.html', {'error': '이미 존재하는 아이디입니다'})
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '아이디 혹은 비밀번호가 일치하지 않습니다'})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'login.html')