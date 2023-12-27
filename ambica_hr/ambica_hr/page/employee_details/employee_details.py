import frappe

@frappe.whitelist()
def get_salary_slips():
    
    query = """
        SELECT
            s.`Name`, s.`Employee_Name`, s.`Employee`, s.`Designation`, s.`Department`, s.`Bank_Account_No`,
            s.`Total_Working_Days`, s.`Absent_Days`, s.`Custom_CL`, s.`Custom_PL`, s.`Custom_PH`, s.`Custom_WO`,
            s.`Leave_Without_Pay`, s.`Payment_Days`, s.`Gross_Pay`, s.`Total_Deduction`, s.`Net_Pay`
        FROM
            `tabSalary Slip` s
    """

    query2 = """
        SELECT d.`Salary_Component`, d.`Amount`, d.`Parent` FROM `tabSalary Detail` d WHERE
        d.`Parent` LIKE 'Sal Slip%' """

    salary_slips = frappe.db.sql(query, as_dict=True)
    salary_component = frappe.db.sql(query2, as_dict=True)

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
        else:
            slip['details'] = []

    return salary_slips