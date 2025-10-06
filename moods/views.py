from django.shortcuts import render
import ast
from Databases.CRUD import CRUD
import json
from django.shortcuts import redirect
from datetime import datetime
import time



crud = CRUD()

def CreateNew(request):
    if request.method == "GET":
        return render(request, "createNewLog.html")
    
    elif request.method == "POST":
        crud.CreateNewDB(filename=request.POST['filename'],
                         name=request.POST['name'],
                         template=request.POST['template'])
        request.session['registry'] = ""
        return redirect("/")
    
def home(request):
    if request.method == "GET":
        print(crud.GetRegistry())
        return render(request, "base.html", {"registry": crud.GetRegistry()})