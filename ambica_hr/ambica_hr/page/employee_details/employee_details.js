frappe.pages['employee-details'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Employee Details',
		single_column: true
	});
	frappe.call({
        method: 'ambica.ambica.page.employee_details.employee_details.get_salary_slips',
        args: {},
        callback: function(response) {
            if (response.message) {
                var salary_slips = response.message;
				displaySalarySlips(salary_slips);
            }
        }
    });
	function displaySalarySlips(salary_slips) {
        
        $(frappe.render_template('employee_details', { salary_slips: salary_slips })).appendTo(page.body);
       
    }
}