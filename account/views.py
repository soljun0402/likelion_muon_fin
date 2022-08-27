from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm

def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password")
      user = authenticate(request=request, username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect("home")
    else:
      form = AuthenticationForm()
      ctx = {
        'form': form,
        'error': '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.'
      }
      return render(request, "login.html", ctx)

  else:
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
  logout(request)
  return redirect("home")

def register_view(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')

    else:
      form = RegisterForm()
      ctx = {
        'form': form,
        'error': '회원가입 형식에 맞게 입력해주세요.'
      }
      return render(request, 'signup.html', ctx)

  else:
    form = RegisterForm()
    return render(request, 'signup.html', {'form':form})