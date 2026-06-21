# ibs_books scaffold — Phase 3 (Sales Quotes)

Apply these on the VM, inside `docker exec -it frappe_docker-backend-1 bash`:

```bash
cd /home/frappe/frappe-bench/apps/ibs_books
# copy this scaffold's ibs_books/ subfolder contents into the app's ibs_books/ package,
# merging with what bench new-app generated:
cp -r /path/to/ibs_books_scaffold/ibs_books/fixtures ibs_books/
cp -r /path/to/ibs_books_scaffold/ibs_books/overrides ibs_books/
mkdir -p ibs_books/public/js
cp /path/to/ibs_books_scaffold/ibs_books/public/js/quotation.js ibs_books/public/js/

# then manually edit ibs_books/hooks.py and merge in the contents of hooks_snippet.py
```

Then:

```bash
cd /home/frappe/frappe-bench
bench --site frontend migrate
bench build --app ibs_books
bench restart
```

Verify:

```bash
bench --site frontend console
>>> frappe.get_meta("Quotation").get_field("custom_quote_status")
```

Test in the UI: open/create a Quotation, save as Draft, submit it, confirm "Mark as Sent" button appears, walk through Sent -> Accepted -> Create Sales Order, and Sent -> Declined with reason.
