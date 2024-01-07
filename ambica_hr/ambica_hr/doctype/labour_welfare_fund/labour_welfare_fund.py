# Copyright (c) 2023, jignasha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
import json
from datetime import datetime
import calendar
from frappe import db




class LabourWelfareFund(Document):
	def on_submit(self):
                
            data = []
            for row in self.category:
                data.append(row.employment_type)
            
            employee_data = frappe.get_all(
            "Employee",
            filters={'employment_type': ['in', data]},
            fields=['employee']
            )

            employee_ids = [data['employee'] for data in employee_data]

            posting_date = self.posting_date 
            date_object = datetime.strptime(posting_date, '%Y-%m-%d')
            month = date_object.month

            salary_slip_start_date = frappe.db.get_all("Salary Slip", fields=['start_date'])
            filtered_data = [entry for entry in salary_slip_start_date if entry['start_date'].month == month]
            extracted_dates = [entry['start_date'] for entry in filtered_data]

            salary_slip = frappe.get_all(
            "Salary Slip",
            filters={'employee': ['in', employee_ids], 'docstatus': 0, 'start_date': ['in', extracted_dates]},
            fields=['name','employee']
            )
            
            slip_ids = [data['name'] for data in salary_slip]
            employees = [data['employee'] for data in salary_slip]
            not_in_employees = set(employee_ids) - set(employees)

            for slip_data in slip_ids:
                    slip = frappe.get_doc("Salary Slip", slip_data)
                    slip.append ('deductions', {'salary_component': self.component, 'amount': self.employee_contribution})
                    slip.save() 

@frappe.whitelist(allow_guest=True)
def get_employee_data(category, department, posting_date):
    try:
        if posting_date:
            if category or department:
                message_object = json.loads(category)
                employment_types = [item["employment_type"] for item in message_object]

                filters = {}

                if department:
                    filters['department'] = department

                if employment_types:
                    filters['employment_type'] = ['in', employment_types]

                if department and employment_types:
                    filters['department'] = department
                    filters['employment_type'] = ['in', employment_types]
                
                employee_data = frappe.get_all(
                    "Employee",
                    filters=filters,
                    fields=['employee', 'employee_name', 'department', 'designation', 'employment_type']
                )
                    
                if not employee_data:
                    frappe.throw("No employee data found for the specified filters")
                return employee_data

                
            
            else:
                frappe.throw("Select Category or Department filter")
        else:
            frappe.throw("Select Posting Date")

    except Exception as e:
        frappe.log_error("Select Category or Department filter")