from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from myapp.models import Reservation
from .serializers import ReservationSerializer
import json
from urllib.parse import parse_qs

def transform_to_json(data_string):
    # Parse the query string into a dictionary
    #{'full_name': 'John sdds', 'CIN': 123456789, 'debut_reservation': '2023-06-15', 'fin_reservation': '2023-06-20', 'num_tel': 987654321, 'montant': 500}
    #{'full_name': ['qq'], 'CIN': ['55'], 'debut_reservation': ['2023-06-11'], 'fin_reservation': ['2023-06-15'], 'num_tel': ['55'], 'montant': ['44']}
    data_dict = parse_qs(data_string)
    for i in data_dict:
        data_dict[i]=data_dict[i][0]

    # Convert the dictionary to JSON
    json_data = json.dumps(data_dict)

    return json_data

struct = {}

    


#class ReservationCreateView(CreateView):
 #   model = Reservation
  #  fields = ['full_name', 'CIN', 'debut_reservation', 'fin_reservation', 'num_tel', 'montant']
#def reservation(request):
 #   if request.method == 'POST':
  #      form = ReservationForm(request.POST)
   #     if form.is_valid():
    #        form.save()
     #       return redirect('reservation-success')  # Redirect to a success page after saving the form data
    #else:
     #   form = ReservationForm()
    #return render(request, 'reservation_form.html', {'form': form})




@csrf_exempt
def ReservationAPI(request):
    #if request.method == 'GET':
      #  departments = Department.objects.all()
       # departments_serializer = DepartmentSerializer(departments, many=True)
        #return JsonResponse(departments_serializer.data, safe=False)
    
    if request.method == 'POST':
        dataformm = request.body.decode('utf-8')
        print("Received data:", dataformm) # Add this line for debugging
        dataformm=dataformm[85:] 
        dataform=transform_to_json(dataformm)
        #Received data: csrfmiddlewaretoken=UHgpKeYVvRuDEyuwVFF82zmGes8ht8WvbEKvqBfvgZtRFH4v8wjxnKvX7Ofpvh5D&full_name=qq&CIN=55&debut_reservation=2023-06-11&fin_reservation=2023-06-15&num_tel=55&montant=44
        print("Received data:", dataform) # Add this line for debugging
        

        try:
            struct = json.loads(dataform)
            print("Parsed data:", struct)  # Add this line for debugging
            reservation_serializer = ReservationSerializer(data=struct)
            
            if reservation_serializer.is_valid():
                reservation_serializer.save()
                return render(request, 'success.html')
            return JsonResponse(reservation_serializer.errors, status=400)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))  # Add this line for debugging
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    
def welcome(request):
    return render(request,'welcome.html')
