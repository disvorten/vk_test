from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from .models import User, Friend_Request
from django.contrib import messages


@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    try:
        friend_request = Friend_Request.objects.get(from_user=to_user, to_user=from_user)
    except:
        friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            messages.success(request, 'friend request sent')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            messages.warning(request, 'friend request was already sent')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        if friend_request:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.success(request, 'friend request accepted')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.warning(request, 'friend request not accepted')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def recall_request(request, requestID):
    friend_request = Friend_Request.objects.get(from_user_id=request.user.id, to_user_id=requestID)
    friend_request.delete()
    messages.success(request, 'friend request recalled')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def deny_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(from_user_id=requestID, to_user_id=request.user.id)
    friend_request.delete()
    messages.success(request, 'friend request denied')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def test(request):
    return render(request, 'contacts/request.html')


def see_users(request):
    if not Friend_Request.objects.filter(to_user_id=request.user.id).exists():
        all = None
    else:
        all = list(Friend_Request.objects.filter(to_user_id=request.user.id))
        all = [x.from_us() for x in all]
    if not Friend_Request.objects.filter(from_user_id=request.user.id).exists():
        your = None
    else:
        your = list(Friend_Request.objects.filter(from_user_id=request.user.id))
        your = [x.to_us() for x in your]
    context = {
        'users': User.objects.all(),
        'all_friend_requests': all,
        'your_friend_requests': your,
    }
    return render(request, 'contacts/users.html', context)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('see_users'))
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'contacts/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'contacts/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
        'all_friend_requests': Friend_Request.objects.filter(to_user_id=request.user.id),
        'your_friend_requests': Friend_Request.objects.filter(from_user_id=request.user.id),
        'friends': request.user.friends.all()
    }
    return render(request, 'contacts/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('see_users'))


@login_required
def delete_from_friends(request, personID):
    friend = request.user.friends.get(id=personID)
    Friend_Request.objects.create(from_user=friend, to_user=request.user)
    request.user.friends.remove(personID)
    friend.friends.remove(request.user.id)
    messages.success(request, 'Successfully deleted ')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
