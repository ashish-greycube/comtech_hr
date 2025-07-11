frappe.ui.form.on("Leave Type", {
    custom_is_vacation_leave_type: function(frm) {
        if (frm.doc.custom_is_vacation_leave_type == 1){
            frm.set_value('is_ppl', 1);
            frm.set_value('fraction_of_daily_salary_per_leave', 1);
            frm.set_df_property('applicable_after', 'reqd', 1);
        }
        else if (frm.doc.custom_is_vacation_leave_type == 0){
            frm.set_value('is_ppl', 0);
            frm.set_value('fraction_of_daily_salary_per_leave', 0);
            frm.set_df_property('applicable_after', 'reqd', 0);
        }
    }
});