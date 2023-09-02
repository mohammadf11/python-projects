from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Todo
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


""" Class-based views """
# class UserLoginView(LoginView):
#     template_name = 'todo/login.html'

''' Function base '''


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'todo/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)

                return redirect('todo:todo_list')
            
        return render(request, self.template_name, {'form': form})


""" Class-based views """
# class UserRegistraionView(FormView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('todo:todo_list')
#     template_name = 'todo/registration.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return super().form_valid(form)

''' Function base '''


class UserRegistraionView(View):
    form_class = UserCreationForm
    success_url = reverse_lazy('todo:todo_list')
    template_name = 'todo/registration.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'], password=data['password2'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('todo:todo_list')
        return render(request, self.template_name, {'form': form})


""" Class-based views """
# class UserLogoutView(LoginRequiredMixin, LogoutView):
#     pass

''' Function base '''


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('todo:login')


""" Class-based views """
# class TodoListView(LoginRequiredMixin, ListView):
#     model = Todo
#     template_name = 'todo/todo_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tasks'] = Todo.objects.filter(user=self.request.user)
#         context['tasks_complete'] = Todo.objects.filter(
#             completed=False, user=self.request.user)
#         context['count'] = context['tasks_complete'].count()
#         search_input = self.request.GET.get('search-area') or ''
#         if search_input:
#             context['tasks'] = context['tasks'].filter(
#                 title__contains=search_input)
#         return context


''' Function base '''
class TodoListView(LoginRequiredMixin, View):
    template_name = 'todo/todo_list.html'

    def get(self, request):
        tasks = Todo.objects.filter(user=self.request.user)
        tasks_complete = tasks.filter(
            completed=False, user=self.request.user)
        count = tasks_complete.count()
        search_input = self.request.GET.get('search-area') 
        if search_input:
            tasks = tasks.filter(
                title__contains=search_input)
        context = {
            'tasks': tasks,
            'tasks_complete': tasks_complete,
            'count': count
        }
        return render(request, self.template_name, context)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo/todo_create.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo:todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'completed']
    template_name = 'todo/todo_update.html'
    success_url = reverse_lazy('todo:todo_list')
    pk_url_kwarg = 'id'


""" Class-based views """
# class TodoDeleteView(LoginRequiredMixin, DeleteView):
#     model = Todo
#     template_name = 'todo/todo_delete.html'
#     success_url = reverse_lazy('todo:todo_list')
#     context_object_name = 'task'
#     pk_url_kwarg = 'id'

''' Function base '''
class TodoDeleteView(LoginRequiredMixin, View):
    template_name = 'todo/todo_delete.html'

    def setup(self, request, *args, **kwargs):
        self.task = get_object_or_404(Todo, id=kwargs.get('id'))
        return super().setup(request, *args, **kwargs)

    def get(self, request, id):
        return render(request, self.template_name, {'task': self.task})

    def post(self, request , id ):
        self.task.delete()
        return redirect('todo:todo_list')

