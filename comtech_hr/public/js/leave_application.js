frappe.ui.form.on("Leave Application", {
    custom_is_vacation_leave: function (frm) {
        frm.set_query('leave_type', function () {
            if (frm.doc.custom_is_vacation_leave == 1) {
                return {
                    filters: {
                        custom_is_vacation_leave_type: 1
                    }
                }
            }
            else if (frm.doc.custom_is_vacation_leave == 0) {
                return
            }
        })
    },

    refresh: function (frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status == "Approved") {
            frm.add_custom_button("Create Vacation Calculation", function () {
                frappe.model.open_mapped_doc({
                    method: 'comtech_hr.api.make_vacation_calculation',
                    frm: cur_frm
                })
            })


            frm.add_custom_button("Create Return From Vacation", function () {
                frappe.model.open_mapped_doc({
                    method: 'comtech_hr.api.make_return_from_vacation',
                    frm: cur_frm
                })
            })
        }
    }
});