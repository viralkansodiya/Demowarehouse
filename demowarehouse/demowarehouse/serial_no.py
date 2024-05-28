import frappe
import json
from typing import List, Optional, Union

import frappe
from frappe import ValidationError, _
from frappe.model.naming import make_autoname
from frappe.query_builder.functions import Coalesce
from frappe.utils import (
	add_days,
	cint,
	cstr,
	flt,
	get_link_to_form,
	getdate,
	nowdate,
	safe_json_loads,
)
from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos
from erpnext.controllers.stock_controller import StockController
from erpnext.stock.get_item_details import get_reserved_qty_for_so


def update_args_for_serial_no(serial_no_doc, serial_no, args, is_new=False):
	for field in ["item_code", "work_order", "company", "batch_no", "supplier", "location"]:
		if args.get(field):
			serial_no_doc.set(field, args.get(field))
	
	meta = frappe.get_meta('Serial No')
	
	if meta.has_field('length') and meta.has_field('width') and meta.has_field('height'):
		if args.get('item_code'):
			doc = frappe.get_doc("Item", args.get('item_code'))
			serial_no_doc.set('length' , doc.length)
			serial_no_doc.set('width', doc.width)
			serial_no_doc.set('height', doc.height)
	serial_no_doc.set('custom_barcode', args.get('serial_no'))
	serial_no_doc.via_stock_ledger = args.get("via_stock_ledger") or True
	serial_no_doc.warehouse = args.get("warehouse") if args.get("actual_qty", 0) > 0 else None

	if is_new:
		serial_no_doc.serial_no = serial_no

	if (
		serial_no_doc.sales_order
		and args.get("voucher_type") == "Stock Entry"
		and not args.get("actual_qty", 0) > 0
	):
		serial_no_doc.sales_order = None
	
	meta = frappe.get_meta('Serial No')

	serial_no_doc.validate_item()
	serial_no_doc.update_serial_no_reference(serial_no)
	
	if is_new:
		serial_no_doc.db_insert()
		if meta.has_field('length') and meta.has_field('width') and meta.has_field('height'):
			doc = frappe.get_doc("Item", args.get('item_code'))
			serial_no_doc.db_set('length' , doc.length)
			serial_no_doc.db_set('width', doc.width)
			serial_no_doc.db_set('height', doc.height)
	else:
		serial_no_doc.db_update()
		if meta.has_field('length') and meta.has_field('width') and meta.has_field('height'):
			doc = frappe.get_doc("Item", args.get('item_code'))
			serial_no_doc.db_set('length' , doc.length)
			serial_no_doc.db_set('width', doc.width)
			serial_no_doc.db_set('height', doc.height)
	if meta.has_field('length') and meta.has_field('width') and meta.has_field('height'):
		doc = frappe.get_doc("Item", args.get('item_code'))
		serial_no_doc.db_set('length' , doc.length)
		serial_no_doc.db_set('width', doc.width)
		serial_no_doc.db_set('height', doc.height)
	return serial_no_doc


def auto_make_serial_nos(args):
	serial_nos = get_serial_nos(args.get("serial_no"))
	created_numbers = []
	voucher_type = args.get("voucher_type")
	item_code = args.get("item_code")
	for serial_no in serial_nos:
		is_new = False
		if frappe.db.exists("Serial No", serial_no):
			sr = frappe.get_cached_doc("Serial No", serial_no)
		elif args.get("actual_qty", 0) > 0:
			sr = frappe.new_doc("Serial No")
			is_new = True

		sr = update_args_for_serial_no(sr, serial_no, args, is_new=is_new)
		meta = frappe.get_meta('Serial No')
		if meta.has_field('length') and meta.has_field('width') and meta.has_field('height'):
			if sr.item_code:
				doc = frappe.get_doc("Item", sr.item_code)
				frappe.db.set_value("Serial No", sr.name, "length", doc.length)
				frappe.db.set_value("Serial No", sr.name, "width", doc.width)
				frappe.db.set_value("Serial No", sr.name, "height", doc.height)

		if is_new:
			created_numbers.append(sr.name)

	form_links = list(map(lambda d: get_link_to_form("Serial No", d), created_numbers))

	# Setting up tranlated title field for all cases
	singular_title = _("Serial Number Created")
	multiple_title = _("Serial Numbers Created")

	if voucher_type:
		multiple_title = singular_title = _("{0} Created").format(voucher_type)

	if len(form_links) == 1:
		frappe.msgprint(_("Serial No {0} Created").format(form_links[0]), singular_title)
	elif len(form_links) > 0:
		message = _("The following serial numbers were created: <br><br> {0}").format(
			get_items_html(form_links, item_code)
		)
		frappe.msgprint(message, multiple_title)