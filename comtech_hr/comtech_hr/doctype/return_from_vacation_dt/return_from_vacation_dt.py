# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ReturnFromVacationDT(Document):
	pass
# def on_submit(self):
# 	self.create_leave_application()

# def create_leave_application(self):
# 	default_company = frappe.db.get_value("Employee",self.employee_no,"company")
# 	default_leave_without_pay = frappe.db.get_value("Company",default_company,"custom_default_leave_without_pay")
# 	if not default_leave_without_pay:
# 		frappe.throw(_("Please set default leave without pay in company {0}".format(frappe.bold(default_company))))
# 	employee_leave_approver = frappe.db.get_value("Employee",self.employee_no,"leave_approver")
# 	if not employee_leave_approver:
# 		frappe.throw(_("Please set leave approver in employee {0}".format(frappe.bold(self.employee_no))))
# 	print("default_leave_without_pay",default_leave_without_pay)
	
# 	if self.no_of_delay > 0:
# 		leave_application_doc = frappe.new_doc("Leave Application")
# 		leave_application_doc.employee = self.employee_no
# 		leave_application_doc.leave_type = default_leave_without_pay
# 		leave_application_doc.from_date = self.return_date
# 		leave_application_doc.to_date = self.return_to_work_date
# 		leave_application_doc.leave_approver = employee_leave_approver
# 		leave_application_doc.save(ignore_permissions=True)
# 		frappe.msgprint(_("Leave Application is created <b>{0}</b>").format(get_link_to_form("Leave Application",leave_application_doc.name)),alert=True)
