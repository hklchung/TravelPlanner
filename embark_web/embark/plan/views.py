from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm

# Create your views here.
def user_input(request):
    if request.method == 'POST':
            form = InputForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['Your_name']
                email = form.cleaned_data['Your_email']
                Trip_day = form.cleaned_data['Trip_day']
                Start_Hour = form.cleaned_data['Trip_start_hour']
                End_Hour = form.cleaned_data['Trip_end_hour']
                loc_count = form.cleaned_data['Number_of_locations_to_visit']
                trv_time = form.cleaned_data['Total_transportation_hours']
                trv_dist = form.cleaned_data['Travel_distance_to_first_location']

                #embark = Embark()
                #embark.print_itinerary()


                print(name, email, Start_Hour, End_Hour, loc_count, trv_time, trv_dist)
                # call out function


    form = InputForm()
    return render(request,'form.html', {'form':form})