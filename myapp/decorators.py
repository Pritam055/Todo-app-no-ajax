from django.shortcuts import redirect
from django.http import HttpResponse

def unAuthenticatedUserOnly(fun):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            print("URL: ", request.path)
            return redirect('todo:todoList')
        else:
            return fun(request, *args, **kwargs) 
        

    return wrapper_function