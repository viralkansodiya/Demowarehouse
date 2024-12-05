# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe


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
	if filters.get("owner_code"):
		cond += f" and pr.custom_owner_code = '{filters.get('owner_code')}'"

	data = frappe.db.sql(f"""
			Select pr.name,
			pri.warehouse,
			item.custom_sub_family_name,
			pri.serial_no,
			pr.custom_owner_code,
			pr.customer_batch,
			pri.qty,
			w.custom_warehouse_description,
			pr.posting_date,
			pri.custom_category
			From `tabPurchase Receipt` as pr
			Left Join `tabPurchase Receipt Item` as pri on pri.parent = pr.name
			Left Join `tabWarehouse` as w ON w.name = pri.warehouse
			Left join `tabItem` as item On item.name = pri.item_code
			Where pr.docstatus = 1 and pri.custom_preset_workflow_code= 'INS' and pr.is_return = 0 {cond}
	""", as_dict=1)

	columns = [
		{
			"fieldname":"warehouse",
			"label":"WAREHOUSE_CODE",
			"fieldtype":"Link",
			"options":"Warehouse",
			"width":150,
		},
		{
			"fieldname":"custom_warehouse_description",
			"label":"WAREHOUSE_NAME",
			"fieldtype":"Data",
			"width":150,
		},
		{
			"fieldname":"custom_sub_family_name",
			"label":"SUB FAMILY NAME",
			"fieldtype":"Data",
			"width":150,
		},
		{
			"fieldname":"custom_owner_code",
			"label":"OWNER_CODE",
			"fieldtype":"Data",
			"width":150,
		},
		{
			"fieldname":"serial_no",
			"label":"MSN",
			"fieldtype":"Link",
			"options":"Serial No",
			"width":150,
		},
		{
			"fieldname":"customer_batch",
			"label":"INWARD INVOICE NO",
			"fieldtype":"Data",
			"width":150,
		},
		{
			"fieldname":"qty",
			"label":"QUANTITY",
			"fieldtype":"Float",
			"width":150,
		},
		{
			"fieldname":"posting_date",
			"label":"DATE_INVENTORIED",
			"fieldtype":"Date",
			"width":150,
		},
		{
			"fieldname":"custom_category",
			"label":"CATEGORY",
			"fieldtype":"Data",
			"width":150,
		},

	]

	return columns , data


