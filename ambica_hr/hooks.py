app_name = "ambica_hr"
app_title = "Ambica HR"
app_publisher = "jignasha"
app_description = "Ambica HR"
app_email = "jignasha@sanskartechnolab.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ambica_hr/css/ambica_hr.css"
# app_include_js = "/assets/ambica_hr/js/ambica_hr.js"

# include js, css files in header of web template
# web_include_css = "/assets/ambica_hr/css/ambica_hr.css"
# web_include_js = "/assets/ambica_hr/js/ambica_hr.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ambica_hr/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ambica_hr/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "ambica_hr.utils.jinja_methods",
#	"filters": "ambica_hr.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ambica_hr.install.before_install"
# after_install = "ambica_hr.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ambica_hr.uninstall.before_uninstall"
# after_uninstall = "ambica_hr.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ambica_hr.utils.before_app_install"
# after_app_install = "ambica_hr.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ambica_hr.utils.before_app_uninstall"
# after_app_uninstall = "ambica_hr.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ambica_hr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Salary Structure Assignment": "ambica_hr.salary_structure_assignment_overrides.SalaryStructureAssignment",
    "Employee Promotion": "ambica_hr.employee_promotion_overrides.EmployeePromotion",
    "Attendance": "ambica_hr.attendance_overrides.Attendance"
}


# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------
scheduler_events = {
    "Update_employee_details": {
       "29 13 * * *": [
          "ambica_hr.employee_promotion_overrides.Update_employee_details"
        ]
    },


#	"all": [
#		"ambica_polymer.tasks.all"
#	],
#	"daily": [
#		"ambica_polymer.tasks.daily"
#	],
#	"hourly": [
#		"ambica_polymer.tasks.hourly"
#	],
#	"weekly": [
#		"ambica_polymer.tasks.weekly"
#	],
#	"monthly": [
#		"ambica_polymer.tasks.monthly"
#	],
}

# Testing
# -------

# before_tests = "ambica_hr.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ambica_hr.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "ambica_hr.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ambica_hr.utils.before_request"]
# after_request = ["ambica_hr.utils.after_request"]

# Job Events
# ----------
# before_job = ["ambica_hr.utils.before_job"]
# after_job = ["ambica_hr.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"ambica_hr.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
#	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt":"Server Script","filters":[
        [
            "module","in",[
               "Ambica HR"
            ],
        ]
    ]},
    {"dt":"Custom Field","filters":[
        [
            "module","in",[
               "Ambica HR"
            ]
        ]
    ]},
    {"dt":"Client Script","filters":[
        [
            "module","in",[
               "Ambica HR"
            ],
        ]
    ]},
    {"dt":"Property Setter","filters":[
        [
            "module","in",[
               "Ambica HR"
            ],
        ]
    ]},
    {"dt":"Custom DocPerm","filters":[
        [
            "role","in",[
               "Ambica HR-User"
            ],
        ]
    ]},
    {"dt":"Role","filters":[
        [
            "name","in",[
               "Ambica HR-User"
            ],
        ]
    ]},
    {"dt":"Module Profile","filters":[
        [
            "name","in",[
               "Ambica HR-Payroll"
            ],
        ]
    ]},
    {"dt":"Workspace","filters":[
        [
            "module","in",[
               "Ambica HR"
            ],
        ]
    ]}
    
]
