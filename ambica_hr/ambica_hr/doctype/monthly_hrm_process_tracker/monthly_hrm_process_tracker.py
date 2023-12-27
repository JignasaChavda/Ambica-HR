# Copyright (c) 2023, jignasha and contributors
# For license information, please see license.txt

import calendar
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import re

class MonthlyHRMProcessTracker(Document):
	pass

@frappe.whitelist()
def get_user(): 
    current_user = frappe.session.user
    # "mailto:priyanka@sanskartechnolab.com"

    child_data = frappe.get_all('Compliance User', filters={'user': ('like', f'%{current_user}%')}, fields=['parent', 'user'])

    parents_in_child_data = set(record['parent'] for record in child_data)

    data = frappe.get_all('Monthly HRM Process Tracker', filters={'name': ('in', list(parents_in_child_data))}, fields=['name', 'date', 'kra', 'sub_process'])
    
    custom_message = []
   
    for record in data:
        date_value_str = record['date']
       
        match = re.match(r'(\d+)[a-z]*\s+of\s+([a-zA-Z]+)', date_value_str)
        
        day_of_month = int(match.group(1))
        month_str = match.group(2)
        
        if month_str.lower() == "every":
            month_num = datetime.now().month
        else:
            month_num = list(calendar.month_name).index(month_str.capitalize())
        
        last_day_of_month = calendar.monthrange(datetime.now().year, month_num)[1]
       
        if day_of_month > last_day_of_month:
             day_of_month = last_day_of_month
             
        given_date = datetime(datetime.now().year, month_num, day_of_month, 23, 59, 59, 999999)
        one_week_before_given_date = given_date - timedelta(days=7)
        today_date = datetime.now()
        
        if one_week_before_given_date <= today_date <= given_date:
            custom_message.append(record['custom_kra'] + " " + record['custom_sub_process'])
            
        # custom_message.append({
        #      "month_num": month_num,
        #      "day_of_month": day_of_month,
        #     'given_date': given_date,
        #     'one_week_before_given_date': one_week_before_given_date,
        #     'today_date': today_date
        # })
    return custom_message

