import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import rounded, cint, time_diff_in_seconds, time_diff_in_hours, get_time

@frappe.whitelist()
def make_vacation_calculation(source_name, target_doc=None):
    doc = get_mapped_doc(
        "Leave Application",
        source_name,
        {
            "Leave Application" : {
                "doctype" : "Vacation Calculation",
                "field_map" : {
                    "company" : "company",
                    "employee" : "employee_no",
                    "employee_name" : "employee_name",
                    "department" : "department",
                    "name" : "leave_application_reference",
                    "from_date" : "leave_start_date",
                    "to_date" : "leave_end_date"
                }
            }
        },
        target_doc
    )
    return doc


@frappe.whitelist()
def make_return_from_vacation(source_name, target_doc=None):
    def set_missing_value(source, target):
        target.designation = frappe.db.get_value("Employee", source.employee, "designation")

    doc = get_mapped_doc(
        "Leave Application",
        source_name,
        {
            "Leave Application" : {
                "doctype" : "Return From Vacation DT",
                "field_map" : {
                    "employee" : "employee_no",
                    "employee_name" : "employee_name",
                    "department" : "department",
                    "from_date" : "leave_date",
                    "to_date" : "return_date",
                    "name" : "leave_application_reference"
                }
            }
        },
        target_doc,
        set_missing_value
    )
    return doc

@frappe.whitelist()
def calculate_actual_working_hours(self,method):
	print('--------------------------------------4'*10)
	print('calculate_extra_working_hours'*10)
	shift = frappe.db.get_value("Employee", self.employee, "default_shift")
	print("Shift: ", shift)
	if shift:
		shift_start_time = frappe.db.get_value("Shift Type",self.shift,"start_time")
		shift_end_time = frappe.db.get_value("Shift Type",self.shift,"end_time")

		expected_working_hours = time_diff_in_hours(shift_end_time, shift_start_time)
		self.custom_expected_working_hours = expected_working_hours

		if self.late_entry == 1:
			late_entry_duration = time_diff_in_seconds(str((self.in_time).time()),str(get_time(str(shift_start_time))))
			self.custom_actual_delay_minutes = cint(rounded(late_entry_duration/60,0))
		
		if self.early_exit == 1:
			early_exit_duration = time_diff_in_seconds(str(get_time(str(shift_end_time))),str((self.out_time).time()))
			self.custom_actual_early_minutes = cint(rounded(early_exit_duration/60,0))