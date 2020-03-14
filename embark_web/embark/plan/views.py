from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm

# Create your views here.
def user_input(request):
    if request.method == 'POST':
            form = InputForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                Start_Hour = form.cleaned_data['Start_Hour']
                End_Hour = form.cleaned_data['End_Hour']
                loc_count = form.cleaned_data['loc_count']
                trv_time = form.cleaned_data['trv_time']
                trv_dist = form.cleaned_data['trv_dist']


                print(name, email, Start_Hour, End_Hour, loc_count, trv_time, trv_dist)
                # call out function


    form = InputForm()
    return render(request,'form.html', {'form':form})