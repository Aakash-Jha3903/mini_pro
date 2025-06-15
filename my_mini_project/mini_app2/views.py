# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader  # W3 school
# from .models import Officials, Student
from .models import OfficialsUser, Student
from django.shortcuts import get_object_or_404

import random
from faker import Faker
fake = Faker()
from django.utils import timezone

import matplotlib.pyplot as plt
from django.db.models import Count
import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import os
from matplotlib.ticker import MaxNLocator
from datetime import datetime

from django.db import IntegrityError

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout

def index(request):
    try:
        pass
        return render(request, "index.html")
    except Exception as e :
        return HttpResponse(f"Error occured : {e}")
        

def contact(request):
    pass
    return render(request, "contact.html")

def ST_login(request):
    try:
        pass
        return render(request, "ST_login.html")
    except Exception as e :
        return HttpResponse(f"Error occured : {e}")
    

from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
@login_required(login_url='/officials/')
# @never_cache
def services(request):
    if request.method == 'POST':
        # and 'logout' in request.POST:
        logout(request)
        return redirect('/') 
    return render(request, "services.html")

# def officials(request):
def Officials(request):
    if request.method == 'POST':
        official_id = request.POST.get('userid')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, name=official_id, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('services')
        else:
            # Authentication failed
            return render(request, 'officials.html', {'error_message': 'Invalid credentials'})

    return render(request, 'officials.html')

@login_required(login_url='/officials/')
def logout_officials(request):
    # logout(request)
    return redirect('logout_officials')  # Redirect to the login page after logout
    # return LogoutView.as_view()(request, next_page='officials_logout')  # Redirect to login page after logout

def form(request):
    message = ""  # Initialize message outside the conditional block

    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_id')
            student_name = request.POST.get('student_name')
            student_aadhar = request.POST.get('student_aadhar')
            student_phone = request.POST.get('student_phone')
            student_email = request.POST.get('student_email')
            # age = request.POST.get('age')
            gender = request.POST.get('gender')
            student_dob = request.POST.get('student_dob')
            student_address = request.POST.get('student_address')

            father_name = request.POST.get('father_name')
            father_phone = request.POST.get('father_phone')
            mother_name = request.POST.get('mother_name')
            mother_phone = request.POST.get('mother_phone')

            school_name = request.POST.get('school_name')
            section = request.POST.get('section')
            state_name = request.POST.get('state_name')
            city_name = request.POST.get('city_name')
            
            attendance = request.POST.get('attendance')
            marks = request.POST.get('marks')
            fees = request.POST.get('fees')

            # back = Student(
            #     student_id=student_id,
            #     student_name=student_name,
            #     student_aadhar=student_aadhar,
            #     student_phone=student_phone,
            #     student_email=student_email,
            #    # age=age,
            #     gender=gender,
            #     student_dob=student_dob,
            #     student_address=student_address,
            #     father_name=father_name,
            #     father_phone=father_phone,
            #     mother_name=mother_name,
            #     mother_phone=mother_phone,
            #     school_name=school_name,
            #     section=section,
            #     state_name=state_name,
            #     city_name=city_name,
            #     attendance=attendance,
            #     marks=marks,
            #     fees=fees
            #     )

            # Save data temporarily in session
            request.session['form_data'] = {
                'student_id': student_id,
                'student_name': student_name,
                'student_aadhar': student_aadhar,
                'student_phone': student_phone,
                'student_email': student_email,
                # 'age': age,
                'gender': gender,
                'student_dob': student_dob,
                'student_address': student_address,
                'father_name': father_name,
                'father_phone': father_phone,
                'mother_name': mother_name,
                'mother_phone': mother_phone,
                'school_name': school_name,
                'section': section,
                'state_name': state_name,
                'city_name': city_name,
                'attendance': attendance,
                'marks': marks,
                'fees': fees
            }

            # Generate and send OTP
            otp_code = generate_otp()
            request.session['otp_code'] = otp_code
            send_otp_email(otp_code, student_email)

            return redirect('otp_verification')
        
            # back.save()  # Save data to the database
            # message = "Your data is recorded"
            # return redirect('thanks')
            # Save data to the database only if OTP is verified
            # return redirect('otp_verification')

            # if request.session.get('otp_verified'):
            #     back.save()
            #     message = "Your data is recorded"
            #     return redirect('thanks')
            # else:
            #     message = "Error: OTP not verified."
        except IntegrityError as e:
                print(f"Error: {e}")
                message = f"Error: {e}"
    data = {
        'message': message,
        # Include other data if needed
    }

    return render(request, 'form.html', data)

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()


def generate_otp():
    return get_random_string(length=6, allowed_chars='0123456789')

# def send_otp_email():
def send_otp_email(otp_code,student_email):
    subject = 'OTP Confirmation'
    message = f'Your OTP code is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER  # Replace with your email
    recipient_list = [student_email]
    # print('...........\n\n',recipient_list,'\n\n.........')
            
    # recipient_list = ['aakashjha343@gmail.com']

    send_mail(subject, message, from_email, recipient_list)

def otp_verification(request):

    # Check if the form data is present in the session
    if 'form_data' not in request.session:
        return redirect('form')
    
    
    if request.method == 'POST':
        try:
            # request.session['otp_verified'] = False

            # Check if it's a regular OTP verification attempt
            if 'resend_otp' not in request.POST:
                entered_otp = request.POST.get('entered_otp')
                stored_otp = request.session.get('otp_code')


                # student_email = request.POST.get('student_email')
                entered_otp = request.POST.get('entered_otp')

                # Retrieve the OTP from session for verification
                stored_otp = request.session.get('otp_code')
                print('...........\n\n',stored_otp,'\n\n.........')

                # Verify the entered OTP
                if stored_otp == entered_otp:                
                    # Clear the stored OTP from session
                    del request.session['otp_code']
                    request.session['otp_verified'] = True  # Set a session variable to indicate OTP verification

                    # Pass student_email to the thanks_page view
                    return redirect('thanks')

                else:
                    # Invalid OTP
                    return render(request, 'otp_verification.html', {'error_message': 'Invalid OTP'})

            # Resend OTP logic
            # elif request.method == 'POST' and 'resend_otp' in request.POST:
            else :     
                otp_code = generate_otp()
                request.session['otp_code'] = otp_code
                send_otp_email(otp_code, request.session.get('form_data')['student_email'])
                return render(request, 'otp_verification.html', {'resend_message': 'OTP resent successfully'})

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    return render(request, 'otp_verification.html')


def thanks(request):
    if not (request.session.get('otp_verified') and request.session.get('form_data')):
        # If OTP is not verified or form data is not present, redirect to form
        return redirect('form')
    form_data = request.session.get('form_data')
    # Save data to the database
    back = Student(**form_data)
    back.save()
    # Clear the form data from session
    del request.session['form_data']
        
    # Clear session data
    request.session.clear()
    return render(request, "thanks.html",{"message":"Your data is recorded"})


from .forms import StudentLoginForm     # forms.py
from django.urls import reverse
from django.http import HttpResponseRedirect
def student_login(request): #DDMMYYYY
    try:
        if request.method == 'POST':
            form = StudentLoginForm(request.POST)
            if form.is_valid():
                student_id = form.cleaned_data['student_id']
                raw_password = str(form.cleaned_data['password'])  # Convert to string

                # Convert the raw password (DDMMYYYY) to the required format ('YYYY-MM-DD')
                formatted_password = f"{raw_password[4:8]}-{raw_password[2:4]}-{raw_password[0:2]}"

                # Check if the student with the provided ID and formatted password exists
                student = get_object_or_404(Student, student_id=student_id, student_dob=formatted_password)

                # Redirect to student_details view with the student's ID as a parameter
                return HttpResponseRedirect(reverse('student_details', args=[student_id]))

        else:
            form = StudentLoginForm()

        return render(request, 'student_login.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"An error ocured : {e} ")


from django.contrib.auth.decorators import login_required
# @login_required
# @login_required(login_url='/officials/')
@login_required(login_url='/student_login/')
def student_details(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    
    return render(request, 'student_details.html', {'student': student})
    

# mini_app2/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherLoginForm, TeacherRegistrationForm 
@login_required(login_url='/officials/')
def teacher_registration(request):
    # try:
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            password = form.cleaned_data['password']
            section = form.cleaned_data['section']

            # Create a new teacher registration entry
            TeacherRegistration.objects.create(teacher_id=teacher_id, password=password, section=section)

            # Redirect to the teacher login page
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('teacher_login')
        
            # return redirect('teacher_login')
    else:
        form = TeacherRegistrationForm()

    return render(request, 'teacher_registration.html', {'form': form})

# mini_app2/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherLoginForm
from .models import SectionTeacher
from .models import TeacherRegistration
def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            password = form.cleaned_data['password']
            section = form.cleaned_data['section']

            # Check if the provided credentials are valid
            try:
                teacher = TeacherRegistration.objects.get(teacher_id=teacher_id, password=password, section=section)
                # Store teacher_id in the session for future checks
                request.session['teacher_id'] = teacher_id
                messages.success(request, 'Login successful.')
                # Redirect to teacher_dashboard
                return redirect('teacher_dashboard', section=section)
            except TeacherRegistration.DoesNotExist:
                # return redirect('teacher_dashboard', section=section)
                messages.error(request, 'Invalid credentials. Please try again.')

    else:
        form = TeacherLoginForm()

    return render(request, 'teacher_login.html', {'form': form})







# mini_app2/views.py
import os
import csv
import datetime
from django.shortcuts import render, HttpResponse
from .models import Student
from .utils import get_csv_path, update_attendance_csv

# @login_required(login_url='/teacher_login/')     ##infinite loop --------------------
@never_cache
def teacher_dashboard(request, section):
    now = datetime.datetime.now()
    students_data = Student.objects.filter(section=section)
    csv_file_path = get_csv_path(section, now)

    if request.method == 'POST':
        is_present_list = {}

        # Iterate through the students to get the attendance values
        for student in students_data:
            key = f'student_{student.id}'
            value = request.POST.get(key, 'A')  # Use get() to handle non-selected radio buttons
            is_present_list[key] = value

        update_attendance_csv(csv_file_path, students_data, is_present_list)
        return HttpResponse("Attendance data has been recorded successfully.")

    return render(request, 'teacher_dashboard.html', {'students_data': students_data, 'section': section, 'current_date': now})




# # views.py
# from django.shortcuts import render, HttpResponse
# from .utils import get_csv_path, update_attendance_csv, plot_attendance_graph

# def teacher_dashboard(request, section):
#     now = datetime.datetime.now()
#     students_data = Student.objects.filter(section=section)
#     csv_file_path = get_csv_path(section, now)

#     if request.method == 'POST':
#         is_present_list = {}
#         for student in students_data:
#             key = f'student_{student.id}'
#             value = request.POST.get(key, 'A')
#             is_present_list[key] = value

#         update_attendance_csv(csv_filfor student in students_data:
        # csv_writer.writerow([student.student_id, student.student_name])e_path, students_data, is_present_list)

#         # Read the updated data for visualization
#         with open(csv_file_path, 'r', newline='') as csvfile:
#             csv_reader = csv.reader(csvfile)
#             data = list(csv_reader)

#         # Plot the attendance graph and get the path to the saved image
#         image_path = plot_attendance_graph(data, section)

#         return render(request, 'attendance_success.html', {'image_path': image_path})

#     return render(request, 'teacher_dashboard.html', {'students_data': students_data, 'section': section, 'current_date': now})



@login_required(login_url='/officials/')
def data_analysis(request):     # function name must be data_analysis ************
    students_data = Student.objects.all()
    return render(request, 'data_analysis.html', {'students': students_data})

from django.http import HttpResponse
import csv
from django.contrib import messages

# def export_excel(request):
#     students_data = Student.objects.all()
#     # Create a response object with appropriate headers for an Excel file
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=student_data.csv'

#     csv_writer = csv.writer(response)
#     # headers = ['Student ID', 'Student Name']
#     # csv_writer.writerow(headers)

#     # # Write the student data
#     # 

#     # Define the headers
#     headers = [
#         'Student ID', 'Student Name', 'Student Aadhar', 'Student Phone', 'Student Email',
#         'Gender', 'Date of Birth', 'Address', 'Father Name', 'Father Phone', 
#         'Mother Name', 'Mother Phone', 'School Name', 'Section', 'State', 'City',
#         'Attendance', 'Marks', 'Fees', 'Created At', 'Updated At'
#     ]
#     csv_writer.writerow(headers)

#     # Write the student data
#     for student in students_data:
#         csv_writer.writerow([
#             student.student_id,
#             student.student_name,
#             student.student_aadhar,
#             student.student_phone,
#             student.student_email,
#             student.gender,
#             student.student_dob,
#             student.student_address,
#             student.father_name,
#             student.father_phone,
#             student.mother_name,
#             student.mother_phone,
#             student.school_name,
#             student.section,
#             student.state_name,
#             student.city_name,
#             student.attendance,
#             student.marks,
#             student.fees,
#             student.created_at,
#             student.updated_at,
#         ])

#     excel_download = request.POST.get("excel_download")
#     if 'excel_download' in request.POST: 
#         try:
#                 return response
#         except Exception as e :
#             # return render(request, 'data_analysis.html',{"excel_down":f"Unable to download the excel file , An error occurred: {str(e)}"})
#             messages.error(request, f"Unable to download the excel file. An error occurred: {str(e)}")

#     user_email = request.POST.get('user_email')
#     if user_email:
#         try:
#             # Email the file to the user
#             subject = 'Student Management System'
#             message = 'Student Data excel Sheet attached .'
#             from_email = 'ajdjango3@gmail.com'  
#             to_email = [user_email]  

#             email = EmailMessage(subject, message, from_email, to_email)
#             email.attach('student_data.csv', response.content, 'text/csv')
#             email.send()
#             # del request.session['user_email']
#             # return render(request, 'data_analysis.html', {'students': students_data, 'email_sent': f"Student Data excel Sheet sent to your email. {user_email}"})
#             messages.success(request, f"Student Data excel Sheet sent to your email: {user_email}")
       
#         except Exception as e:
#             messages.error(request, f"Email not sent. An error occurred: {str(e)}")

#             # return render(request, 'data_analysis.html',{"email_not_sent":f"email not send , An error occurred: {str(e)}"})
#             # return HttpResponse(f"email not send , An error occurred: {str(e)}")
#     return render(request, 'data_analysis.html', {'students': students_data})
#     # return render(request, 'data_analysis.html')
import pandas as pd
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import Student

def export_excel(request):
    students_data = Student.objects.all()

    # Convert the students data to a Pandas DataFrame
    data = {
        'Student ID': [student.student_id for student in students_data],
        'Student Name': [student.student_name for student in students_data],
        'Student Aadhar': [student.student_aadhar for student in students_data],
        'Student Phone': [student.student_phone for student in students_data],
        'Student Email': [student.student_email for student in students_data],
        'Gender': [student.gender for student in students_data],
        'Date of Birth': [student.student_dob for student in students_data],
        'Address': [student.student_address for student in students_data],
        'Father Name': [student.father_name for student in students_data],
        'Father Phone': [student.father_phone for student in students_data],
        'Mother Name': [student.mother_name for student in students_data],
        'Mother Phone': [student.mother_phone for student in students_data],
        'School Name': [student.school_name for student in students_data],
        'Section': [student.section for student in students_data],
        'State': [student.state_name for student in students_data],
        'City': [student.city_name for student in students_data],
        'Attendance': [student.attendance for student in students_data],
        'Marks': [student.marks for student in students_data],
        'Fees': [student.fees for student in students_data],
        'Created At': [student.created_at for student in students_data],
        'Updated At': [student.updated_at for student in students_data],
    }
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file in memory
    excel_file = pd.ExcelWriter('student_data.xlsx', engine='xlsxwriter')
    df.to_excel(excel_file, index=False)
    excel_file.save()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_data.xlsx'
    response.write(excel_file)

    # Handle file download
    if request.POST.get('excel_download'):
        try:
            return response
        except Exception as e:
            messages.error(request, f"Unable to download the Excel file. An error occurred: {str(e)}")

    # Handle email sending
    user_email = request.POST.get('user_email')
    if user_email:
        try:
            subject = 'Student Management System'
            message = 'Student Data Excel Sheet attached.'
            from_email = 'ajdjango3@gmail.com'
            to_email = [user_email]

            email = EmailMessage(subject, message, from_email, to_email)
            email.attach('student_data.xlsx', response.content, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()

            messages.success(request, f"Student Data Excel Sheet sent to your email: {user_email}")
        except Exception as e:
            messages.error(request, f"Email not sent. An error occurred: {str(e)}")

    return render(request, 'data_analysis.html', {'students': students_data})


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import matplotlib
matplotlib.use('Agg')  # Use Agg backend which does not require a GUI
# import matplotlib.pyplot as plt
@login_required(login_url='/officials/')
def data_visualization(request):
    try:
        # Retrieve data from the database

        # gender_count = Student.objects.values('gender').annotate(count=Count('id'))
        gender_stats = Student.objects.filter(gender='Male').count(), Student.objects.filter(gender='Female').count()
        attendance_stats = Student.objects.filter(attendance__gt=75).count(), Student.objects.filter(attendance__lte=75).count()
        marks_stats = Student.objects.filter(marks__gt=35).count(), Student.objects.filter(marks__lte=35).count()
        fees_stats = Student.objects.filter(fees='Paid').count(), Student.objects.filter(fees='Unpaid').count()
        
        # age_distribution = Student.objects.values_list('age', flat=True)

        city_distribution = Student.objects.values('city_name').annotate(count=Count('id'))
        state_distribution = Student.objects.values('state_name').annotate(count=Count('id'))
        creation_date_distribution = Student.objects.values_list('created_at', flat=True)
        section_distribution = Student.objects.values('section').annotate(count=Count('id'))

        students_data = Student.objects.all()
        import numpy as np

        # Generate plots        
        plt.figure(figsize=(15, 15))

        # Pie chart for Gender Distribution
        # plt.subplot(4, 4, 1)
        # labels = ['Male', 'Female']
        # plt.pie([entry['count'] for entry in gender_count], labels=labels, autopct='%1.1f%%')
        # plt.title('Gender Distribution')

        # Pie chart for Fees
        plt.subplot(4, 4, 1)
        labels = ['Male', 'Female']
        plt.pie(gender_stats, labels=labels, autopct='%1.1f%%')
        plt.title('Gender Distribution')

        # Pie chart for Attendance
        plt.subplot(4, 4, 2)
        labels = ['Above 75%', '75% and Below']
        plt.pie(attendance_stats, labels=labels, autopct='%1.1f%%')
        plt.title('Attendance Distribution')

        # Pie chart for Marks
        plt.subplot(4, 4, 3)
        labels = ['Pass', 'Fail']
        plt.pie(marks_stats, labels=labels, autopct='%1.1f%%')
        plt.title('Marks Distribution')

        # Pie chart for Fees
        plt.subplot(4, 4, 4)
        labels = ['Paid', 'Unpaid']
        plt.pie(fees_stats, labels=labels, autopct='%1.1f%%')
        plt.title('Fees Distribution')


        # Function to generate fake placement data
        def generate_placement_data(size=100):
            placement_statuses = ['Placed','Placed','Placed', 'Placed','Not Placed']
            return np.random.choice(placement_statuses, size=size)

        # Inside your data_visualization function
        # Generate fake data for placement
        fake_placement_data = generate_placement_data(size=len(students_data))

        # Pie chart for Placement
        # plt.subplot(4, 4, 14)  # Adjust the subplot number as needed
        plt.subplot(4, 4, 5)  # Adjust the subplot number as needed
        labels_placement, counts_placement = np.unique(fake_placement_data, return_counts=True)
        plt.pie(counts_placement, labels=labels_placement, autopct='%1.1f%%')
        plt.title('Placement Status Distribution')



        # Bar graph for City Distribution
        plt.subplot(4, 4, 6)
        cities = [entry['city_name'] for entry in city_distribution]
        city_counts = [entry['count'] for entry in city_distribution]
        plt.bar(cities, city_counts)
        plt.title('City Distribution')
        plt.xlabel('City')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha="right")

        # Bar graph for State Distribution
        plt.subplot(4, 4, 7)
        states = [entry['state_name'] for entry in state_distribution]
        state_counts = [entry['count'] for entry in state_distribution]
        plt.bar(states, state_counts)
        plt.title('State Distribution')
        plt.xlabel('State')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha="right")

        from datetime import datetime, timezone
        # Line graph for Creation Date Distribution
        plt.subplot(4, 4, 8)
        # creation_dates = [datetime.utcfromtimestamp(date.timestamp()).strftime('%Y-%m-%d') for date in creation_date_distribution]
        # Alternatively, you can use datetime.fromtimestamp and specify timezone as UTC
        creation_dates = [datetime.fromtimestamp(date.timestamp(), tz=timezone.utc).strftime('%Y-%m-%d') for date in creation_date_distribution]

        plt.plot(creation_dates)
        plt.title('Creation Date Distribution')
        plt.xlabel('Student')
        plt.ylabel('Creation Date')

        # Line graph for Section Distribution
        plt.subplot(4, 4, 9)
        sections = [entry['section'] for entry in section_distribution]
        section_counts = [entry['count'] for entry in section_distribution]
        plt.plot(sections, section_counts)
        plt.title('Section Distribution')
        plt.xlabel('Section')
        plt.ylabel('Count')
        # Set the number of ticks on the y-axis
        plt.yticks(range(0, max(section_counts) + 1, max(section_counts) // 5))


        ## Matplotlib Box Plot for Marks Distribution
        # plt.subplot(4, 4, 10)
        # plt.boxplot(marks_stats, vert=False)
        # plt.title('Marks Distribution')
        # plt.xlabel('Marks')
        # plt.yticks([])

        
        plt.subplot(4, 4, 10)  # Adjust the subplot number as needed
        section_names = ['CSE', 'CS-DS', 'CS-AI', 'CS-IOT', 'CS-IT']
        section_attendance_counts = [Student.objects.filter(section=section, attendance__gt=75).count() for section in section_names]

        # plt.figure(figsize=(8, 6))
        plt.bar(section_names, section_attendance_counts)    #, color='skyblue'
        plt.xlabel('Section')
        plt.ylabel('No. of Students ')
        plt.title('Section-wise Attendance > 75%')
        

        students_data = Student.objects.all()
        import numpy as np
        # Function to generate fake accommodation data
        def generate_accommodation_data(size=100):
            accommodation_types = ['Hostel','Hostel', 'PG', 'Day Scholar']
            return np.random.choice(accommodation_types, size=size)
        
        # Function to generate fake transportation data
        def generate_transportation_data(size=100):
            transportation_modes = ['Cycle', 'Bike', 'Walk', 'Car', 'Bus', 'Auto', 'Walk']
            return np.random.choice(transportation_modes, size=size)
        
        # Inside your data_visualization function
        # Generate fake data for accommodation and transportation
        fake_accommodation_data = generate_accommodation_data(size=len(students_data))
        fake_transportation_data = generate_transportation_data(size=len(students_data))
        
        # Pie chart for Accommodation Type
        plt.subplot(4, 4, 11)
        labels_accommodation, counts_accommodation = np.unique(fake_accommodation_data, return_counts=True)
        plt.pie(counts_accommodation, labels=labels_accommodation, autopct='%1.1f%%')
        plt.title('Accommodation Distribution')
        
        # Bar graph for Transportation Mode
        plt.subplot(4, 4, 12)
        labels_transportation, counts_transportation = np.unique(fake_transportation_data, return_counts=True)
        plt.bar(labels_transportation, counts_transportation)
        plt.title('Transportation Mode Distribution')
        plt.xlabel('Mode of Transportation')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha="right")
        

        # import numpy as np
        # import matplotlib.pyplot as plt
        # Function to generate fake placement in LPA data
        def generate_placement_lpa_data(size=100):
            placement_lpas = [5, 10, 15, 20, 25, 30]
            return np.random.choice(placement_lpas, size=size)

        # Function to generate fake student enrollment year data
        def generate_enrollment_year_data(size=100):
            enrollment_years = [ 2019, 2020, 2021, 2022,2023]
            return np.random.choice(enrollment_years, size=size)

        # Inside your data_visualization function
        # Generate fake data for placement in LPA and enrollment year
        fake_placement_lpa_data = generate_placement_lpa_data(size=len(students_data))
        fake_enrollment_year_data = generate_enrollment_year_data(size=len(students_data))

        # Line graph for Placement in LPA vs Year
        plt.subplot(4, 4, 13)  # Adjust the subplot number as needed
        years, counts_years = np.unique(fake_enrollment_year_data, return_counts=True)

        # Plot lines for each LPA value
        for lpa_value in [5, 10, 15, 20, 25, 30]:
            counts_placement_years = np.sum(fake_placement_lpa_data == lpa_value)
            plt.plot(years, [counts_placement_years] * len(years), label=f'Placed in {lpa_value} LPA', marker='o')

        plt.title('Placement in LPA vs Year (Line Graph)')
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.legend()
        plt.xticks(rotation=45, ha="right")
        

        # Line graphs for Year vs Placement Statistics (Average, Median, Highest)
        # plt.subplot(4, 4, 16)  # Adjust the subplot number as needed
        import pandas as pd
        df = pd.DataFrame({'Year': fake_enrollment_year_data, 'Placement': fake_placement_lpa_data})
        # Inside your data_visualization function
        # ...

        # Line graphs for Year vs Placement Statistics (Average, Lowest, Highest)
        plt.subplot(4, 4, 14)  # Adjust the subplot number as needed

        years = [2019,2020, 2021, 2022, 2023]

        # Initialize lists to store data for each statistic
        avg_placements = []
        low_placements = []
        high_placements = []

        for year in years:
            year_data = df[df['Year'] == year]['Placement']

            if len(year_data) > 0:
                # Calculate statistics
                average_placement = np.mean(year_data)
                lowest_placement = np.min(year_data) - np.random.uniform(0, 10)  # Increase range for more up and down
                highest_placement = np.max(year_data) + np.random.uniform(0, 50)  # Increase range for more up and down

                # Append values to lists
                avg_placements.append(average_placement)
                low_placements.append(lowest_placement)
                high_placements.append(highest_placement)
            else:
                # If there is no data for the current year, add placeholder values
                avg_placements.append(np.nan)
                low_placements.append(np.nan)
                high_placements.append(np.nan)

        # Plot all three lines in a single graph
        plt.plot(years, avg_placements, marker='o', label='Average', color='blue')
        plt.plot(years, low_placements, marker='o', label='Lowest', color='red')  # Replace 'Median' with 'Lowest'
        plt.plot(years, high_placements, marker='o', label='Highest', color='orange')

        plt.title('Year vs Placement Statistics (Line Graph)')
        plt.xlabel('Year')
        plt.ylabel('Placement in LPA')
        plt.legend()
        # plt.xticks(rotation=45, ha="right")







        # # plt.subplot(4, 5, 14)  # Adjust the subplot number as needed
        # try : 
        #     import csv 
        #     fields=[]
        #     rows=[]
        #     dict={}
        #     with open("mini_pro\my_mini_project\attendance_csv\CSE\CSE_attendance.csv" ,'r') as file:
        #         csvreader=csv.reader(file)
        #         next(csvreader)   # Skip header row
        #         for row in csvreader:
        #             rows.append(row[:])
        #             # dict[row[0]]=

        # except Exception as e :
        #     return HttpResponse(f"Error in csv : {e}")



        # # New function for data visualization
        # # mini_app2/utils.py
        # import os
        # import csv
        # import datetime
        # import matplotlib.pyplot as plt
        # def plot_attendance_graph(data):
        #     sections = data[0][3:]  # Extract section names from headers
        #     attendance_data = list(map(list, zip(*data[1:])))  # Transpose data for easier plotting

        #     x = sections
        #     y = [attendance_data[i].count('P') for i in range(len(attendance_data))]

        #     plt.bar(x, y)
        #     plt.xlabel('Sections')
        #     plt.ylabel('Number of Students Present')
        #     plt.title('Attendance Summary by Section')
        #     # plt.show()





        # Customize layout
        plt.tight_layout()

        # Save the plot to a file
        plot_filename = 'plot.png'
        plot_path = os.path.join('static', 'img', plot_filename)
        plt.savefig(plot_path)    #************
        # plt.close()
        
        # Send email if the user provided an email in the form
        user_email = request.POST.get('user_email')
        if user_email:
            try:
                # Render the data visualization template to a string
                # visualization_html_data = render_to_string('data_analysis.html', context={})

                # Create an EmailMessage object(subject, body ,from_email ,to_email) ********
                email = EmailMessage(
                    'Data Visualization',
                    'Please find the attached visualization.',
                    settings.EMAIL_HOST_USER,  # Replace with your email
                    [user_email],
                )

                # Attach the rendered HTML to the email
                # email.attach('data_analysis.html', visualization_html_data, 'text/html')

                # Attach the plot image to the email
                email.attach_file(plot_path)

                try:
                    # Send the email
                    email.send()
                    # return HttpResponse(f"Data Visualization sent to your email. {user_email}")
                    return render(request, 'data_visualization.html',{"email_sent":f"Data Visualization sent to your email. {user_email}"})
                except Exception as e:
                    # return HttpResponse(f"email not send , An error occurred: {str(e)}")
                    return render(request, 'data_visualization.html',{"email_not_sent":f"email not send , An error occurred: {str(e)}"})

            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")

         # If no email provided, continue with rendering the page
        data = {'plot_path': plot_path, 'user_email': user_email}  # Pass user_email to the template
        return render(request, 'data_visualization.html', data)
    
    except Exception as e:
        return HttpResponse(f"Either your database is empty or an error occured : {str(e)} ")    
    # return render(request, 'data_visualization.html')

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore    
from django.db.models import Q
@login_required(login_url='/officials/')
def search(request):
    if request.method == 'POST':
        # Get user inputs from the form
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        student_aadhar = request.POST.get('student_aadhar')
        student_phone = request.POST.get('student_phone')
        gender = request.POST.get('gender')
        section = request.POST.get('section')

        attendance_from = request.POST.get('attendance_from')
        attendance_to = request.POST.get('attendance_to')
        marks_from = request.POST.get('marks_from')
        marks_to = request.POST.get('marks_to')
        fees = request.POST.get('fees')

        # Starting with an empty query
        query = Q()

        # to extend this query with additional conditions using the & (AND) and | (OR) operators.
        if student_id:
            query &= Q(student_id=student_id)
        if student_name:
            query &= Q(student_name__icontains=student_name)
    
        if student_aadhar:
            # query &= Q(student_aadhar__icontains=student_aadhar)
            query &= Q(student_aadhar=student_aadhar)
        if student_phone:
            query &= Q(student_phone__icontains=student_phone)
        if gender:
            query &= Q(gender = gender)
        if section:
            query &= Q(section__icontains=section)
        if attendance_from:
            query &= Q(attendance__gte=attendance_from)
        if attendance_to:
            query &= Q(attendance__lte=attendance_to)
        if fees:
            query &= Q(fees=fees)
        if marks_from:
            query &= Q(marks__gte=marks_from)
        if marks_to:
            query &= Q(marks__lte=marks_to)

        results = Student.objects.filter(query)
        
        return render(request, 'search.html', {'results': results})

    return render(request, 'search.html', {'results': None})

@login_required(login_url='/officials/')
def download_csv(request):
    # Get user inputs from the form
    student_id = request.POST.get('student_id')
    student_name = request.POST.get('student_name')
    student_aadhar = request.POST.get('student_aadhar')
    student_phone = request.POST.get('student_phone')
    gender = request.POST.get('gender')
    section = request.POST.get('section')

    attendance_from = request.POST.get('attendance_from')
    attendance_to = request.POST.get('attendance_to')
    marks_from = request.POST.get('marks_from')
    marks_to = request.POST.get('marks_to')
    fees = request.POST.get('fees')

    # Starting with an empty query
    query = Q()
    
    # to extend this query with additional conditions using the & (AND) and | (OR) operators.
    if student_id:
        query &= Q(student_id=student_id)
    if student_name:
        query &= Q(student_name__icontains=student_name)

    if student_aadhar:
        # query &= Q(student_aadhar__icontains=student_aadhar)
        query &= Q(student_aadhar=student_aadhar)
    if student_phone:
        query &= Q(student_phone__icontains=student_phone)
    if gender:
        query &= Q(gender=gender)
    if section:
        query &= Q(section__icontains=section)
    if attendance_from:
        query &= Q(attendance__gte=attendance_from)
    if attendance_to:
        query &= Q(attendance__lte=attendance_to)
    if fees:
        query &= Q(fees=fees)
    if marks_from:
        query &= Q(marks__gte=marks_from)
    if marks_to:
        query &= Q(marks__lte=marks_to)

    # Filter the results based on the query
    results = Student.objects.filter(query)

    try:
        # Create a CSV response for download
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=student_data.csv'
        csv_writer = csv.writer(response)
        headers = ['Student ID', 'Student Name', 'Student Phone']
        csv_writer.writerow(headers)

        for student in results:
            csv_writer.writerow([student.student_id, student.student_name, student.student_phone])

        return response   # Return the CSV response

    except Exception as e:
        messages.error(request, f"Unable to download the excel file. An error occurred: {str(e)}")
        return render(request, 'search.html', {'results': results})  # Render the search results if download fails
    

@login_required(login_url='/officials/')
def email_download_csv(request):
    # Get user inputs from the form
    student_id = request.POST.get('student_id')
    student_name = request.POST.get('student_name')
    student_aadhar = request.POST.get('student_aadhar')
    student_phone = request.POST.get('student_phone')
    gender = request.POST.get('gender')
    section = request.POST.get('section')

    attendance_from = request.POST.get('attendance_from')
    attendance_to = request.POST.get('attendance_to')
    marks_from = request.POST.get('marks_from')
    marks_to = request.POST.get('marks_to')
    fees = request.POST.get('fees')

    # Starting with an empty query
    query = Q()
    # to extend this query with additional conditions using the & (AND) and | (OR) operators.
    if student_id:
        query &= Q(student_id=student_id)
    if student_name:
        query &= Q(student_name__icontains=student_name)

    if student_aadhar:
        # query &= Q(student_aadhar__icontains=student_aadhar)
        query &= Q(student_aadhar=student_aadhar)
    if student_phone:
        query &= Q(student_phone__icontains=student_phone)
    if gender:
        query &= Q(gender=gender)
    if section:
        query &= Q(section__icontains=section)
    if attendance_from:
        query &= Q(attendance__gte=attendance_from)
    if attendance_to:
        query &= Q(attendance__lte=attendance_to)
    if fees:
        query &= Q(fees=fees)
    if marks_from:
        query &= Q(marks__gte=marks_from)
    if marks_to:
        query &= Q(marks__lte=marks_to)

    results = Student.objects.filter(query)

    user_email = request.POST.get('user_email')
    if user_email:
        try:
            # Create a CSV response for download
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=student_data.csv'
            csv_writer = csv.writer(response)
            headers = ['Student ID', 'Student Name', 'Student Phone']
            csv_writer.writerow(headers)

            for student in results:
                csv_writer.writerow([student.student_id, student.student_name, student.student_phone, ])

            subject = 'Student Management System'
            message = 'Student Data excel Sheet attached .'
            from_email = 'ajdjango3@gmail.com'  
            to_email = [user_email]  
            # to_email = [request.POST.get('user_email')
            email = EmailMessage(subject, message, from_email, to_email)
            email.attach('student_data.csv', response.content, 'text/csv')
            email.send()    # del request.session['user_email'

            
            # if 'user_email' in request.POST:
            #     del request.session['user_email']
            messages.success(request, f"Student Data excel Sheet sent to your email: {user_email}")
            
        except Exception as e:
            messages.error(request, f"Email not sent. An error occurred: {str(e)}")
        # del request.POST['user_email']
            
    return render(request, 'search.html', {'results': results})  # Render the search results if download fails
    
@login_required(login_url='/officials/')
def delete_selected(request):
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students')
        delete_action = request.POST.get('delete_action')
        
        if delete_action == 'delete_all':
            # Delete all shown students
            Student.objects.all().delete()
            
        elif delete_action == 'delete_selected':
            # Delete selected students
            Student.objects.filter(id__in=selected_students).delete()
            
        return redirect('search')

    return render(request, 'search.html', {'results': None})

@login_required(login_url='/officials/')
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        # Update the student details based on the form submission

        student.student_id = request.POST.get('student_id')     #********************
        student.student_name = request.POST.get('student_name')
        student.student_aadhar = request.POST.get('student_aadhar')
        student.student_phone = request.POST.get('student_phone')
        student.student_email = request.POST.get('student_email')

        # student.age = request.POST.get('age')
        
        student.gender = request.POST.get('gender')
        student.student_dob = request.POST.get('student_dob')
        student.student_address = request.POST.get('student_address')
        student.father_name = request.POST.get('father_name')
        student.father_phone = request.POST.get('father_phone')
        student.mother_name = request.POST.get('mother_name')
        student.mother_phone = request.POST.get('mother_phone')
        student.school_name = request.POST.get('school_name')
        student.section = request.POST.get('section')
        student.state_name = request.POST.get('state_name')
        student.city_name = request.POST.get('city_name')
        student.attendance = request.POST.get('attendance')
        student.marks = request.POST.get('marks')
        student.fees = request.POST.get('fees')

        student.save()
        return redirect('search')

    return render(request, 'update_student.html', {'student': student})





def generate_unique_id_aadhar():
    student_id = fake.unique.random_number(digits=8)
    student_aadhar = fake.unique.random_number(digits=10)
    return student_id, student_aadhar

def add_random_students():
    for _ in range(30):
        student_id, student_aadhar = generate_unique_id_aadhar()

        student = Student(
            student_id=student_id,
            student_name=random.choice(['Aditya', 'Aryan','Ravi','Prakash','Deepak','Diya', 'Payal','Priya','Rani','Harry']),
            student_aadhar=student_aadhar,
            student_phone=random.randint(11111, 2522222),
            student_email=fake.email(),
            # age=random.choice([19,20,21,22,23]),
            gender=random.choice(["Male","Female"]),
            student_dob=fake.date_of_birth(),
            student_address=fake.address(),
            father_name=fake.name(),
            father_phone=random.randint(11111, 2522222),
            mother_name=fake.name(),
            # mother_phone=fake.phone_number(),
            mother_phone=random.randint(11111, 2522222),
            # school_name=fake.company(),
            school_name=''.join(random.choice(["ABESIT", "AKG", "ABES", "KVS", "Doc"])),
            # section=random.choice(['CSE']),
            section=random.choice(['CSE','CS-DS','CS-AI','CS-IOT','CS-IT']),
            state_name=fake.random.choice(['Gujrat','Delhi','Delhi', 'UP', 'Bihar','J&K','kerala','Others']),
            city_name=fake.random.choice(['Ahmedabad','Ghaziabad', 'Lucknow', 'Patna','Srinagar','Thiruvananthapuram','Others']),
            attendance=random.randint(50, 100),
            marks=random.randint(50, 100),
            fees=random.choice(['Paid','Paid','Paid','Unpaid']),
            created_at=timezone.now(),
            updated_at=timezone.now(),
         )
#         student.save()   #!!!!!!! ctrl+S  or  Refresh to execution
# add_random_students()


# kundan.rautela@abesit.edu.in
# krishna.dubey@abesit.in

