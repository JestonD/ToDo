# Fuction based views
from django.shortcuts import render,redirect
from .forms import taskForm
from .models import Task
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Class based views
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy #instead of redirect
from django.views.generic.edit import FormView # also used to add other Class based views


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterView(FormView):
    template_name = 'Register.html'
    redirect_authenticated_user = True
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        
        if user is not None:
            login(self.request, user)
            
        return super(RegisterView, self).form_valid(form)
    
    # same as redirect_authenticated_user = True
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterView, self).get(*args, **kwargs)


# Fuction based views
@login_required
def Disp_tasks(request):
    tasks = Task.objects.all()
    context = {
        'tasks' : tasks
    }
    context['tasks'] = context['tasks'].filter(user=request.user)
    context['count'] = context['tasks'].filter(complete=False).count()

    search_input = request.GET.get('search-area') or ''

    if search_input:
        context['tasks'] = context['tasks'].filter(title__icontains=search_input)
    
    context['search_input'] = search_input

    return render(request,"Disp_tasks.html",context)
    
@login_required
def Create_Task(request):

    if request.method == "POST":
        form = taskForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('home')
    else:
        form = taskForm()

    context = {'form' : form}
    return render(request, "createTask.html", context)

@login_required
def Edit_View(request, id):
    task = Task.objects.get(id = id )

    if request.method == "POST":
        form = taskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = taskForm(instance=task)

    return render(request,'Edit_view.html',{'form': form,'task': task })

@login_required
def Delete_View(request, id):
    task = Task.objects.get(id = id )

    if request.method == "POST":
        form = taskForm(request.POST,instance=task)
        if form.is_valid():
            task.delete()
            return redirect('home')
    else:
        form = taskForm(instance=task)

    return render(request,'Delete_View.html',{'form': form,'task': task })

@login_required
def Complete_View(request, id):
    task = Task.objects.get(id = id )
    task.complete = not(task.complete)
    task.save()
    return redirect('home')

