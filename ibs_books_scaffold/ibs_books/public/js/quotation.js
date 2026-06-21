frappe.ui.form.on("Quotation", {
	refresh(frm) {
		if (frm.doc.docstatus !== 1) return;

		const status = frm.doc.custom_quote_status;

		if (status === "Draft" || !status) {
			frm.add_custom_button("Mark as Sent", () => {
				frappe.call({
					method: "ibs_books.overrides.quotation.mark_as_sent",
					args: { quotation_name: frm.doc.name },
					callback: () => frm.reload_doc(),
				});
			});
		}

		if (status === "Sent") {
			frm.add_custom_button("Mark as Accepted", () => {
				frappe.call({
					method: "ibs_books.overrides.quotation.mark_as_accepted",
					args: { quotation_name: frm.doc.name },
					callback: () => frm.reload_doc(),
				});
			});
			frm.add_custom_button("Mark as Declined", () => {
				frappe.prompt(
					{ fieldname: "reason", label: "Decline Reason", fieldtype: "Small Text" },
					(values) => {
						frappe.call({
							method: "ibs_books.overrides.quotation.mark_as_declined",
							args: { quotation_name: frm.doc.name, reason: values.reason },
							callback: () => frm.reload_doc(),
						});
					},
					"Decline Quotation"
				);
			});
		}

		if (status === "Accepted") {
			frm.add_custom_button("Sales Order", () => {
				frappe.model.open_mapped_doc({
					method: "ibs_books.overrides.quotation.make_sales_order",
					frm: frm,
				});
			}, "Create");
			frm.add_custom_button("Sales Invoice", () => {
				frappe.model.open_mapped_doc({
					method: "ibs_books.overrides.quotation.make_sales_invoice",
					frm: frm,
				});
			}, "Create");
		}
	},
});
