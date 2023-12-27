
import frappe

@frappe.whitelist()
def get_attendance_details():
    
    query = """
        SELECT
            `Employee`, `Attendance_Date`, `Status`, `Custom_Derived_Present_Minutes`, `Leave_Type`
        FROM
            `tabAttendance` 
        WHERE
            MONTH(`Attendance_Date`) = 11;
    """
    query2 = """
        SELECT
            DISTINCT `Employee`, `Employee_Name`, `Department`, `Custom_Probation_Date`, `Shift`
        FROM
            `tabAttendance`
    """
    attendance_details = frappe.db.sql(query, as_dict=True)
    employees = frappe.db.sql(query2, as_dict=True)

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
            employee['days_details'] = organized_details[employee_id]['days']
        else:
            employee['attendance_details'] = []
            employee['days_details'] = {}

    return employees