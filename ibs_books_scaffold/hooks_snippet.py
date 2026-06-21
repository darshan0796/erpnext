# Add/merge these into apps/ibs_books/ibs_books/hooks.py

fixtures = ["Custom Field"]

override_doctype_class = {
	"Quotation": "ibs_books.overrides.quotation.CustomQuotation",
}

doctype_js = {
	"Quotation": "public/js/quotation.js",
}
