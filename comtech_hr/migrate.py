import frappe
from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_migrate():
    custom_fields = {
        "Leave Type" : [
            dict(
                fieldname = "custom_is_vacation_leave_type",
                fieldtype = "Check",
                label =  _("Is Vacation Leave Type?"),
                insert_after = "is_lwp",
                is_custom_field = 1,
                is_system_generated = 0,
            )
        ],

        "Leave Application" : [
            dict(
                fieldname = "custom_is_vacation_leave",
                fieldtype = "Check",
                label =  _("Is Vacation Leave?"),
                insert_after = "column_break_4",
                is_custom_field = 1,
                is_system_generated = 0,
            )
        ],

        "Salary Detail" : [
            dict(
                fieldname = "custom_include_in_vacation_leave_type_calculation",
                fieldtype = "Check",
                label =  _("Include In Vacation Leave Type Calculation?"),
                insert_after = "deduct_full_tax_on_selected_payroll_date",
                is_custom_field = 1,
                is_system_generated = 0,
            )
        ], 

        "Employee" : [
            dict(
                fieldname = "custom_ticket_amount",
                fieldtype = "Currency",
                label =  _("Ticket Amount"),
                insert_after = "custom_number_of_months_of_service",
                is_custom_field = 1,
                is_system_generated = 0,
                description = _("This Is Yearly Amount")
            )
        ], 

        "Company" : [
            dict(
                fieldname = "custom_default_loan_account_for_employee",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Loan Account For Employee"),
                insert_after = "default_payroll_payable_account",
                is_custom_field = 1,
                is_system_generated = 0,
            ),
            dict(
                fieldname = "custom_default_petty_cash_account",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Petty Cash Account"),
                insert_after = "custom_default_loan_account_for_employee",
                is_custom_field = 1,
                is_system_generated = 0,
            ),
            dict(
                fieldname = "custom_default_ticket_expense_account",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Ticket Expense Account"),
                insert_after = "custom_default_petty_cash_account",
                is_custom_field = 1,
                is_system_generated = 0,
            ),
            dict(
                fieldname = "custom_default_due_amount_for_ticket",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Due Amount for Ticket"),
                insert_after = "default_employee_advance_account",
                is_custom_field = 1,
                is_system_generated = 0,
            ),
            dict(
                fieldname = "custom_default_extra_payment_expense_account",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Extra Payment Expense Account"),
                insert_after = "custom_default_due_amount_for_ticket",
                is_custom_field = 1,
                is_system_generated = 0,
            ),
            dict(
                fieldname = "custom_default_exttra_due_amount_account",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Extra Due Amount Account"),
                insert_after = "custom_default_ticket_expense_account",
                is_custom_field = 1,
                is_system_generated = 0,
            ),
            dict(
                fieldname = "custom_default_vacation_due_employee_account",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Vacation Due Employee Account"),
                insert_after = "custom_default_exttra_due_amount_account",
                is_custom_field = 1,
                is_system_generated = 0,
            ),
            dict(
                fieldname = "custom_default_vacation_expense_account",
                fieldtype = "Link",
                options = "Account",
                label =  _("Default Vacation Expense Account"),
                insert_after = "custom_default_vacation_due_employee_account",
                is_custom_field = 1,
                is_system_generated = 0,
            )
        ],

        "Journal Entry" : [
            dict(
                fieldname = "custom_vacation_calculation_reference",
                fieldtype = "Link",
                label = _("Vacation Calculation Reference"),
                options = "Vacation Calculation",
                is_custom_field = 1,
                is_system_generated = 0,
                insert_after = "custom_pc_clearance_reference"
            )
        ],

        "Return From Vacation DT": [
            dict(
                fieldname = "custom_leave_application_reference",
                fieldtype = "Link",
                label = _("Leave Application Reference"),
                options = "Leave Application",
                is_custom_field = 1,
                is_system_generated = 0,
                insert_after = "no_of_delay"
            )
        ]
    }

    print("Creating Custom Fields For Comtech HR App:")
    for dt, fields in custom_fields.items():
        print("*******\n %s: " % dt, [d.get("fieldname") for d in fields])
        create_custom_fields(custom_fields)

def update_dashboard_link_for_core_doctype(doctype,link_doctype,link_fieldname,group=None):
    print(doctype,link_doctype,link_fieldname,group)
    try:
        d = frappe.get_doc("Customize Form")
        if doctype:
            d.doc_type = doctype
        d.run_method("fetch_to_customize")
        for link in d.get('links'):
            if link.link_doctype==link_doctype and link.link_fieldname==link_fieldname:
                # found so just return
                return
        d.append('links', dict(link_doctype=link_doctype, link_fieldname=link_fieldname,table_fieldname=None,group=group))
        d.run_method("save_customization")
        frappe.clear_cache()
    except Exception:
        frappe.log_error(frappe.get_traceback())

update_dashboard_link_for_core_doctype(doctype='Leave Application',link_doctype='Vacation Calculation',link_fieldname='leave_application_reference',group=None)
update_dashboard_link_for_core_doctype(doctype='Leave Application',link_doctype='Return From Vacation DT',link_fieldname='custom_leave_application_reference',group=None)
