# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _


def execute(filters=None):
	columns, data = [], []

	columns = get_columns(filters)
	data = get_data(filters)

	if not data:
		msgprint(_("No records found"))
		return columns, data
	
	return columns, data

def get_conditions(filters):
	conditions =""

	if filters.get("from_date") and filters.get("to_date"):
		if filters.get("to_date") >= filters.get("from_date"):
			conditions += "DATE(att.attendance_date) between {0} and {1}".format(
        		frappe.db.escape(filters.get("from_date")),
        		frappe.db.escape(filters.get("to_date")))		
		else:
			frappe.throw(_("To Date should be greater then From Date"))	

	if filters.employee:
		conditions += " and att.employee = '{0}'".format(filters.employee)
	
	if filters.department:
		conditions += " and e.department = '{0}'".format(filters.department)
	
	if filters.designation:
		conditions += " and e.designation = '{0}'".format(filters.designation)

	return conditions

def get_columns(filters):
	columns = [
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": _("Employee ID"),
			"options": "Employee",
			"width": 200
		},
		{
			"fieldname": "first_name",
			"fieldtype": "Data",
			"label": _("First Name"),
			"width": 200
		},
		{
			"fieldname": "attendance_date",
			"fieldtype": "Date",
			"label": _("Date"),
			"width": 200
		},
		{
			"fieldname": "attendance_day",
			"fieldtype": "Data",
			"label": _("Day"),
			"width": 200
		},
		{
			"fieldname": "designation",
			"fieldtype": "Link",
			"label": _("Designation"),
			"options": "Designation",
			"width": 200
		},
		{
			"fieldname": "department",
			"label":_("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 200
		},
		{
			"fieldname": "in_time",
			"fieldtype": "Data",
			"label": _("Time In"),
			"width": 200
		},
		{
			"fieldname": "out_time",
			"fieldtype": "Data",
			"label": _("Time Out"),
			"width": 200
		},
		{
			"fieldname": "actual_working_hours",
			"fieldtype": "Data",
			"label": _("Actual Working Hours"),
			"width": 200
		},
		{
			"fieldname": "required_working_hours",
			"fieldtype": "Data",
			"label": _("Required Working Hours"),
			"width": 200
		},
		{
			"fieldname": "late_in",
			"fieldtype": "Data",
			"label": _("Late In (mins)"),
			"width": 200
		},
		{
			"fieldname": "early_out",
			"fieldtype": "Data",
			"label": _("Early Out (mins)"),
			"width": 200
		},
		{
			"fieldname": "attendance",
			"label":_("Attendance"),
			"fieldtype": "Link",
			"options": "Attendance",
			"width": 200
		},
		{
			"fieldname": "attendance_status",
			"label":_("Attendance Status"),
			"fieldtype": "Select",
			"options": "Present\nAbsent\nOn Leave\nOn LWP\nIn Training\nBusiness Trip\nScholarship\nPresent Due To Reconciliation\nHalf Day\nWork From Home",
			"width": 200
		}
	]

	return columns

def get_data(filters):

	conditions = get_conditions(filters)

	data = frappe.db.sql(""" 

SELECT
	att.employee,
	e.first_name,
	e.designation,
	e.department,
	att.name attendance,
	att.attendance_date as attendance_date,
	DAYNAME(att.attendance_date) as attendance_day,
	att.custom_expected_working_hours required_working_hours,
	att.custom_actual_early_minutes early_out,
	att.custom_actual_delay_minutes late_in,
	att.in_time,
	att.out_time,
	att.status attendance_status,
	att.working_hours actual_working_hours
FROM
	`tabAttendance` att
INNER JOIN `tabEmployee` e ON
	att.employee = e.name
WHERE
	att.docstatus < 2
	AND att.status != 'Draft' and {0}
				
 		""".format(conditions),filters, as_dict=1,debug=1)
	return data