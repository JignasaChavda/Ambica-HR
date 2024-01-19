var content_wrapper;


function printDiv() {
   var printWindow = window.open('', '_blank');
   var contentToPrint = $('<div>').html($('#page-content').html());


   var contentWrapper = $('<div>').html(content_wrapper.html());
   contentToPrint.append(contentWrapper);


   contentToPrint.find('*').css('color', 'black');


   contentWrapper.css({
       'border-collapse': 'collapse'
   });


   printWindow.document.open();
   printWindow.document.write('<html><head><title>Print</title><style type="text/css">/</style></head><body>');
   printWindow.document.write(contentToPrint.html());
   printWindow.document.write('</body></html>');
   printWindow.document.close();


   printWindow.onload = function () {
       printWindow.print();
       printWindow.onafterprint = function () {
           printWindow.close();
       };
   };
}


frappe.pages['lwf-details'].on_page_load = function(wrapper) {
   var page = frappe.ui.make_app_page({
       parent: wrapper,
       // title: 'LWF Details',
       single_column: true
   });


   // Create a separate div to hold the date fields and data
   content_wrapper = $('<div>').appendTo(page.body);


   // Dynamic Date Fields
   let fields = [
       {
           label: 'From Date',
           fieldtype: 'Date',
           fieldname: 'from'
       },
       {
           label: 'To Date',
           fieldtype: 'Date',
           fieldname: 'to'
       }
   ];


   let fromDate, toDate;


   fields.forEach(field => {
       let dateField = page.add_field(field);


       // Set default values to the first day of the current month
       if (field.fieldname === 'from') {
           let firstDayOfMonth = new Date(frappe.datetime.get_today());
           firstDayOfMonth.setDate(1);
           let formattedDate = frappe.datetime.str_to_user(firstDayOfMonth).split('-').reverse().join('-');
           dateField.set_value(formattedDate);
       } else if (field.fieldname === 'to') {
           let today = new Date(frappe.datetime.get_today());
           let lastDayOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
           let formattedDate = frappe.datetime.str_to_user(lastDayOfMonth).split('-').reverse().join('-');
           dateField.set_value(formattedDate);
       }


       // Clear existing bindings before adding a new one
       dateField.$input.off('change').on('change', function() {
           var changing_date = dateField.get_value();
           if (field.fieldname === 'from') {
               fromDate = changing_date;
               // console.log('From Date:', fromDate);
           } else if (field.fieldname === 'to') {
               toDate = changing_date;
               // console.log('To Date:', toDate);
           }


           // Call getLWFDetailedData after the dates have been updated
           getLWFDetailedData(fromDate, toDate);
       });
   });


   var print = $('<div class="ml-auto mt-auto mb-auto"><input type="button" class="float-right btn btn-primary" id="btn" value="Print" onclick="printDiv();"></div></div> ');


   $('#btn').on('click', function() {
       printDiv();
   });
   // page.body.append(print);
   $('.page-form').append(print);


   // Initial call to getLWFDetailedData with default dates
   // getLWFDetailedData(fromDate, toDate);


   function getLWFDetailedData(from_date, to_date) {
       frappe.call({
           method: 'ambica_hr.ambica_hr.page.lwf_details.lwf_details.get_lwf_details',
           args: {
               from_date: from_date,
               to_date: to_date
           },
           callback: function(response) {
               if (response.message) {
                   var company_name = response.message[0];
                   var employees = response.message[1];
                   var employeeshare = response.message[2];
                   var employershare = response.message[3];
                   var total = response.message[4];
                   var date = response.message[5];
                   var address = response.message[6]
                   displayAttendanceDetails(company_name, employees, employeeshare, employershare, total, date, address);
                   // console.log(response.message);
               }
           }
       });
   }


   function displayAttendanceDetails(company_name, employees, employeeshare, employershare, total, date, address) {
       // Empty the content_wrapper before appending new data
       content_wrapper.empty();
       $(frappe.render_template('lwf_details', { company_name: company_name, employees: employees, employeeshare: employeeshare, employershare: employershare, total:total, date: date, address: address })).appendTo(content_wrapper);
   }
};






