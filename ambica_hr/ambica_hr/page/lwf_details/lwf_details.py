import frappe
from datetime import datetime


@frappe.whitelist()
def get_lwf_details(from_date=None, to_date=None):


   query = """
       SELECT
           DISTINCT `Custom_Company`
       FROM
           `tabLabour Welfare Fund`
   """


   query2 = """
       SELECT
           `Employee`
       FROM
           `tabLWF`
       WHERE
           `Parent` IN (
               SELECT
                   `Name`
               FROM
                   `tabLabour Welfare Fund`
               WHERE
                   `Posting_Date` BETWEEN %s AND %s
           )
   """


   query3 = """
       SELECT
           `address_line1`, `address_line2`, `city`, `state`, `pincode`, `phone`
       FROM
           `tabAddress`
       WHERE
           `Address_Title` = 'SHRI AMBICA POLYMER PVT LTD'
   """   


   lwf_details = frappe.db.sql(query, as_dict=True)
   employees = frappe.db.sql(query2, (from_date, to_date), as_dict=True)
   address = frappe.db.sql(query3, as_dict=True)
   today_date = datetime.today().strftime('%d-%m-%Y')


   company_name = lwf_details[0]['Custom_Company'] if lwf_details else None   
   total_employee = len(employees)
   employees_share = format(round(total_employee*6,2),'.2f')
   employers_share = format(round(total_employee*12,2),'.2f')
   total = format(round((float(employees_share) + float(employers_share)),2),'.2f')


   return company_name, total_employee, employees_share, employers_share, total, today_date, address


