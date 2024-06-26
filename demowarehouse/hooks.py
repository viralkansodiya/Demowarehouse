from . import __version__ as app_version

app_name = "demowarehouse"
app_title = "Demowarehouse"
app_publisher = "Viral Patel"
app_description = "Test"
app_email = "viral@gmail.ocm"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/demowarehouse/css/demowarehouse.css"
# app_include_js = "/assets/demowarehouse/js/demowarehouse.js"

# include js, css files in header of web template
# web_include_css = "/assets/demowarehouse/css/demowarehouse.css"
# web_include_js = "/assets/demowarehouse/js/demowarehouse.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "demowarehouse/public/scss/website"
from erpnext.stock.doctype.serial_no import serial_no
from demowarehouse.demowarehouse.serial_no import update_args_for_serial_no, auto_make_serial_nos
serial_no.update_args_for_serial_no = update_args_for_serial_no
serial_no.auto_make_serial_nos = auto_make_serial_nos
# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"Serial No" : "public/js/serial_no.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

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
#	"methods": "demowarehouse.utils.jinja_methods",
#	"filters": "demowarehouse.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "demowarehouse.install.before_install"
# after_install = "demowarehouse.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "demowarehouse.uninstall.before_uninstall"
# after_uninstall = "demowarehouse.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "demowarehouse.utils.before_app_install"
# after_app_install = "demowarehouse.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "demowarehouse.utils.before_app_uninstall"
# after_app_uninstall = "demowarehouse.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "demowarehouse.notifications.get_notification_config"

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

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

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
# doc_events = {
#     "Serial No" : {
#         'after_insert' : "demowarehouse.demowarehouse.serial_no.after_insert"
#     }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"demowarehouse.tasks.all"
#	],
#	"daily": [
#		"demowarehouse.tasks.daily"
#	],
#	"hourly": [
#		"demowarehouse.tasks.hourly"
#	],
#	"weekly": [
#		"demowarehouse.tasks.weekly"
#	],
#	"monthly": [
#		"demowarehouse.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "demowarehouse.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "demowarehouse.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "demowarehouse.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["demowarehouse.utils.before_request"]
# after_request = ["demowarehouse.utils.after_request"]

# Job Events
# ----------
# before_job = ["demowarehouse.utils.before_job"]
# after_job = ["demowarehouse.utils.after_job"]

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
#	"demowarehouse.auth.validate"
# ]
