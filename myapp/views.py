from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Todo 
from .decorators import unAuthenticatedUserOnly
# Create your views here.


@method_decorator(unAuthenticatedUserOnly, name='dispatch')
class RegisterView(CreateView):
    template_name = 'myapp/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('todo:login')



@method_decorator(unAuthenticatedUserOnly, name='dispatch')
class LoginView(FormView):
    template_name = 'myapp/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('todo:todoList')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        # print(usr)
        if usr is not None:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form':self.form_class})
        
        return super().form_valid(form)
    
    def get_success_url(self):
        print("-"*20)
        print(self.request.GET)
        if 'next' in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
        
        

@method_decorator(login_required, name='dispatch')
class TodoListView(ListView):
    model = Todo
    template_name = 'myapp/todoList.html'
    context_object_name = "todos" 

    def get_queryset(self, *args, **kwargs):
        # print(Todo.objects.filter(user=self.request.user))
        return Todo.objects.filter(user=self.request.user).order_by('complete') 


@method_decorator(login_required, name='dispatch')
class AddTodo(CreateView): 
    model = Todo
    fields = ['title','description'] 
    template_name = "myapp/addTodo.html"
    success_url = reverse_lazy('todo:todoList') # with reverse_lazy we can use name
    # success_url = "/"

    def form_valid(self, form):
        # print(form.instance.title)
        # print(form.instance.description)
        # print(form.instance.user)
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TodoDetailView(DetailView):
    model = Todo
    template_name = 'myapp/detail.html'
    context_object_name = 'todo_object'


@method_decorator(login_required, name='dispatch')
class TodoEditView(UpdateView):
    model = Todo
    fields = ['title','description', 'complete']
    template_name = 'myapp/update.html'
    success_url = reverse_lazy('todo:todoList')

    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['name'].widget = 

@method_decorator(login_required, name='dispatch')
class TodoDeleteView(View):
    def get(self, request, *args, **kwargs):
        # print(self.kwargs)
        pk = self.kwargs["pk"]
        print('pk: ', pk)
        getTodo = Todo.objects.get(id=pk)
        if getTodo is not None:
            getTodo.delete()

        return redirect('todo:todoList')
    

