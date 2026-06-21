import frappe
from frappe.utils import now_datetime
from erpnext.selling.doctype.quotation.quotation import Quotation


class CustomQuotation(Quotation):
	def validate(self):
		super().validate()
		if not self.custom_quote_status:
			self.custom_quote_status = "Draft"


@frappe.whitelist()
def mark_as_sent(quotation_name):
	doc = frappe.get_doc("Quotation", quotation_name)
	doc.custom_quote_status = "Sent"
	doc.custom_sent_on = now_datetime()
	doc.save()
	return doc.custom_quote_status


@frappe.whitelist()
def mark_as_accepted(quotation_name):
	doc = frappe.get_doc("Quotation", quotation_name)
	doc.custom_quote_status = "Accepted"
	doc.custom_accepted_on = now_datetime()
	doc.save()
	return doc.custom_quote_status


@frappe.whitelist()
def mark_as_declined(quotation_name, reason=None):
	doc = frappe.get_doc("Quotation", quotation_name)
	doc.custom_quote_status = "Declined"
	doc.custom_declined_reason = reason
	doc.save()
	return doc.custom_quote_status


def _assert_accepted(source_name):
	status = frappe.db.get_value("Quotation", source_name, "custom_quote_status")
	if status != "Accepted":
		frappe.throw("Quotation must be Accepted before it can be converted.")


@frappe.whitelist()
def make_sales_order(source_name, target_doc=None):
	_assert_accepted(source_name)
	from erpnext.selling.doctype.quotation.quotation import make_sales_order as _make_sales_order
	return _make_sales_order(source_name, target_doc)


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	_assert_accepted(source_name)
	from erpnext.selling.doctype.quotation.quotation import make_sales_invoice as _make_sales_invoice
	return _make_sales_invoice(source_name, target_doc)
