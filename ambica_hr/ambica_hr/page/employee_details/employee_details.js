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
   var rule1 = $('#rule1').text();
   var rule2 = $('#rule2').text();
   var rule3 = $('#rule3').text();
   var rule4 = $('#rule4').text();
   var rule5 = $('#rule5').text();
   var pf = $('#pf').text();
   var esi = $('#esi').text();
   var date = $('#date').text();
   var reportName = $('#reportname').text();
   var selectedMonth = $('#month').val();
   var month = monthNames[selectedMonth - 1];
   var year = $('#year').val();
   var note1 = $('#note1').text();
   var note2 = $('#note2').text();




   var headerContent = $('<div>').html('<div style="display: flex; justify-content: space-between; margin:10px 0px;"><div><h2 style="margin:0px 0px;">'
   + companyName + '</h2><p style="font-size: 10px; margin:5px 0px;"><b>' + address + '</b></p></div><div><p style="font-size: 10px; margin:0px 0px;">' + rule1 +
   '</p><p style="font-size: 10px; margin:0px 0px;">' + rule2 + '</p><p style="font-size: 10px; margin:0px 0px;">' + rule3 +
   '</p><p style="font-size: 10px; margin:0px 0px;">' + rule4 + '</p><p style="font-size: 10px; margin:0px 0px;">' + rule5 +
   '</p></div></div><hr/><div style="display: flex; justify-content: space-between;"><p style="font-size: 10px; margin:0px 0px;"><b>' + pf +
   '</b></p><p style="font-size: 10px; margin:0px 0px;"><b>' + month + " " + year +
   '</b></p></div><div style="display: flex; justify-content: space-between;"><p style="font-size: 10px; margin:5px 0px;"><b>' + esi +
   '</b></p><h4 style="margin:5px 0px;">' +
   reportName + '</h4><p style="font-size: 10px; margin:5px 80px 5px 0px;"><b>' + date + '</b></p></div>');


   var footerContent = $('<div>').html('<div style="position: absolute; bottom: 0px; width: 100%;"><p style="font-size: 10px; margin:0px 0px;"><b>'
   + note1 + '</b></p><p style="font-size: 10px; margin:0px 0px;"><b>'
   + note2 + '</b></p></div>');


   // contentToPrint.prepend(headerContent);
   contentToPrint.append(footerContent);


   var contentWrapper = $('<div>').html(content_wrapper.html());
   contentToPrint.append(contentWrapper);


   contentToPrint.find('*').css('color', 'black');


   contentWrapper.css({
       'border-collapse': 'collapse',
       'margin-bottom': '100px',
       'page-break-after': 'auto'


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


frappe.pages['employee-details'].on_page_load = function(wrapper) {
   var page = frappe.ui.make_app_page({
       parent: wrapper,
       single_column: true
   });


   var print = $('<div class="row col col-sx-9 ml-auto justify-content-end"><input type="button" class="justify-content-end float-right btn btn-primary" id="btn" value="Print" onclick="printDiv();"></div></div> ');


   $('#btn').on('click', function() {
       printDiv();
   });


   // var title = $('\
   // <div class="">\
   //     <div style="display: flex; justify-content: space-between;">\
   //         <div class="">\
   //             <h2 class="bold mb-2" id="companyname">SHRI AMBICA POLYMER PVT.LTD.</h2>\
   //             <p class="mb-0" style="font-size: 10px; color: black;" id="address"><b>503, OPP BHARAT GAS PLANT, VADALA ROAD, HARIYALA, VADALA, KHEDA- 387570</b></p>\
   //         </div>\
   //         <div class="">\
   //             <p class="mb-0" style="font-size: 10px; color: black;" id="rule1">(1) Form under Rule - 6 of Equal Remuneration Rules 1976.</p>\
   //             <p class="mb-0" style="font-size: 10px; color: black;" id="rule2">(2) From under Rule - 21(4),25(2),26(1) and 26(2) of Gujarat Minimum Wages Rules 1961</p>\
   //             <p class="mb-0" style="font-size: 10px; color: black;" id="rule3">(3) From under Rule - 6 of Payment of Wages Gujarat Rules.1963.</p>\
   //             <p class="mb-0" style="font-size: 10px; color: black;" id="rule4">(4) From 17 under Rule - 78 of Contract Labour (Regulation && Abolition) Gujarat,Rules,1972</p>\
   //             <p class="mb-0" style="font-size: 10px; color: black;" id="rule5">(5) From under Rule - 52(2)of Inter State Migrant Workers (Gujarat) Rules 1981</p>\
   //         </div>\
   //     </div>\
   //     <hr style="background-color: black; margin-bottom: 4px;">\
   //     <p class="mb-1" style="font-size: 10px; color:black;" id="pf"><b>PF. No. :-</b></p>\
   //     <div style="display: flex; justify-content: space-between;">\
   //         <p class="mb-0" style="font-size: 10px; color:black;" id="esi"><b>ESI No. :-</b></p>\
   //         <h4 class="text-center bold mb-1" id="reportname">Wages Register</h4>\
   //         <p class="mb-0" style="font-size: 10px; margin-right:150px; color:black;" id="date"><b>Date of Payment :-</b></p>\
   //     </div>\
   // </div >\
   // ');


   var footer = $('\
   <div class="" style="position: absolute; bottom: -40px; width: 100%;">\
   <p class="mb-0" style="font-size: 10px; color: black;" id="note1"><b>Note : BS = Basic, HRA = House Rent Allowance, CONV= Conveyance Allowance.</b></p>\
   <p class="mb-0" style="font-size: 10px; color: black;" id="note2"><b>Note : ATD. INC. = Attendance Incentive, PRD. INC. = Production Incentive, LOY. INC. = Loyalty Incentive, OTH.DED. = Other Deduction.</b></p>\
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
           <label class="my-auto" id="department-label1"><h5 class="my-auto ml-3" id="customer-labels">Department &nbsp;</h5>\</label>\
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
           <label class="my-auto" id="designation-label"><h5 class="my-auto ml-3" id="designation-id">Designation &nbsp;</h5>\</label>\
           </div>\
           \
           <div class="my-auto">\
               <input class="form-control" list="designationid" id="designation" placeholder="Select Designation..">\
               <div id="designationstore"></div>\
               <datalist id="designationid" class=""></datalist>\
               \
           </div>\
       </div>\
       <div class="row ml-auto mr-auto mt-3" id="filterrow2">\
           <div class="from-col my-auto">\
           <label class="my-auto" id="company-label"><h5 class="my-auto ml-3" id="comany-id">Company &nbsp;</h5>\</label>\
           </div>\
           \
           <div class="my-auto">\
               <input class="form-control" list="companyid" id="company" placeholder="Select Company..">\
               <div id="companystore"></div>\
               <datalist id="companyid" class=""></datalist>\
               \
           </div>\
           \
           <div class="from-col my-auto">\
           <label class="my-auto" id="branch-label"><h5 class="my-auto ml-3" id="branch-id">Branch &nbsp;</h5>\</label>\
           </div>\
           \
           <div class="my-auto">\
               <input class="form-control" list="branchid" id="branch" placeholder="Select Branch..">\
               <div id="branchstore"></div>\
               <datalist id="branchid" class=""></datalist>\
               \
           </div>\
           \
           <div class="from-col my-auto">\
               <label class="my-auto">\
                   <h5 class="my-auto ml-3" id="select-status">Status &nbsp;</h5>\
               </label>\
           </div>\
           \
           <div class="">\
               <select class="form-control my-auto" id="status">\
                   <option></option>\
                   <option>Draft</option>\
                   <option>Submitted</option>\
                   <option>Cancelled</option>\
               </select>\
               <div id="selected-status" hidden></div>\
           </div>\
           \
           <div class="from-col my-auto">\
           <label class="my-auto" id="employee-id"><h5 class="my-auto ml-3" id="employee-ids">Employee &nbsp;</h5>\</label>\
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


   page.main.append(filters, print, content_wrapper, footer);


   var today = new Date();
   var currentYear = today.getFullYear();
   var currentMonth = today.getMonth() + 1; // Adding 1 to get the correct month


   // Set the current year and month as the default values
   $('#year').val(currentYear);
   $('#select-month').val(currentMonth);
  
   var defaultCompanyName = "Shri Ambica Polymer Pvt Ltd";
   var uppercasedCompanyName = defaultCompanyName.toUpperCase();
   $('#company').val(defaultCompanyName);
   $('#companyname').text(uppercasedCompanyName);


   fetchCompanyDetails(defaultCompanyName);


   getEmployeeDetailedData(currentMonth, currentYear, null, null, defaultCompanyName, null, null, null);


   $('#month, #year, #department, #designation, #company, #branch, #status, #employee').on('change', function () {


       var month = $('#month').val();


       var year = $('#year').val();


       var department = $('#department').val();


       var designatin = $('#designation').val();


       var company = $('#company').val();


       var branch = $('#branch').val();


       var status = $('#status').val();


       var employee = $('#employee').val();


       getEmployeeDetailedData(month, year, department, designatin, company, branch, status, employee);
   });


   $('#company').on('change', function () {
       var selectedCompany = $(this).val();
       $('#companyname').html('<h2 class="bold mb-2">' + selectedCompany.toUpperCase() + '</h2>');
       fetchCompanyDetails(selectedCompany);
   });
  
   function fetchCompanyDetails(companyName) {
       frappe.call({
           method: 'ambica_hr.ambica_hr.page.employee_details.employee_details.get_branches',
           args: {
               company: companyName
           },
           callback: function(response) {
               if (response.message) {
                   var branches = response.message[0];
                   var pf_no = response.message[1] || "NA";
                   var esi_no = response.message[2] || "NA";
                   var address = response.message[3];
                   populateBranchDropdown(branches);
                   setPfAndEsiNumbers(pf_no, esi_no, address);
               }
           }
       });
   }


   function populateBranchDropdown(branches) {
       var datalist = $('#branchid');
       datalist.empty();  // Clear existing options


       branches.forEach(function(branch) {
           var option = $('<option>').attr('value', branch.name);
           datalist.append(option);
       });
   }


   function setPfAndEsiNumbers(pf_no, esi_no, address) {
      
       $('#pf').html('<p class="mb-1" style="font-size: 10px; color:black;"><b>PF. No. :- ' + pf_no + '</b></p>');
       $('#esi').html('<p class="mb-1" style="font-size: 10px; color:black;"><b>ESI No. :- ' + esi_no + '</b></p>');
       $('#address').html('<p class="mb-0" style="font-size: 10px; color: black;"><b>' + address.toUpperCase() + '</b></p>');
   }


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
           doctype: 'Designation',
           fields: ['name']
       },
       callback: function(response) {
           if (response.message) {
               var designations = response.message;
               var datalist = $('#designationid');
               designations.forEach(function(designation) {
                   var option = $('<option>').attr('value', designation.name);
                   datalist.append(option);
               });
           }
       }
   });


   frappe.call({
       method: 'frappe.client.get_list',
       args: {
           doctype: 'Company',
           fields: ['name']
       },
       callback: function(response) {
           if (response.message) {
               var companynames = response.message;
               var datalist = $('#companyid');
               companynames.forEach(function(company) {
                   var option = $('<option>').attr('value', company.name);
                   datalist.append(option);
               });
              
           }
       }
   });


   // frappe.call({
   //     method: 'frappe.client.get_list',
   //     args: {
   //         doctype: 'Branch',
   //         fields: ['name']
   //     },
   //     callback: function(response) {
   //         if (response.message) {
   //             var branches = response.message;
   //             var datalist = $('#branchid');
   //             branches.forEach(function(branch) {
   //                 var option = $('<option>').attr('value', branch.name);
   //                 datalist.append(option);
   //             });
              
   //         }
   //     }
   // });


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


   // content_wrapper.appendTo(page.body);
   content_wrapper = $('<div>').appendTo(page.body);
   // footer.appendTo(content_wrapper);
   // page.footer.append(footer);


   function getEmployeeDetailedData(month, year, department, designation, company, branch, status, employee) {
       frappe.call({
           method: 'ambica_hr.ambica_hr.page.employee_details.employee_details.get_salary_slips',
           args: {
               month: month,
               year: year,
               department: department,
               designation: designation,
               company: company,
               branch: branch,
               status: status,
               employee: employee
           },
           callback: function(response) {
               if (response.message) {
                   var salary_slips = response.message[0];
                   var company = response.message [1];
                   var pf_number = response.message[2] || "NA";
                   var esi_number = response.message[3] || "NA";
                   var address = response.message[4];
                   var month = response.message[5];
                   var year = response.message[6];
                   // console.log(response.message)
                   displaySalarySlips(salary_slips, company, pf_number, esi_number, address, month, year);
               }
           }
       });
   }


   function displaySalarySlips(salary_slips, company, pf_number, esi_number, address, month, year) {
       content_wrapper.empty();
       $(frappe.render_template('employee_details', { salary_slips: salary_slips, company: company, pf_number: pf_number, esi_number: esi_number,
           address: address, month: month, year: year })).appendTo(content_wrapper);
       // footer.appendTo(content_wrapper);
   }
}
