// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vacation Calculation', {
	refresh: function(frm) {
		frm.set_value("no_of_leave_days", frappe.datetime.get_day_diff( frm.doc.leave_end_date , frm.doc.leave_start_date) + 1)

		if (frm.doc.docstatus == 1){
			frm.add_custom_button("Create Payment JV", function(frm) {
				frappe.model.open_mapped_doc({
					method : "comtech_hr.comtech_hr.doctype.vacation_calculation.vacation_calculation.make_journal_entry",
					frm : cur_frm
				})
			});
		}
	}
});