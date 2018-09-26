from django.db import models

# Create your models here.

class Airplane(models.Model):
    flight_id = models.CharField(max_length=20, primary_key=True)
    flight_type = models.CharField(max_length=50)
    no_of_seats = models.IntegerField()


class Traffic(models.Model):
    flight_id = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    date_and_time = models.DateField()
    fromLocation = models.CharField(max_length=200)
    toLocation = models.CharField(max_length=200)
    sche_dept = models.DateTimeField()
    sche_arrival = models.DateTimeField()
    actual_dept = models.DateTimeField()
    actual_arrival = models.DateTimeField()

    class Meta:
        unique_together = (('flight_id', 'date_and_time'), )



class Customer(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    #Check if better than this
    # age = models.ValueRange()
    age = models.IntegerField()
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    street_details = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)


class Customer_mobile_no(models.Model):
    mobile_no = models.CharField(max_length=10)
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('mobile_no', 'username'), )


class Tickets(models.Model):
    ticket_id = models.CharField(max_length=20, primary_key=True)
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    flight_id = models.CharField(max_length=20)
    date_and_time = models.DateField()
    flight_date_time_combo = models.ForeignKey(Traffic, on_delete=models.CASCADE)


class Seat_Allocation(models.Model):
    #ticket_id = models.ForeignKey(Tickets, primary_key=True)
    ticket_id = models.OneToOneField(Tickets, on_delete=models.CASCADE)
    seat_no = models.IntegerField()
    baggage_weight = models.IntegerField()
    food_preference = models.CharField(max_length=50)


class Employee(models.Model):
    emp_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    # Check if better than this
    #age = models.ValueRange()
    age = models.IntegerField()
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    street_details = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)


class Employee_mobile_no(models.Model):
    mobile_no = models.CharField(max_length=10)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('mobile_no', 'emp_id'), )


class Airhostess(models.Model):
    emp_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    next_flight_id = models.CharField(max_length=20)
    next_date_and_time = models.DateTimeField()
    flight_id = models.CharField(max_length=20)
    flight_date_time_combo = models.ForeignKey(Traffic, on_delete=models.CASCADE)
    airport_name = models.CharField(max_length=100)


class Pilot(models.Model):
    emp_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    next_flight_id = models.CharField(max_length=20)
    next_date_and_time = models.DateTimeField()
    flight_id = models.CharField(max_length=20)
    flight_date_time_combo = models.ForeignKey(Traffic, on_delete=models.CASCADE)
    airport_name = models.CharField(max_length=100)

class Desk_Workers(models.Model):
    #emp_id = models.ForeignKey(Employee, primary_key=True)
    emp_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    airport_name = models.CharField(max_length=100)
    desk_no = models.IntegerField()

