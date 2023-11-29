# study_groups/views.py

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import StudyGroupForm, MessageForm
from .models import StudyGroup, GroupPermission, Message


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('study_groups')  # Redirect to the study groups page after login
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, you can automatically log in the user after registration
            # login(request, user)
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def study_groups(request):
    groups = StudyGroup.objects.all()
    return render(request, 'study_groups/study_group.html', {'group': groups})


@login_required
def create_study_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.members.add(request.user)
            permission = GroupPermission(group=group, user=request.user, can_post=True, can_comment=True, can_invite=False)
            permission.save()
            return redirect('study_groups')
    else:
        form = StudyGroupForm()

    return render(request, 'study_groups/create_study_group.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    permission = GroupPermission.objects.get(group=group, user=request.user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = group
            message.sender = request.user
            message.save()
    else:
        form = MessageForm()

    messages = Message.objects.filter(group=group)

    return render(request, 'study_groups/group_detail.html', {'group': group, 'permission': permission, 'form': form, 'messages': messages})

