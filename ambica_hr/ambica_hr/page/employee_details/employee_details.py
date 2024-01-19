import frappe
import calendar


@frappe.whitelist()
def get_salary_slips(month=None, year=None, department=None, designation=None, company=None, branch=None, status=None, employee=None):
  
   query = """
       SELECT
           `Name`, `Employee_Name`, `Employee`, `Designation`, `Department`, `pf_account_number`, `Bank_Account_No`,
           Format(Round(`Total_Working_Days`,4),4) AS `Total_Working_Days`,
           Format(Round(`Absent_Days`,4),4) AS `Absent_Days`,
           Format(Round(`CL`,4),4) AS `CL`,
           Format(Round(`PL`,4),4) AS `PL`,
           # Format(Round(`Custom_PH`,4),4) AS `Custom_PH`,
           # Format(Round(`Custom_WO`,4),4) AS `Custom_WO`,
           Format(Round(`Leave_Without_Pay`,4),4) AS `Leave_Without_Pay`,
           Format(Round(`Payment_Days`,4),4) AS `Payment_Days`,
           Format(Round(`Gross_Pay`,2),2) AS `Gross_Pay`,
           Format(Round(`Total_Deduction`,2),2) AS `Total_Deduction`,
           Format(Round(`Net_Pay`,2),2) AS `Net_Pay`,
           Format(Round(`Payment_Days`+`CL`+`PL`,4),4) AS `Total_days`
       FROM
           `tabSalary Slip`
       WHERE 1=1
   """


   query2 = """
       SELECT
           `Salary_Component`, `Parent`, `custom_earning_component_type`, `custom_incentive_type`, `custom_pf_account_contribution`,
           Format(Round(`Amount`, 2),2) AS `Amount`, `custom_type`,
           `custom_difference_type`, `custom_deduction_component_type`, `custom_is_income_tax_component`, `custom_canteen_type`
       FROM
           `tabSalary Detail`
       WHERE
           `Parent` LIKE 'Sal Slip%' """
  
   params = []


   if month:
       query += " AND MONTH(`Start_Date`) = %s"
       params.append(month)


   if year:
       query += " AND YEAR(`Start_Date`) = %s"
       params.append(year)


   if department and department != 'All Departments':
       query += " AND `Department` = %s"
       params.append(department)


   if designation:
       query += "AND `Designation` = %s"
       params.append(designation)


   if company:
       query += "AND `Company` = %s"
       params.append(company)


   if branch:
       query += "AND `Branch` = %s"
       params.append(branch)


   if status:
       query += "AND `status` = %s"
       params.append(status)


   if employee:
       query += "AND `Employee` = %s"
       params.append(employee)


   salary_slips = frappe.db.sql(query, tuple(params), as_dict=True)
   salary_component = frappe.db.sql(query2, as_dict=True)


   employee_data = frappe.get_all("Employee", fields=["name"])


   earning_data = []
   for employee in employee_data:
       employee_doc = frappe.get_doc("Employee", employee.name)


       for earning in employee_doc.get("custom_earnings"):
           earning_data.append({
               "employee_id": employee.name,
               "salary_component": earning.salary_component,
               "amount": "{:.2f}".format(earning.amount),
               "earning_component_type": earning.custom_earning_component_type
           })


   organized_details = {}
   for detail in salary_component:
       parent = detail['Parent']
       if parent not in organized_details:
           organized_details[parent] = []
       organized_details[parent].append(detail)


   for slip in salary_slips:
       parent = slip['Name']
       if parent in organized_details:
           slip['details'] = organized_details[parent]
           slip['earning_data'] = [earning for earning in earning_data if earning["employee_id"] == slip["Employee"]]
       else:
           slip['details'] = []
           slip['earning_data'] = []


   for slip in salary_slips:
       total_rate = 0
       for earning in slip['earning_data']:
           total_rate += float(earning['amount'])
       slip['total_rate'] = "{:.2f}".format(total_rate)


   # Convert company to uppercase
   company = company.upper()


   month_number = int(month)
   month_name = calendar.month_name[month_number]


   year = year
   # print(month_name + " - " + year)


   query3 = """
       SELECT `custom_pf_number`, `custom_esi_number` FROM `tabCompany` WHERE
       `name` = %s
   """


   numbers = frappe.db.sql(query3, (company), as_dict=True)


   pf_no = None
   esi_no = None


   for number in numbers:
       pf_no = number.get('custom_pf_number', None)
       esi_no = number.get('custom_esi_number', None)


   query4 = """
       SELECT `address_line1`, `address_line2`, `city`, `state`, `pincode` FROM `tabAddress` WHERE
       `address_title` = %s
   """


   address_list = frappe.db.sql(query4, (company), as_dict=True)


   address = ""  # Initialize an empty string to concatenate the individual addresses


   if address_list:
       for individual_address in address_list:
           # Assuming individual_address is a dictionary
           address += (
               individual_address.get('address_line1', '') + ", " +
               individual_address.get('address_line2', '') + ", " +
               individual_address.get('city', '') + ", " +
               individual_address.get('state', '') + "- " +
               individual_address.get('pincode', '')
           )


   return salary_slips, company, pf_no, esi_no, address, month_name, year


@frappe.whitelist()
def get_branches(company=None):
   query = """
       SELECT `name` FROM `tabBranch` WHERE
       `custom_company` = %s
   """
   query2 = """
       SELECT `custom_pf_number`, `custom_esi_number` FROM `tabCompany` WHERE
       `name` = %s
   """
   query3 = """
       SELECT `address_line1`, `address_line2`, `city`, `state`, `pincode` FROM `tabAddress` WHERE
       `address_title` = %s
   """


   branches = frappe.db.sql(query, (company), as_dict=True)
   numbers = frappe.db.sql(query2, (company), as_dict=True)
   address_list = frappe.db.sql(query3, (company), as_dict=True)


   for number in numbers:
       pf_no = number['custom_pf_number']
       esi_no = number['custom_esi_number']
  
   address = ""  # Initialize an empty string to concatenate the individual addresses


   if address_list:
       for individual_address in address_list:
           # Assuming individual_address is a dictionary
           address += (
               individual_address.get('address_line1', '') + ", " +
               individual_address.get('address_line2', '') + ", " +
               individual_address.get('city', '') + ", " +
               individual_address.get('state', '') + "- " +
               individual_address.get('pincode', '')
           )


   return branches, pf_no, esi_no, address


