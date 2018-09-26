

# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.http import  Http404
from .models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import datetime
from dateutil.parser import parse
# Create your views here.
def index(request):
    return render(request,'Airline_Management_System/airkgp.html')


def detail(request):
    return render(request, 'airline/employee.html')


def customer(request):
    return render(request, 'airline/customer.html')


def employee_login(request):
    employee_id=request.POST.get('user')
    employee_password=request.POST.get('pass')
    if (Employee.objects.filter(emp_id=employee_id).exists() and Employee.objects.filter( password =employee_password).exists()):
        traffic = str(employee_id)
        traffic_details = traffic.split(":")
        print(traffic_details[0])
        if(traffic_details[0]=="DW"):
            employee = Employee.objects.get(emp_id=employee_id)
            return render(request, 'airline/deskjob.html',{'name':employee.name })
        elif (traffic_details[0] == "AH"):
            employee=Employee.objects.get(emp_id=employee_id)
            airhostess=Airhostess.objects.get(emp_id=employee)
            print(employee.airhostess.next_flight_id)
            #return render(request, 'airline/employee.html')
            return render(request, 'airline/airhostess.html',{'airhostess_next_flight_id':employee.airhostess.next_flight_id,
                                                                'dateandtime': employee.airhostess.next_date_and_time ,
                                                                 'name':employee.name , 'from' : employee.airhostess.airport_name })
        elif(traffic_details[0] == "PL"):
            employee = Employee.objects.get(emp_id=employee_id)
            pilot = Pilot.objects.get(emp_id=employee)
            return render(request, 'airline/pilot.html',
                          {'airhostess_next_flight_id': employee.pilot.next_flight_id,
                           'dateandtime': employee.pilot.next_date_and_time,
                           'name': employee.name, 'from': employee.pilot.airport_name})

    else:
        return render(request, 'airline/employee.html')

# def flight_list(request,user_name):
#     From = request.POST.get('from')
#     To = request.POST.get('to')
#     Date= request.POST.get('date')
#     Flights=Traffic.objects.all().filter( fromLocation=From,toLocation=To)
#     return render(request, 'airline/flight_list.html', {'flights': Flights})
#     #return render(request, 'airline/customer.html')

def customer_create(request):
    username = request.POST.get('user')
    password = request.POST.get('pass')
    name = request.POST.get('name')
    age = request.POST.get('age')
    street = request.POST.get('street')
    city = request.POST.get('city')
    state = request.POST.get('state')
    mobile = request.POST.get('mobile')
    genderGet = request.POST.get('gender')
    try:
        age = int(age)
        mobile = int(mobile)
    except ValueError:
        return render(request, 'airline/customer.html')
    if not (Customer.objects.filter(username=username).exists()):
        customer1 = Customer()
        customer1.username = username
        customer1.password = password
        customer1.name=name
        customer1.age=age
        customer1.street_details=street
        customer1.city=city
        customer1.state=state
        customer1.gender = genderGet
        print(genderGet)
        if(username == '' or password == '' or name == '' or age == '' or street == '' or city == '' or state == '' or mobile == ''):
            return render(request, 'airline/customer.html')
        customer1.save()
        obj = Customer_mobile_no.objects.create(mobile_no=mobile, username=customer1)
        obj.save()
        return render(request, 'airline/customer_choices.html')
    else:
        return render(request, 'airline/customer.html')


def customer_signin(request):
    usernametemp = request.POST.get('user')
    passwordtemp = request.POST.get('pass')
    if passwordtemp == '':
        return render(request, 'airline/customer.html')
    customer_rec = Customer.objects.all().filter(username=usernametemp)
    if customer_rec.count() == 0:
        return render(request, 'airline/customer.html')
    if customer_rec[0].username == usernametemp and customer_rec[0].password == passwordtemp:
        return render(request, 'airline/customer_choices.html', {'customer':customer_rec[0]})
    else:
        return render(request, 'airline/customer.html')


def see_flights(request,user_name):
    customer_rec = Customer.objects.get(username=user_name)
    return render(request, 'airline/filght_detail.html', {'customer': customer_rec})


def flight_list(request,user_name):
    customer_rec = Customer.objects.get(username=user_name)
    From = request.POST.get('from')
    To = request.POST.get('to')
    Date=request.POST.get('date')
    print(Date)
    if(Date!=''):
        traffic=Traffic.objects.all().filter(fromLocation=From,toLocation=To,date_and_time=Date)
    else :
        return render(request, 'airline/filght_detail.html', {'customer': customer_rec})

    if(traffic.count()==0) :
        List1 = []
        List2 = []
        Traffic1 = Traffic.objects.all().filter(fromLocation=From, date_and_time=Date)
        Traffic2 = Traffic.objects.all().filter(toLocation=To)
        for traffic1 in Traffic1:
            for traffic2 in Traffic2 :
                if traffic1.toLocation == traffic2.fromLocation :
                    List1.append(traffic1)
                    List2.append(traffic2)
        if len(List1) == 0:
            return render(request, 'airline/filght_detail.html', {'customer': customer_rec})
        else:
            list=zip(List1,List2)
            return render(request, 'airline/flight_list_transitive.html', {'list': list, 'customer': customer_rec})

    return render(request, 'airline/flight_list.html', {'flights': traffic, 'customer': customer_rec})

def customer_got_status(request, user_name):
    customer_rec = Customer.objects.get(username=user_name)
    ticketidtemp = request.POST.get('ticketid')
    ticketlist = Tickets.objects.all().filter(ticket_id=ticketidtemp)
    if ticketlist.count() == 0:
        return render(request, 'airline/check_status.html', {'customer': customer_rec})
    print(ticketlist[0].flight_date_time_combo.fromLocation)
    print(ticketlist[0].flight_date_time_combo_id)
    delayDeparture = ticketlist[0].flight_date_time_combo.actual_dept - ticketlist[0].flight_date_time_combo.sche_dept
    return render(request, 'airline/got_status.html', {'customer': customer_rec,
                                                       'flight_details': ticketlist[0].flight_date_time_combo, 'delayInDeparture': delayDeparture})

def customer_check_status(request, user_name):
    customer_rec = Customer.objects.get(username=user_name)
    return render(request,'airline/check_status.html', {'customer': customer_rec})


'''def flight_book(request,user_name) :
    import random
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p = "".join(random.sample(s, passlen))
    print(p)
    traffic=request.POST.get('ticket')
    traffic=str(traffic)
    traffic_details=traffic.split(":")
    print(traffic_details[3])
    airplane = Airplane.objects.get(flight_id=traffic_details[0])
    customer_rec = Customer.objects.get(username=user_name)
    #datetime.strptime('07/28/2014 18:54:55.099', '%m/%d/%Y %H:%M:%S.%f')
    #datetime_object = datetime.strptime(traffic_details[3], '%b %d %Y %I:%M%p')

    if(airplane.no_of_seats>0) :
        airplane.no_of_seats=airplane.no_of_seats-1
        airplane.save()
        traffic_obj=Traffic.objects.all().filter(flight_id=airplane,fromLocation=traffic_details[1],toLocation=traffic_details[2])
        ticket_obj = Tickets.objects.create(ticket_id=p, username=customer_rec,flight_id=traffic_details[0],date_and_time=traffic_obj[0].date_and_time, flight_date_time_combo=traffic_obj[0])
        ticket_obj.save()
        return render(request, 'airline/customer.html')
    else:
        return render(request, 'airline/filght_detail.html', {'customer': customer_rec})
 '''

def flight_book(request,user_name) :
    import random
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p = "".join(random.sample(s, passlen))
    print(p)
    traffic=request.POST.get('ticket')
    traffic=str(traffic)
    traffic_details=traffic.split(":")
    print(traffic_details[3])
    airplane = Airplane.objects.get(flight_id=traffic_details[0])
    customer_rec = Customer.objects.get(username=user_name)
    #datetime.strptime('07/28/2014 18:54:55.099', '%m/%d/%Y %H:%M:%S.%f')
    #datetime_object = datetime.strptime(traffic_details[3], '%b %d %Y %I:%M%p')

    if(airplane.no_of_seats>0) :
        airplane.no_of_seats=airplane.no_of_seats-1
        airplane.save()
        traffic_obj=Traffic.objects.all().filter(flight_id=airplane,fromLocation=traffic_details[1],toLocation=traffic_details[2])
        ticket_obj = Tickets.objects.create(ticket_id=p, username=customer_rec,flight_id=traffic_details[0],date_and_time=traffic_obj[0].date_and_time, flight_date_time_combo=traffic_obj[0])
        ticket_obj.save()
        return render(request, 'airline/ticket_display.html', {'ticket_id': p,'date':traffic_obj[0].date_and_time,'flight_id': airplane.flight_id ,
                                                               'from':traffic_details[1], 'to' : traffic_details[2],'schdep' : traffic_obj[0].sche_dept
                                                               ,'scharr': traffic_obj[0].sche_arrival,'name' : customer_rec.name, 'age':customer_rec.age,
                                                               })
    else:
        return render(request, 'airline/filght_detail.html', {'customer': customer_rec})


def update(request,user_name):
    customer_rec = Customer.objects.get(username=user_name)
    return render(request, 'airline/update.html', {'customer': customer_rec})


def updating(request,user_name):
    customer_rec = Customer.objects.get(username=user_name)
    password = request.POST.get('pass')
    name = request.POST.get('name')
    age = request.POST.get('age')
    street = request.POST.get('street')
    city = request.POST.get('city')
    state = request.POST.get('state')
    mobile = request.POST.get('mobile')
    genderGet = request.POST.get('gender')
    if(age != ''):
        age = int(age)
    if (mobile != ''):
        mobile = int(mobile)
    customer1 = Customer.objects.get(username=user_name)
    if(password != ''):
        customer1.password = password
    if(name != ''):
        customer1.name = name
    if (age != ''):
        customer1.age = age
    if (street != ''):
        customer1.street_details = street
    if (city != ''):
        customer1.city = city
    if (state != ''):
        customer1.state = state
    customer1.gender = genderGet
    customer1.save()
    if (mobile != ''):
        obj = Customer_mobile_no.objects.create(mobile_no=mobile, username=customer1)
        obj.save()
    return render(request, 'airline/customer_choices.html', {'customer': customer_rec})


def logout_view(request):
    logout(request)
    return redirect('index')


def go_back(request,user_name):
    customer_rec = Customer.objects.get(username=user_name)
    return render(request, 'airline/customer_choices.html', {'customer': customer_rec})

def web_checkin(request, user_name):
    customer_rec = Customer.objects.get(username=user_name)
    return render(request, 'airline/webcheckin.html', {'customer': customer_rec})

def boarding_pass(request, user_name):
    customer_rec = Customer.objects.get(username=user_name)
    ticketidtemp = request.POST.get('ticketid')
    ticketlist = Tickets.objects.all().filter(ticket_id=ticketidtemp, username=customer_rec.username)
    if ticketlist.count() == 0:
        return render(request, 'airline/webcheckin.html', {'customer': customer_rec})
    seatlist = Seat_Allocation.objects.all().filter(ticket_id=ticketidtemp)
    if seatlist.count() == 0:
        return render(request, 'airline/webcheckin.html', {'customer': customer_rec})
    #print(ticketlist[0].flight_date_time_combo.fromLocation)
    #delayDeparture = ticketlist[0].flight_date_time_combo.actual_dept - ticketlist[0].flight_date_time_combo.sche_dept
    return render(request,
                  'airline/get_boarding.html',
                  {'customer': customer_rec, 'flight_details': ticketlist[0].flight_date_time_combo,
                   'ticket_details': ticketlist[0], 'seat_details': seatlist[0]})


def airplane_list (request) :
    airplanes=Airplane.objects.all()
    return render(request, 'airline/airplane_list.html', {'airplanes': airplanes})


def scheduled_traffic_list(request):
    airplanes = Traffic.objects.all()
    return render(request, 'airline/scheduled_traffic_list.html', {'airplanes': airplanes})
