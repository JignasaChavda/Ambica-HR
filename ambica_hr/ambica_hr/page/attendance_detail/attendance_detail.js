frappe.pages['attendance-detail'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Attendance Detail',
		single_column: true
	});
	frappe.call({
        method: 'ambica_hr.ambica_hr.page.attendance_detail.attendance_detail.get_attendance_details',
        args: {
            // employee: 'EMPLOYEE_ID'  // Replace with the actual employee ID
        },
        callback: function(response) {
            if (response.message) {
                var attendance_details = response.message;
				displayAttendanceDetails(attendance_details);
				console.log(attendance_details)
            }
        }
    });
	function displayAttendanceDetails(attendance_details) {
        
        $(frappe.render_template('attendance_detail', { attendance_details: attendance_details })).appendTo(page.body);
       
    }
}