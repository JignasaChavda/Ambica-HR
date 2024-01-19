var content_wrapper;


function printDiv() {
   var printWindow = window.open('', '_blank');
   var contentToPrint = $('<div>').html($('#page-content').html());


   var monthNames = [
       "January", "February", "March", "April",
       "May", "June", "July", "August",
       "September", "October", "November", "December"
   ];


   var companyName = $('#companyname').text();
   var address = $('#address').text();
   var reportName = $('#reportname').text();
   var selectedMonth = $('#month').val();
   var month = monthNames[selectedMonth - 1];
   var year = $('#year').val();




   var headerContent = $('<div>').html('<h2 style="text-align:center;">' + companyName + '</h2><h6 style="text-align:center;">' + address + '</h6><hr/><div style="display: flex; justify-content: space-between;">' +
   '<h3 style="text-align:left;">' + reportName + '</h3>' +
   '<h6 style="text-align:right;">' + month + " " + year + '</h6>' +
   '</div>');


   contentToPrint.prepend(headerContent);


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


frappe.pages['attendance-detail'].on_page_load = function(wrapper) {
   var page = frappe.ui.make_app_page({
       parent: wrapper,
       single_column: true
   });
  
   var print = $('<div class="row col col-sx-9 ml-auto justify-content-end"><input type="button" class="justify-content-end float-right btn btn-primary" id="btn" value="Print" onclick="printDiv();"></div></div> ');


   $('#btn').on('click', function() {
       printDiv();
   });


   var title = $('\
   <div class="">\
   <h2 class="text-center bold" id="companyname" style="margin: 5px 0px 8px 0px">SHRI AMBICA POLYMER PVT.LTD.</h2>\
   <h6 class="text-center" id="address">503, OPP BHARAT GAS PLANT, VADALA ROAD, HARIYALA, VADALA, KHEDA- 387570</h6>\
   <hr class="border-black">\
   <h3 class="bold" id="reportname">Muster Roll</h3>\
   </div >\
   ');


   var filters = $('\
   <div class="form-group row main-row">\
       <div class="row ml-auto mr-auto justify-content-center align-items-center d-flex">\
           \
           <div class="from-col my-auto">\
               <label class="my-auto">\
                   <h5 class="my-auto ml-3" id="select-month">Month &nbsp;</h5>\
               </label>\
           </div>\
           \
           <div class="">\
               <select class="form-control my-auto" id="month">\
                   <option value="1">January</option>\
                   <option value="2">February</option>\
                   <option value="3">March</option>\
                   <option value="4">April</option>\
                   <option value="5">May</option>\
                   <option value="6">June</option>\
                   <option value="7">July</option>\
                   <option value="8">August</option>\
                   <option value="9">September</option>\
                   <option value="10">October</option>\
                   <option value="11">November </option>\
                   <option value="12">December</option>\
               </select>\
               <div id="selected-month" hidden></div>\
           </div>\
           \
           <div class="from-col my-auto">\
               <label class="my-auto">\
                   <h5 class="my-auto ml-3" id="select-year">Year &nbsp;</h5>\
               </label>\
           </div>\
           \
           <div class="">\
               <input type="number" class="my-auto form-control" id="year">\
               <div id="current-year" hidden></div>\
           </div>\
           \
           <div class="from-col my-auto">\
           <label class="my-auto" id="department-label1"><h5 class="my-auto ml-3"  id="customer-labels">Department &nbsp;</h5>\</label>\
           </div>\
           \
           <div class="my-auto">\
               <input class="form-control" list="departmentid" id="department" placeholder="Select Department..">\
               <div id="departmentstore"></div>\
               <datalist id="departmentid" class=""></datalist>\
               \
           </div>\
           \
           <div class="from-col my-auto">\
           <label class="my-auto" id="employee-id"><h5 class="my-auto ml-3"  id="employee-ids">Employee &nbsp;</h5>\</label>\
           </div>\
           \
           <div class="my-auto">\
               <input class="form-control" list="employeeid" id="employee" placeholder="Select Employee..">\
               <div id="employeestore"></div>\
               <datalist id="employeeid" class=""></datalist>\
               \
           </div>\
           \
       </div>\
       \
   </div>\
   ');


   page.main.append(filters, print, title);


   // var today = new Date();
   // var firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
   // var lastDayOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);


   // var formattedFirstDay = formatDate(firstDayOfMonth);
   // var formattedLastDay = formatDate(lastDayOfMonth);


   var today = new Date();
   var currentYear = today.getFullYear();
   var currentMonth = today.getMonth() + 1; // Adding 1 to get the correct month


   // Set the current year and month as the default values
   $('#year').val(currentYear);
   $('#select-month').val(currentMonth);


   getAttendanceDetailedData(currentMonth, currentYear, null, null);


   // $('#start-date').val(formattedFirstDay);
   // $('#end-date').val(formattedLastDay);


   $(' #month, #year, #department, #employee').on('change', function () {
       // var startDate = $('#start-date').val();
       // var parts = startDate.split("-");
       // var formattedDate = parts[2] + "-" + parts[1] + "-" + parts[0];
       // $("#fromdate").text(formattedDate);


       // var endDate = $('#end-date').val();
       // var parts = endDate.split("-");
       // var formattedDate = parts[2] + "-" + parts[1] + "-" + parts[0];
       // $("#from_dates").text(formattedDate);


       var month = $('#month').val();


       var year = $('#year').val();


       var department = $('#department').val();


       var employee = $('#employee').val();


       getAttendanceDetailedData(month, year, department, employee);
   });


   frappe.call({
       method: 'frappe.client.get_list',
       args: {
           doctype: 'Department',
           fields: ['name']
       },
       callback: function(response) {
           if (response.message) {
               var departments = response.message;
               var datalist = $('#departmentid');
               departments.forEach(function(department) {
                   var option = $('<option>').attr('value', department.name);
                   datalist.append(option);
               });
           }
       }
   });


   frappe.call({
       method: 'frappe.client.get_list',
       args: {
           doctype: 'Employee',
           fields: ['employee']
       },
       callback: function(response) {
           if (response.message) {
               var employees = response.message;
               var datalist = $('#employeeid');
               employees.forEach(function(employee) {
                   var option = $('<option>').attr('value', employee.employee);
                   datalist.append(option);
               });
           }
       }
   });


   content_wrapper = $('<div>').appendTo(page.body);


   function getAttendanceDetailedData(month, year, department, employee) {
       frappe.call({
           method: 'ambica_hr.ambica_hr.page.attendance_detail.attendance_detail.get_attendance_details',
           args: {
               // from_date: fromdate,
               // to_date: todate,
               month: month,
               year: year,
               department: department,
               employee: employee
           },
           callback: function(response) {
               if (response.message) {
                   var attendance_details = response.message;
                   displayAttendanceDetails(attendance_details);
                   console.log(response.message)
               }
           }
       });
   }


   function displayAttendanceDetails(attendance_details) {
       content_wrapper.empty();
       $(frappe.render_template('attendance_detail', { attendance_details: attendance_details })).appendTo(content_wrapper);
     
   }
}
   // function formatDate(date) {
   //     var day = date.getDate();
   //     var month = date.getMonth() + 1;
   //     var year = date.getFullYear();
  
   //     day = day < 10 ? '0' + day : day;
   //     month = month < 10 ? '0' + month : month;
  
   //     return year + '-' + month + '-' + day;
   // }
 






// \
// <div class="from-col my-auto">\
//     <label class="my-auto">\
//         <h5 class="my-auto ml-3" id="from-date">From Date &nbsp;</h5>\
//     </label>\
// </div>\
// \
// <div class="">\
//     <input type="date" class="my-auto form-control" id="start-date">\
//     <div id="fromdate" hidden></div>\
// </div>\
// \
// <div class="from-col my-auto">\
//     <label class="my-auto">\
//         <h5 class="my-auto ml-3" id="to-date">To Date &nbsp;</h5>\
//     </label>\
// </div>\
// \
// <div class="">\
//     <input type="date" class="form-control my-auto " id="end-date">\
//     <div id="from_dates" hidden></div>\
// </div>\


//     // let fields = [
//     //     {
   //         label: 'From Date',
   //         fieldtype: 'Date',
   //         fieldname: 'from'
   //     },
   //     {
   //         label: 'To Date',
   //         fieldtype: 'Date',
   //         fieldname: 'to'
   //     },
   //     {
   //         label: 'Department',
   //         fieldtype: 'Link',
   //         fieldname: 'department',
   //         options: 'Department'
   //     },
   //     {
   //         label: 'Employee',
   //         fieldtype: 'Link',
   //         fieldname: 'employee',
   //         options: 'Employee'
   //     }
   // ];


   // let fromDate, toDate, department, employee;


   // fields.forEach(field => {
   //     let dateField = page.add_field(field);


   //     if (field.fieldname === 'from') {
   //         let firstDayOfMonth = new Date(frappe.datetime.get_today());
   //         firstDayOfMonth.setDate(1);
   //         let formattedDate = frappe.datetime.str_to_user(firstDayOfMonth).split('-').reverse().join('-');
   //         dateField.set_value(formattedDate);
   //     }
   //     else if (field.fieldname === 'to') {
   //         let today = new Date(frappe.datetime.get_today());
   //         let lastDayOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
   //         let formattedDate = frappe.datetime.str_to_user(lastDayOfMonth).split('-').reverse().join('-');
   //         dateField.set_value(formattedDate);
   //     }
       // else if (field.fieldname === 'department') {
       //     department = dateField.field_value;
       // }
       // else if (field.fieldname === 'employee') {
       //     employee = "";
       // }


       // dateField.$input.css({
       //     'margin': '20px', 
       //     'padding': '5px'
       // });
      
   //     dateField.$input.off('change').on('change', function() {


   //         var field_value = dateField.get_value();


   //         if (field.fieldname === 'from') {
   //             fromDate = field_value;
   //             let toField = page.fields_dict['to'];
   //             let toDate = new Date(new Date(field_value).getFullYear(), new Date(field_value).getMonth() + 1, 0);
   //             let formattedToDate = frappe.datetime.str_to_user(toDate).split('-').reverse().join('-');
   //             toField.set_value(formattedToDate);
   //         }
   //         else if (field.fieldname === 'to') {
   //             toDate = field_value;
   //         } else if (field.fieldname === 'department') {
   //             department = field_value;
   //         } else if (field.fieldname === 'employee') {
   //             employee = field_value;
   //         }
          
   //         getAttendanceDetailedData(fromDate, toDate, department, employee);
   //     });
   // });


   // getAttendanceDetailedData(fromDate, toDate, department, employee);
  


  








