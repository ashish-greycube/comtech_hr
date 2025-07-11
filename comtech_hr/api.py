import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc

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
                    "name" : "custom_leave_application_reference"
                }
            }
        },
        target_doc,
        set_missing_value
    )
    return doc