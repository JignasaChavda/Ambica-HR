# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class DuplicateAssignment(frappe.ValidationError):
	pass


class SalaryStructureAssignment(Document):

	def on_submit(self):
		emp = self.employee
		CTC = self.base

		basic_amount = 0
		pf_acc_1 = 0
		pf_acc_10 = 0
		
		

		
		# Set salary structure and salary structure assignment
		ans = frappe.db.get_list("Salary Structure Assignment", filters={"employee": emp, "docstatus": 1}, fields=["name","salary_structure"], order_by="creation DESC", limit=1, as_list=True)
		current_assignment = ans[0][0]
		current_structure = ans[0][1]

		if current_assignment:
			frappe.db.set_value("Employee", emp, 'custom_salary_structure_assignment', current_assignment)
			frappe.db.set_value("Employee", emp, 'custom_salary_structure', current_structure)

			
		employee = frappe.get_doc("Employee", emp)
				
		employee.get("custom_earnings").clear()
		employee.get("custom_deductions").clear()

		
		salary_components = frappe.get_all("Salary Detail", filters={"parent": current_structure}, fields=['salary_component', 'formula'], order_by="idx Asc")	
		for component in salary_components:
			component_name = component.salary_component
			component_formula = component.formula

			if component_name:

				# Earnings
				earning_component_details = frappe.get_all("Salary Component", filters={"name": component_name, "type": "Earning"}, fields=["name","type", "earning_component_type", "formula"])
				for com in earning_component_details:
					earning_com_nm = com.name
					earning_com_type = com.earning_component_type
					earning_com_formula = com.formula

					
					if earning_com_type == "Basic Pay":
						if earning_com_formula:
							context = {"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
							basic_result = eval(component_formula, context)
							if basic_result is not None:
								new_earning = employee.append("custom_earnings", {})
								new_earning.salary_component = earning_com_nm
								new_earning.custom_component_type = earning_com_type
								new_earning.amount = basic_result
								basic_amount = basic_result
								# new_earning.annual_amount = result*12								
								employee.save()
						else:
							new_earning = employee.append("custom_earnings", {})
							new_earning.salary_component = earning_com_nm
							new_earning.custom_component_type = earning_com_type
							new_earning.amount = 0
							basic_amount = 0
							# new_earning.annual_amount = result*12								
							employee.save()
									

					if earning_com_type in ["HRA", "Conveyance Allowance"]:
						if earning_com_formula:
							context = {"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
							result = eval(component_formula, context)
							if result is not None:
								new_earning = employee.append("custom_earnings", {})
								new_earning.salary_component = earning_com_nm
								new_earning.custom_component_type = earning_com_type
								new_earning.amount = result
								# new_earning.annual_amount = result*12
								employee.save()
						else:
							new_earning = employee.append("custom_earnings", {})
							new_earning.salary_component = earning_com_nm
							new_earning.custom_component_type = earning_com_type
							new_earning.amount = 0
							basic_amount = 0
							# new_earning.annual_amount = result*12								
							employee.save()


					if earning_com_type in ["Gratuity", "Bonus", "Leave Benefit", "Canteen Benefit"]:
						if earning_com_formula:
							context = {"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
							result = eval(component_formula, context)
							new_earning = employee.append("custom_benefits", {})
							new_earning.salary_component = earning_com_nm
							new_earning.custom_component_type = earning_com_type
							new_earning.amount = result
							# new_earning.annual_amount = result*12
							employee.save()
						else:
							new_earning = employee.append("custom_benefits", {})
							new_earning.salary_component = earning_com_nm
							new_earning.custom_component_type = earning_com_type
							new_earning.amount = 0
							basic_amount = 0
							# new_earning.annual_amount = result*12								
							employee.save()
							


				
				# Deductions
				deduction_component_details = frappe.get_all("Salary Component", filters={"name": component_name, "type": "Deduction"}, fields=["name","type", "is_income_tax_component", "component_type", "pf_account_contribution", "formula", "canteen_type"])
				for com in deduction_component_details:
					deduction_com_nm = com.name
					deduction_com_type = com.component_type
					pf_type = com.pf_account_contribution
					deduction_com_formula = com.formula
					canteen_type = com.canteen_type

					if (deduction_com_type == "Provident Fund"):
						if (pf_type == "Employer's Contri A/C No. 1"):
							if deduction_com_formula:
								context = {"B":basic_amount,"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
								pf_acc_1 = eval(deduction_com_formula, context)
						
						if (pf_type == "Employer's Contri A/C No. 10"):
							if deduction_com_formula:
								context = {"B":basic_amount,"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
								pf_acc_10 = eval(deduction_com_formula, context)
								
						if (pf_type == "Employer's Total Contribution (A/C No.1+A/C No.10)"):
							if deduction_com_formula:
								context = {"PF_1":pf_acc_1, "PF_10":pf_acc_10}
								result = eval(deduction_com_formula, context)
								if result is not None:
									new_earning = employee.append("custom_benefits", {})
									new_earning.salary_component = component_name
									new_earning.amount = result
									# new_earning.annual_amount = result*12
									employee.save()
							else:
								new_earning = employee.append("custom_benefits", {})
								new_earning.salary_component = component_name
								new_earning.amount = 0
								# new_earning.annual_amount = result*12
								employee.save()

						if (pf_type == "Employee's Contri A/C No. 1"):
							if deduction_com_formula:
								context = {"B":basic_amount,"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
								result = eval(deduction_com_formula, context)
								if result is not None:
									new_earning = employee.append("custom_deductions", {})
									new_earning.salary_component = component_name
									new_earning.amount = result
									# new_earning.annual_amount = result*12
									employee.save()
							else:
								new_earning = employee.append("custom_benefits", {})
								new_earning.salary_component = component_name
								new_earning.amount = 0
								# new_earning.annual_amount = result*12
								employee.save()

			
					elif deduction_com_type in  ["Professional Tax","Canteen Deduction"]:
						if deduction_com_formula:
							context = {"B":basic_amount,"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
							result = eval(deduction_com_formula, context)
							if result is not None:
								new_earning = employee.append("custom_deductions", {})
								new_earning.salary_component = component_name
								new_earning.amount = result
								new_earning.annual_amount = result*12
								employee.save()
						else:
								new_earning = employee.append("custom_benefits", {})
								new_earning.salary_component = component_name
								new_earning.amount = 0
								# new_earning.annual_amount = result*12
								employee.save()

					elif (deduction_com_type == "Canteen Deduction") and (canteen_type == None):
						if deduction_com_formula:
							context = {"B":basic_amount,"base": CTC, "employment_type": employee.employment_type, "custom_payroll_category":employee.custom_payroll_category}
							result = eval(deduction_com_formula, context)
							if result is not None:
								new_earning = employee.append("custom_deductions", {})
								new_earning.salary_component = component_name
								new_earning.amount = result
								new_earning.annual_amount = result*12
								employee.save()
						else:
								new_earning = employee.append("custom_benefits", {})
								new_earning.salary_component = component_name
								new_earning.amount = 0
								# new_earning.annual_amount = result*12
								employee.save()
				

		





    


	def onload(self):
		if self.employee:
			self.set_onload(
				"earning_and_deduction_entries_does_not_exists",
				self.earning_and_deduction_entries_does_not_exists(),
			)

	def validate(self):
		self.validate_dates()
		self.validate_income_tax_slab()
		self.set_payroll_payable_account()

		if self.earning_and_deduction_entries_does_not_exists():
			if not self.taxable_earnings_till_date and not self.tax_deducted_till_date:
				frappe.msgprint(
					_(
						"""
						Not found any salary slip record(s) for the employee {0}. <br><br>
						Please specify {1} and {2} (if any),
						for the correct tax calculation in future salary slips.
						"""
					).format(
						self.employee,
						"<b>" + _("Taxable Earnings Till Date") + "</b>",
						"<b>" + _("Tax Deducted Till Date") + "</b>",
					),
					indicator="orange",
					title=_("Warning"),
				)

		if not self.get("payroll_cost_centers"):
			self.set_payroll_cost_centers()

		self.validate_cost_center_distribution()

	def validate_dates(self):
		joining_date, relieving_date = frappe.db.get_value(
			"Employee", self.employee, ["date_of_joining", "relieving_date"]
		)

		if self.from_date:
			if frappe.db.exists(
				"Salary Structure Assignment",
				{"employee": self.employee, "from_date": self.from_date, "docstatus": 1},
			):
				frappe.throw(_("Salary Structure Assignment for Employee already exists"), DuplicateAssignment)

			if joining_date and getdate(self.from_date) < joining_date:
				frappe.throw(
					_("From Date {0} cannot be before employee's joining Date {1}").format(
						self.from_date, joining_date
					)
				)

			# flag - old_employee is for migrating the old employees data via patch
			if relieving_date and getdate(self.from_date) > relieving_date and not self.flags.old_employee:
				frappe.throw(
					_("From Date {0} cannot be after employee's relieving Date {1}").format(
						self.from_date, relieving_date
					)
				)

	def validate_income_tax_slab(self):
		if not self.income_tax_slab:
			return

		income_tax_slab_currency = frappe.db.get_value(
			"Income Tax Slab", self.income_tax_slab, "currency"
		)
		if self.currency != income_tax_slab_currency:
			frappe.throw(
				_("Currency of selected Income Tax Slab should be {0} instead of {1}").format(
					self.currency, income_tax_slab_currency
				)
			)

	def set_payroll_payable_account(self):
		if not self.payroll_payable_account:
			payroll_payable_account = frappe.db.get_value(
				"Company", self.company, "default_payroll_payable_account"
			)
			if not payroll_payable_account:
				payroll_payable_account = frappe.db.get_value(
					"Account",
					{
						"account_name": _("Payroll Payable"),
						"company": self.company,
						"account_currency": frappe.db.get_value("Company", self.company, "default_currency"),
						"is_group": 0,
					},
				)
			self.payroll_payable_account = payroll_payable_account

	def on_cancel(self):
		emp = self.employee
		cur_assignment = self.name

		employee = frappe.get_doc("Employee", emp)
		emp_assignment = employee.custom_salary_structure_assignment

		if cur_assignment == emp_assignment:
			employee.custom_salary_structure_assignment = ""
			employee.custom_salary_structure = ""
			employee.get("custom_earnings").clear()
			employee.get("custom_deductions").clear()
			employee.get("custom_benefits").clear()
			employee.save()
    

	@frappe.whitelist()
	def set_payroll_cost_centers(self):
		self.payroll_cost_centers = []
		default_payroll_cost_center = self.get_payroll_cost_center()
		if default_payroll_cost_center:
			self.append(
				"payroll_cost_centers", {"cost_center": default_payroll_cost_center, "percentage": 100}
			)

	def get_payroll_cost_center(self):
		payroll_cost_center = frappe.db.get_value("Employee", self.employee, "payroll_cost_center")
		if not payroll_cost_center and self.department:
			payroll_cost_center = frappe.db.get_value("Department", self.department, "payroll_cost_center")

		return payroll_cost_center

	def validate_cost_center_distribution(self):
		if self.get("payroll_cost_centers"):
			total_percentage = sum([flt(d.percentage) for d in self.get("payroll_cost_centers", [])])
			if total_percentage != 100:
				frappe.throw(_("Total percentage against cost centers should be 100"))

	@frappe.whitelist()
	def earning_and_deduction_entries_does_not_exists(self):
		if self.enabled_settings_to_specify_earnings_and_deductions_till_date():
			if not self.joined_in_the_same_month() and not self.have_salary_slips():
				return True
			else:
				if self.docstatus in [1, 2] and (
					self.taxable_earnings_till_date or self.tax_deducted_till_date
				):
					return True
				return False
		else:
			return False

	def enabled_settings_to_specify_earnings_and_deductions_till_date(self):
		"""returns True if settings are enabled to specify earnings and deductions till date else False"""

		if frappe.db.get_single_value(
			"Payroll Settings", "define_opening_balance_for_earning_and_deductions"
		):
			return True
		return False

	def have_salary_slips(self):
		"""returns True if salary structure assignment has salary slips else False"""

		salary_slip = frappe.db.get_value(
			"Salary Slip", filters={"employee": self.employee, "docstatus": 1}
		)

		if salary_slip:
			return True

		return False

	def joined_in_the_same_month(self):
		"""returns True if employee joined in same month as salary structure assignment from date else False"""

		date_of_joining = frappe.db.get_value("Employee", self.employee, "date_of_joining")
		from_date = getdate(self.from_date)

		if not self.from_date or not date_of_joining:
			return False

		elif date_of_joining.month == from_date.month:
			return True

		else:
			return False



def get_assigned_salary_structure(employee, on_date):
	if not employee or not on_date:
		return None
	salary_structure = frappe.db.sql(
		"""
		select salary_structure from `tabSalary Structure Assignment`
		where employee=%(employee)s
		and docstatus = 1
		and %(on_date)s >= from_date order by from_date desc limit 1""",
		{
			"employee": employee,
			"on_date": on_date,
		},
	)
	return salary_structure[0][0] if salary_structure else None


@frappe.whitelist()
def get_employee_currency(employee):
	employee_currency = frappe.db.get_value(
		"Salary Structure Assignment", {"employee": employee}, "currency"
	)
	if not employee_currency:
		frappe.throw(
			_("There is no Salary Structure assigned to {0}. First assign a Salary Stucture.").format(
				employee
			)
		)
	return employee_currency