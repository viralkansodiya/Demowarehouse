# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns, data = get_data(filters)
	return columns, data

def get_data(filters):

	cond = ''
	if filters.get('from_date'):
		cond += f" and pr.posting_date >= '{filters.get('from_date')}'"
	if filters.get('to_date'):
		cond += f" and pr.posting_date <= '{filters.get('to_date')}'"
	
	data = frappe.db.sql(f"""
		Select pr.name,
		pr.set_warehouse,
		w.custom_warehouse_description,
		item.custom_sub_family_code,
		item.custom_sub_family_name,
		pri.serial_no,
		pr.custom_order_reference,
		pri.qty,
		pr.posting_date
		From `tabPurchase Receipt` as pr
		Left Join `tabPurchase Receipt Item` as pri ON pri.parent = pr.name
		Left Join `tabItem` as item ON pri.item_code = item.name
		Left Join `tabWarehouse` as w ON w.name = pr.set_warehouse
		Where pr.docstatus = 1 and pr.is_return = 1 {cond}
	""", as_dict= 1)

	columns =[
		{
			'fieldname': 'set_warehouse',
			'label': _('WAREHOUSE_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_warehouse_description',
			'label': _('WAREHOUSE_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_sub_family_name',
			'label': _('SUB_FAMILY_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'serial_no',
			'label': _('MSN'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_order_reference',
			'label': _('ORDER_REFERENCE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_order_refer',
			'label': _('AWB / GCN #'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'qty',
			'label': _('QUANTITY'),
			'fieldtype': 'Float',
			'width': 150
		},
		{
			'fieldname': 'posting_date',
			'label': _('DATE_SHIPPED'),
			'fieldtype': 'Date',
			'width': 150
		},

	]
	return columns, data