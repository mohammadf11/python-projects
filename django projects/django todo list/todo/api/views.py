from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from ..models import Todo
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import permissions
from rest_framework.viewsets import ViewSet, ModelViewSet
"""class base"""
# class TodoListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = serializers.AdminTodoserializer


# class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = serializers.AdminTodoserializer

""" Api View """

# class TodoSerializer(APIView):
#     authentication_classes = [SessionAuthentication, ]
#     def setup(self, request, *args, **kwargs):
#         self.serializer_class = self.get_serializer_(request)
#         return super().setup(request, *args, **kwargs)

#     def get_serializer_(self, request):
#         if request.user.is_staff:
#             return serializers.AdminTodoserializer
#         return serializers.UserTodoserializer


# class TodoListCreateAPIView(TodoSerializer):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         if request.user.is_staff:
#             todos = Todo.objects.all()
#         else:
#             todos = Todo.objects.filter(user=request.user)
#         srz_data = self.serializer_class(instance=todos, many=True)
#         return Response(srz_data.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         srz_data = self.serializer_class(data=request.data)
#         if srz_data.is_valid():
#             if request.user.is_staff:
#                 srz_data.save()

#             else:
#                 srz_data.save(user=request.user)

#             return Response(srz_data.data, status=status.HTTP_201_CREATED)
#         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

# class TodoRetrieveUpdateDestroyAPIView(TodoSerializer):
#     permission_classes = [IsAuthenticated , permissions.IsOwnerOrReadOnly]
#     def get(self,request , pk):
#         todo = get_object_or_404(Todo , id = pk)
#         srz_data = self.serializer_class(instance = todo)
#         return Response(srz_data.data , status=status.HTTP_200_OK)

#     def put(self ,request , pk):
#         todo = get_object_or_404(Todo , id = pk)
#         self.check_object_permissions(request , todo)
#         srz_data = self.serializer_class(data=request.POST , instance=todo , partial= True)
#         if srz_data.is_valid():
#             if request.user.is_staff:
#                 srz_data.save()
#             else:
#                 srz_data.save(user=request.user)
#                 return Response(srz_data.data, status=status.HTTP_201_CREATED)
#         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


#     def delete(self , request , pk):
#         todo = get_object_or_404(Todo , id = pk)
#         self.check_object_permissions(request , todo)
#         todo.delete()
#         return Response({"message" : 'this todo deleted'} , status=status.HTTP_404_NOT_FOUND)


""""    viewset """

# class TodoViewSet(ViewSet):
#     authentication_classes = [SessionAuthentication, ]
#     permission_classes = [IsAuthenticated , permissions.IsOwnerOrReadOnly]
#     queryset = Todo.objects.all()

#     def dispatch(self, request, *args, **kwargs):
#         self.serializer_class = self.get_serializer_(request)
#         return super().dispatch(request, *args, **kwargs)

#     def get_serializer_(self, request):
#         if request.user.is_staff:
#             return serializers.AdminTodoserializer
#         return serializers.UserTodoserializer

#     def list(self, request):
#         if request.user.is_staff:
#             todos = Todo.objects.all()
#         else:
#             todos = Todo.objects.filter(user=request.user)
#         srz_data = self.serializer_class(instance=todos, many=True)
#         return Response(srz_data.data, status=status.HTTP_200_OK)

#     def create(self, request):
#         srz_data = self.serializer_class(data=request.data)
#         if srz_data.is_valid():
#             if request.user.is_staff:
#                 srz_data.save()
#             else:
#                 srz_data.save(user=request.user)
#             return Response(srz_data.data, status=status.HTTP_201_CREATED)
#         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk):
#         todo = get_object_or_404(Todo, id=pk)
#         srz_data = self.serializer_class(instance=todo)
#         return Response(srz_data.data, status=status.HTTP_200_OK)

#     def update(self, request, pk):
#         todo = get_object_or_404(Todo, id=pk)
#         self.check_object_permissions(request, todo)
#         srz_data = self.serializer_class(
#             instance=todo , data=request.POST , partial = True)
#         if srz_data.is_valid():

#                 srz_data.save()
#                 return Response(srz_data.data, status=status.HTTP_200_OK)
#         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk):
#         todo = get_object_or_404(Todo, id=pk)
#         self.check_object_permissions(request, todo)
#         todo.delete()
#         return Response({"message": 'this todo deleted'}, status=status.HTTP_404_NOT_FOUND)

"""" ModelViewSet """


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_staff:
            return serializers.AdminTodoserializer
        return serializers.UserTodoserializer

    def create(self, request):
        srz_data = self.get_serializer_class()(data=request.data)
        if srz_data.is_valid():
            if request.user.is_staff:
                srz_data.save()
            else:
                srz_data.save(user=request.user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated,
                                  permissions.IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


# class UserRegisterApiView(APIView):
#     serializer_class = serializers.UserRegisterserializer

#     def post(self, request):
#         srz_data = self.serializer_class(data=request.data)
#         if srz_data.is_valid():
#             srz_data.save()
#             return Response(srz_data.data, status=status.HTTP_201_CREATED)
#         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
