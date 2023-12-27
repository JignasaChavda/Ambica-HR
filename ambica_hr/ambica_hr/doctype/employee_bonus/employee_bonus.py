# Copyright (c) 2023, jignasha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class EmployeeBonus(Document):
	pass

@frappe.whitelist()
def get_employee_data(category, department):
        try:
            filters = {}

            if department and category:
                if department != 'All Departments':
                    filters['department'] = department
                filters['employment_type'] = category
            elif department:
                if department != 'All Departments':
                    filters['department'] = department
            elif category:
                filters['employment_type'] = category
            else:
                filters = None
            
            employee_data = frappe.get_all(
                "Employee",
                filters= filters,
                fields=['employee','employee_name','department','designation']
            )

            # frappe.msgprint("message:", department)
            # frappe.msgprint("Employee Data: {}".format(employee_data))
            
            return employee_data
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Failed to fetch employee data")
            return None
