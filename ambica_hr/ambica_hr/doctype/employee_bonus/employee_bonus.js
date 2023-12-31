// Copyright (c) 2023, jignasha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Bonus', {
	get_data: function(frm) {
        frm.call({
            method: 'ambica_hr.ambica_hr.doctype.employee_bonus.employee_bonus.get_employee_data',
            args: {
                category: frm.doc.category || null,
                department: frm.doc.department || null
            },
            callback: function(response) {
                if (response.message) {
                 
                    frm.clear_table('bonus_details');
                    $.each(response.message, function(i, data) {
                        var row = frappe.model.add_child(cur_frm.doc, 'Bonus Details', 'bonus_details');
						row.employee = data.employee;
                        row.employee_name = data.employee_name;
						row.department = data.department;
                        row.designation = data.designation;
						
                    });
                    frm.refresh_field('bonus_details');
                }

            }
        });
    }
});

