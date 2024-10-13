// Copyright (c) 2024, Amrinder Singh and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Assignment", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Assignment", {
    user: function(frm) {  // Replace 'user_field' with the actual field name for user selection
        const user = frm.doc.user;

        if (user) {
            frappe.db.get_value("Student", {"user": user}, "name", function(value) {
                if (value && value.name) {
                    frm.set_value("student", value.name);  // Replace 'student' with the actual field name for the student
                    console.log("Linked Student Name:", value.name);
                } else {
                    console.log("No student found for this user.");
                }
            });
        } else {
            frm.set_value("student", ""); // Clear the student field if no user is selected
        }
    }
});
frappe.ui.form.on("Assignment", "check_plagiarism_status",
    function(frm) {
        const user = frm.doc.user;
        frappe.call({
            method: "drillbit.drillbit.doctype.assignment.assignment.hello",
            args: {
            assignment: frm.doc
            },
            callback: function(response) {
            console.log(response.message);
            }
        });
    });