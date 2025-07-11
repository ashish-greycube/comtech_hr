# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
import erpnext
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from erpnext.accounts.utils import get_balance_on
from frappe.utils import date_diff, today, get_link_to_form
from erpnext.accounts.report.general_ledger.general_ledger import execute 
	
@frappe.whitelist()
def make_journal_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.voucher_type = "Journal Entry"
		target.posting_date = today()
		target.custom_vacation_calculation_reference = source.name

		account = frappe.db.get_value("Company", {'company_name_in_arabic' : source.company}, "default_payroll_payable_account")
		if account == "": frappe.throw("In Company Default Account Is Not Set For {0} ".format(frappe.bold("Payroll Payable Account")))
		row = create_payment_jv_table_data(source, source.company, source.employee_no, debit_account=account, party_type="Employee", party_name=source.employee_no)
		target.append('accounts', row)

		if source.vacation_due_amount > 0:
			account = frappe.db.get_value("Company", {'company_name_in_arabic' : source.company}, "custom_default_vacation_due_employee_account" )
			if account == "": frappe.throw("In Company Default Account Is Not Set For {0} ".format(frappe.bold("Vacation Due Employee Account")))
			row = create_payment_jv_table_data(source, source.company, source.employee_no, debit_account=account, party_type="Employee", party_name=source.employee_no)
			target.append('accounts', row)

		if source.calculate_ticket == "Yes":
			account = frappe.db.get_value("Company", {'company_name_in_arabic' : source.company}, "custom_default_due_amount_for_ticket" )
			if account == "": frappe.throw("In Company Default Account Is Not Set For {0} ".format(frappe.bold("Due Amount For Ticket")))
			row = create_payment_jv_table_data(source, source.company, source.employee_no, debit_account=account, party_type="Employee", party_name=source.employee_no)
			target.append('accounts', row)

		if source.extra_payment > 0:
			account = frappe.db.get_value("Company", {'company_name_in_arabic' : source.company}, "custom_default_exttra_due_amount_account" )
			if account == "": frappe.throw("In Company Default Account Is Not Set For {0} ".format(frappe.bold("Extra Due Amount Account")))
			row = create_payment_jv_table_data(source, source.company, source.employee_no, debit_account=account, party_type="Employee", party_name=source.employee_no)
			target.append('accounts', row)

	doc = get_mapped_doc(
		"Vacation Calculation",
		source_name,
		{
			"Vacation Calculation" : {
				"doctype" : "Journal Entry",
				"field_map" : {
					"company" : "company"
				}
			}
		},
		target_doc,
		set_missing_values
	)
	return doc


def create_payment_jv_table_data(source,  company, employee, credit_account=None, debit_account=None, party_type=None, party_name=None):
	company_default_cost_center = frappe.db.get_value("Company",company,"cost_center")

	filters = frappe._dict({
		"company" : company,
		"party_type" : "Employee",
		"party" : [employee] ,
		"from_date" : frappe.utils.add_months(today(), months=-1),
		"to_date" : today(),
		"account" : [debit_account if debit_account != None else credit_account]
	})

	data = execute(filters)
	if len(data[1]) > 0:
		for d in data[1]:
			if d.get('account') == "'Total'":
				amount = d['balance']

	accounts_row = {
		"account" : debit_account,
		"cost_center":company_default_cost_center,
	}
	if debit_account != None:
		accounts_row.update({
			"debit_in_account_currency":amount
		})
	elif credit_account != None:
		accounts_row.update({
			"credit_in_account_currency":amount
		})

	account_type = frappe.db.get_value("Account", debit_account if debit_account != None else credit_account, "account_type")
	if account_type in ["Receivable", "Payable"]:
		accounts_row["party_type"] = party_type
		accounts_row["party"] = party_name

	return accounts_row


def get_working_start_date(employee):
	doc_type = ""
	doc_name = ""
	latest_return_from_vacation = frappe.db.get_all(
									doctype = "Return From Vacation DT",
									filters = {
										"employee_no" : employee
									},
									fields = ["name"],
									order_by = "date desc",
									limit = 1
								)
	if latest_return_from_vacation != [] or None:
		start_date = frappe.db.get_value("Return From Vacation DT", latest_return_from_vacation[0]['name'], "return_to_work_date")
		doc_type = "Return From Vacation DT"
		doc_name = latest_return_from_vacation[0]['name'] 
	elif latest_return_from_vacation == []:
		start_date = frappe.db.get_value("Employee", employee, "date_of_joining")
		doc_type = "Date of Joining"
		doc_name = employee
	return start_date, doc_type, doc_name

def create_payment_jv_from_vacation_calculation(doc,debit_account,credit_account,amount,jv_date=None,party_type=None,party_name=None):
	if jv_date == None:
		jv_date = today()
	
	payment_jv_doc = frappe.new_doc("Journal Entry")
	payment_jv_doc.voucher_type = "Journal Entry"
	payment_jv_doc.posting_date = jv_date
	payment_jv_doc.custom_vacation_calculation_reference = doc.name
	accounts = []

	company = erpnext.get_default_company()
	company_default_cost_center = frappe.db.get_value("Company",company,"cost_center")

	accounts_row = {
		"account":debit_account,
		"cost_center":company_default_cost_center,
		"debit_in_account_currency":amount,
	}

	account_type = frappe.get_cached_value("Account",debit_account, "account_type")
	if account_type in ["Receivable", "Payable"]:
		accounts_row["party_type"]=party_type
		accounts_row["party"]=party_name

	accounts.append(accounts_row)

	accounts_row_2 = {
		"account":credit_account,
		"cost_center":company_default_cost_center,
		"credit_in_account_currency":amount,
	}

	account_type = frappe.get_cached_value("Account",credit_account, "account_type")
	if account_type in ["Receivable", "Payable"]:
		accounts_row_2["party_type"]=party_type
		accounts_row_2["party"]=party_name
	accounts.append(accounts_row_2)

	payment_jv_doc.set("accounts",accounts)
	payment_jv_doc.run_method('set_missing_values')
	payment_jv_doc.save(ignore_permissions=True)
	payment_jv_doc.submit()

	frappe.msgprint(_("Payment Journal Entry is created from Vacation Calculation {0}").format(get_link_to_form("Journal Entry",payment_jv_doc.name)),alert=1)

class VacationCalculation(Document):
	def on_submit(self):
		self.create_separate_jv_on_submit()

	def validate(self):
		self.get_fields_value()

	def after_insert(self):
		working_start_date, doctype, docname = get_working_start_date(self.employee_no) 
		if doctype == "Return From Vacation DT":
			msg = "Working Start Date Is Taken Based on {0} From {1}".format(doctype, get_link_to_form("Return From Vacation DT", docname))
		elif doctype == "Date of Joining":
			msg = "Working Start Date Is Taken Based on {0} From {1}".format(doctype, get_link_to_form("Employee", docname))

		self.add_comment("Comment",  msg)

	def get_fields_value(self):
		net_total = 0

		date_difference = date_diff(self.leave_end_date, self.leave_start_date) + 1
		self.no_of_days_for_calculation = date_difference or 0

		total_vacation_amount = frappe.db.sql('''
				SELECT SUM(tsd.amount) AS "total_amount"
				FROM `tabSalary Structure` tss 
				INNER JOIN `tabSalary Detail` tsd 
				ON tss.name = tsd.parent
				WHERE tsd.parenttype = "Salary Structure"
				AND tss.company = "{0}"
				AND tsd.custom_include_in_vacation_leave_type_calculation = 1;
			'''.format(self.company),
		as_dict = 1)
		if len(total_vacation_amount) > 0:
			if total_vacation_amount[0]['total_amount'] != None:
				per_day_amount = total_vacation_amount[0]['total_amount'] / 30
				self.per_day_vacation_amount = round(per_day_amount, 2)
				self.vacation_due_amount = round(per_day_amount, 2) * date_difference
				net_total = net_total + self.vacation_due_amount

		if self.calculate_ticket == "Yes":
			emp_yearly_ticket_amount = frappe.db.get_value("Employee", self.employee_no, "custom_ticket_amount")
			days_per_year = frappe.db.get_single_value("Comtech HR Settings", "per_year_days")
			if days_per_year > 0:
				per_day_ticket_amount = emp_yearly_ticket_amount / days_per_year
				working_start_date, doctype, docname = get_working_start_date(self.employee_no) 
				working_end_date = frappe.utils.add_to_date(self.leave_start_date, days=-1)
				total_working_days = date_diff(working_end_date, working_start_date)
				final_ticket_amount = round(per_day_ticket_amount, 2) * total_working_days or 0
				self.ticket_amount = final_ticket_amount or 0
				net_total = net_total + self.ticket_amount

		if self.deduct_petty_cash == "Yes":
			emp_petty_cash_account = frappe.db.get_value("Company", {'company_name_in_arabic' : self.company}, "custom_default_petty_cash_account")
			emp_petty_cash_amount = get_balance_on(emp_petty_cash_account, self.leave_start_date, "Employee", self.employee_no, self.company)
			self.petty_cash_amount = emp_petty_cash_amount or 0
			net_total = net_total + self.petty_cash_amount

		if self.deduct_loan == "Yes":
			emp_loan_account = frappe.db.get_value("Company", {'company_name_in_arabic' : self.company}, "custom_default_loan_account_for_employee")
			emp_loan_amount = get_balance_on(emp_loan_account, self.leave_start_date, "Employee", self.employee_no, self.company)
			self.loan_amount = emp_loan_amount or 0
			net_total = net_total + self.loan_amount

		if self.extra_payment > 0:
			net_total = net_total + self.extra_payment

		self.net_amount_for_vacation = net_total
		


	def create_separate_jv_on_submit(self):
		debit = frappe.db.get_value("Company", self.company, "custom_default_vacation_expense_account")
		credit = frappe.db.get_value("Company", self.company, "custom_default_vacation_due_employee_account")
		if debit and credit != "" or None:
			create_payment_jv_from_vacation_calculation(self,debit,credit,self.vacation_due_amount,None,"Employee",self.employee_no)
		else:
			frappe.throw("In Company Default Account Is Not Set For {0}".format(frappe.bold("Vacation Expense Account" if debit=="" else "Vacation Due Employee Account"))) 

		if self.calculate_ticket == "Yes":
			debit = frappe.db.get_value("Company", self.company, "custom_default_ticket_expense_account")
			credit = frappe.db.get_value("Company", self.company, "custom_default_due_amount_for_ticket")
			if debit and credit != "" or None:
				create_payment_jv_from_vacation_calculation(self,debit,credit,self.ticket_amount,None,"Employee",self.employee_no)
			else:
				frappe.throw("In Company Default Account Is Not Set For {0}".format(frappe.bold("Ticket Expense Account" if debit == "" else "Due Amount For Ticket")))

		if self.extra_payment > 0:
			debit = frappe.db.get_value("Company", self.company, "custom_default_extra_payment_expense_account")
			credit = frappe.db.get_value("Company", self.company, "custom_default_exttra_due_amount_account")
			if debit and credit != "" or None:
				create_payment_jv_from_vacation_calculation(self,debit,credit,self.extra_payment,None,"Employee",self.employee_no)
			else:
				frappe.throw("In Company Default Account Is Not Set For {0}".format(frappe.bold("Extra Payment Expense" if debit=="" else "Extra Due Amount Account")))

		if self.deduct_loan == "Yes":
			debit = frappe.db.get_value("Company", self.company, "custom_default_vacation_due_employee_account")
			credit = frappe.db.get_value("Company", self.company, "custom_default_loan_account_for_employee")
			if debit and credit != "" or None:
				create_payment_jv_from_vacation_calculation(self,debit,credit,self.loan_amount,None,"Employee",self.employee_no)
			else:
				frappe.throw("In Company Default Account Is Not Set For {0}".format(frappe.bold("Vacation Due Employee Account" if debit=="" else "Loan Account For Employee")))

		if self.deduct_petty_cash == "Yes":
			debit = frappe.db.get_value("Company", self.company, "custom_default_vacation_due_employee_account")
			credit = frappe.db.get_value("Company", self.company, "custom_default_petty_cash_account")
			if debit and credit != "" or None:
				create_payment_jv_from_vacation_calculation(self,debit,credit,self.petty_cash_amount,None,"Employee",self.employee_no)
			else:
				frappe.throw("In Company Default Account Is Not Set For {0}".format(frappe.bold("Vacation Due Employee Account" if debit=="" else "Petty Cash Account")))