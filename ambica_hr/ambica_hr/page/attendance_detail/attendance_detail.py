import calendar
import frappe


@frappe.whitelist()
def get_attendance_details(month=None, year=None, department=None, employee=None):


   # from_date = frappe.utils.get_datetime_str(frappe.utils.data.get_datetime(from_date)) if from_date else None
   # to_date = frappe.utils.get_datetime_str(frappe.utils.data.get_datetime(to_date)) if to_date else None
  
   query = """
       SELECT
           `Employee`, `Attendance_Date`, `Status`, FORMAT(ROUND(`Custom_Derived_Present_Minutes`,4),4) AS `Custom_Derived_Present_Minutes`, `Leave_Type`
       FROM
           `tabAttendance`
       WHERE 1=1
   """
   # FORMAT(ROUND(`Custom_Derived_Present_Minutes`,4),4) AS


   query2 = """
       SELECT
           DISTINCT
           `Employee`,
           `Employee_Name`,
           `Department`,
           DATE_FORMAT(`Custom_Probation_Date`, '%%d-%%m-%%Y') AS `Custom_Probation_Date`,
           `Shift`
       FROM
           `tabAttendance`
       WHERE 1=1
   """


   params = []


   if month:
       query += " AND MONTH(`Attendance_Date`) = %s"
       params.append(month)


   if year:
       query += " AND YEAR(`Attendance_Date`) = %s"
       params.append(year)


   if department and department != 'All Departments':
       query += " AND `Department` = %s"
       params.append(department)


   if employee:
       query += "AND `Employee` = %s"
       params.append(employee)


   # if from_date and to_date:
       # query += "AND `Attendance_Date` BETWEEN %s AND %s "
   # if month:
   #     query += "AND MONTH(`Attendance_Date`) = %s"
   # if year:
   #     query += "AND YEAR(`Attendance_Date`) = %s"
   # if department:
   #     if department != 'All Departments':
   #         query += " AND `Department` = %s"
   # # if department:
   # #     query += "AND `Department` = %s"
   # # if department:
   # #     if department != 'All Departments':
   # #         query2 += "AND `Department` = %s"
   # #     else:
   # #         query2 = query2
   # # elif department and department == 'All Departments':
   # if employee:
   #     query += "AND `Employee` = %s"


   # if from_date and to_date:
       # query2 += "AND DATE(`Attendance_Date`) BETWEEN %s AND %s "
   if month:
       query2 += "AND MONTH(`Attendance_Date`) = %s"
   if year:
       query2 += "AND YEAR(`Attendance_Date`) = %s"
   if department:
       if department != 'All Departments':
           query2 += " AND `Department` = %s"
   if employee:
       query2 += "AND `Employee` = %s"
  
   # params = []
   # # if from_date and to_date:
   #     # params.extend([from_date, to_date])
   # if month:
   #     params.append(month)
   # if year:
   #     params.append(year)
   # if department:
   #     params.append(department)
   # if employee:
   #     params.append(employee)


   attendance_details = frappe.db.sql(query, tuple(params), as_dict=True)
   employees = frappe.db.sql(query2, tuple(params), as_dict=True)


   organized_details = {}
   for attendance_detail in attendance_details:
       employee_id = attendance_detail['Employee']
       if employee_id not in organized_details:
           organized_details[employee_id] = {'details': [], 'days': {}}


       organized_details[employee_id]['details'].append(attendance_detail)


       day = attendance_detail['Attendance_Date'].day
       organized_details[employee_id]['days'][day] = attendance_detail


   for employee in employees:
       employee_id = employee['Employee']
       if employee_id in organized_details:
           sorted_details = sorted(organized_details[employee_id]['details'], key=lambda x: x['Attendance_Date'])
           employee['attendance_details'] = sorted_details
      
       total_minutes = sum(float(detail['Custom_Derived_Present_Minutes']) for detail in sorted_details)
       rounded_total = format(round(total_minutes, 4), '.4f')
       employee['total_minutes'] = rounded_total


       total_week_off = 0
       total_public_holiday = 0
       total_casual_leave = 0
       total_sick_leave = 0
       total_privilege_leave = 0


       for detail in sorted_details:
           status = detail['Status']
           leave_type = detail.get('Leave_Type', '')


           if status == 'Week Off':
               total_week_off += 1
           elif status == 'Public Holiday':
               total_public_holiday += 1
           elif status == 'On Leave':
               if leave_type == "Casual Leave":
                   total_casual_leave += 1
               elif leave_type == "Sick Leave":
                   total_sick_leave += 1
               elif leave_type == "Privilege Leave":
                   total_privilege_leave += 1


       employee['total_week_off'] = total_week_off
       employee['total_public_holiday'] = total_public_holiday
       employee['total_casual_leave'] = total_casual_leave
       employee['total_sick_leave'] = total_sick_leave
       employee['total_privilege_leave'] = total_privilege_leave
      
       total_days = float(rounded_total) + total_week_off + total_public_holiday + total_privilege_leave + total_casual_leave + total_sick_leave
       employee['total_days'] = format(round(total_days, 4), '.4f')


       if month and year:
           days_in_month = calendar.monthrange(int(year), int(month))[1]


           # Initialize a list to store key-value pairs for each day
           employee['days'] = []


           # Append key-value pairs to the employee list
           for day in range(1, days_in_month + 1):
               if day in organized_details.get(employee_id, {}).get('days', {}):
                   # Append key-value pair for dates with attendance details
                   employee['days'].append({'details': organized_details[employee_id]['days'][day]})
               else:
                   # Append an empty key-value pair for dates without attendance details
                   employee['days'].append({'day': day, 'details': {}})


   return employees
