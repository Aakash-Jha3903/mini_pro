

# mini_app2/utils.py
import os
import csv
import datetime

def get_csv_path(section, date):
    csv_dir = os.path.join('attendance_csv', section)
    os.makedirs(csv_dir, exist_ok=True)
    csv_file = f"{section}_attendance.csv"  # Simplified file name for daily att.
    # csv_file = f"{date.strftime('%Y%m%d')}.csv"
    return os.path.join(csv_dir, csv_file)

def update_attendance_csv(csv_file_path, students_data, is_present_list):
    now = datetime.datetime.now()
    # today = datetime.date.today()
    # now = today + datetime.timedelta(days=1)

    file_exists = os.path.exists(csv_file_path)

    if file_exists:
        with open(csv_file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = list(csv_reader)

            # Get the headers from the existing data
            headers = data[0]

            # Get the last date in the file
            last_date = headers[-1] if len(headers) > 2 else None

            # If the last date matches today's date, update the attendance
            if last_date == now.strftime('%Y-%m-%d'):
                new_attendance = [is_present_list.get(f'student_{student.id}', 'A') for student in students_data]
                data[0] = headers
                for i, student_row in enumerate(data[1:]):
                    student_row.append(new_attendance[i])

                # for i, student in enumerate(students_data):
                #     student_id = student.student_id
                #     is_present = is_present_list.get(f'student_{student_id}', 'A')
                #     data[i + 1].append(is_present)

            else:
                # If the last date is different, add a new column for today's date
                headers.append(f'{now.strftime("%Y-%m-%d")}')
                new_attendance = [is_present_list.get(f'student_{student.id}', 'A') for student in students_data]
                data[0] = headers
                for i, student_row in enumerate(data[1:]):
                    student_row.append(new_attendance[i])

        # Write the updated data back to the file
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
    else:
        # If the file doesn't exist, create a new file and write headers
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            headers = ['Student ID', 'Student Name', 'Date', f'{now.strftime("%Y-%m-%d")}']
            csv_writer.writerow(headers)

            for student in students_data:
                is_present = is_present_list.get(f'student_{student.id}', 'A')
                csv_writer.writerow([student.student_id, student.student_name, now.strftime('%Y-%m-%d'), is_present])

