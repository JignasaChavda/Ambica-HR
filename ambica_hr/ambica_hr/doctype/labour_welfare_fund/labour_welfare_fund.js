// Copyright (c) 2023, jignasha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Labour Welfare Fund', {
    get_data: function(frm) {
        frm.call({
            method: 'ambica_hr.ambica_hr.doctype.labour_welfare_fund.labour_welfare_fund.get_employee_data',
            args: {
                posting_date: frm.doc.posting_date || null,
                category: frm.doc.category || null,
                department: frm.doc.department || null,
            },
            callback: function(response) {
                if (response.message) {
                 
                    frm.clear_table('lwf_deduction');
                    $.each(response.message, function(i, data) {
                        var row = frappe.model.add_child(cur_frm.doc, 'LWF Deduction', 'lwf_deduction');
						row.employee = data.employee;
                        row.employee_name = data.employee_name;
						row.department = data.department;
                        row.designation = data.designation;
						row.category = data.employment_type;
                        row.component = frm.doc.component
                        row.employee_contribution = frm.doc.employee_contribution
                        row.employer_contribution = frm.doc.employer_contribution
                    });
                    frm.refresh_field('lwf_deduction');
                }

            }
        });
    },
});
