// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Return From Vacation DT', {
	return_date : function(frm){
		let start_date = frm.doc.return_date;
		let end_date = frm.doc.return_to_work_date;
		let date_diff = get_diff(start_date, end_date);
		frm.set_value("no_of_delay", date_diff)
	},
	return_to_work_date : function(frm){
		let end_date = frm.doc.return_to_work_date;
		let start_date = frm.doc.return_date;
		let date_diff = get_diff(start_date, end_date);
		frm.set_value("no_of_delay", date_diff)
	}
});

function get_diff(start_date,end_date) {
	if(start_date > end_date){
		frappe.throw(__("The date of return cannot be later than the date of delay"));
	}
	if(start_date && end_date){
		let diff = frappe.datetime.get_day_diff(end_date, start_date);
		return diff + 1;
	}
}