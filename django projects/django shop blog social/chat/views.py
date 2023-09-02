from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render , redirect
from .models import Message
from django.views import View
from django.contrib.auth import get_user_model
from .forms import MessageBarForm
# Create your views here.


User = get_user_model()


class DirectMessageView(LoginRequiredMixin,View):
    template_name = 'chat/chat_page.html'
    form_calss = MessageBarForm
    
    def get(self , request , user_id ):
        
        
        users = User.objects.all()
        user = users.get(id = user_id)
        messages1 = messages2 = []
        messages1 = list(Message.objects.filter(sender = request.user , receiver = user))
        if user != request.user:
            messages2 = list(Message.objects.filter(sender = user, receiver = request.user))
        messages = []
        for _ in range(len(messages1) + len(messages2)):
            if len(messages1) == 0:
                messages.append(messages2.pop(0))
            elif len(messages2) == 0:
                messages.append(messages1.pop(0))
            
            elif messages1[0].created <= messages2[0].created :
                messages.append(messages1.pop(0))
            else:
                messages.append(messages2.pop(0))
        
        
        context ={
            'direct_user' :user,
            'users':users,
            'messages':messages,
            'form':self.form_calss(),
        }
        
        return render(request , self.template_name , context )

    def post(self , request , user_id):
        form = self.form_calss(request.POST)
        if form.is_valid():
            user =get_user_model().objects.get(id = user_id)
            Message.objects.create(
                sender = request.user ,
                receiver =user ,
                message_body = form.cleaned_data['message_bar']
                )
            return redirect('chat:direct_message' , user_id)
        return render(request , self.template_name , {"form":form} )

