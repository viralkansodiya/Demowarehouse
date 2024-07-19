# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

# import frappe


def execute(filters=None):
	columns, data = [], []
	return columns, data


def get_data(filters):
	cond = ''
	if filters.get('from_date'):
		cond += f" and pr.custom_date_shipped >= '{filters.get('from_date')}'"
	if filters.get('to_date'):
		cond += f" and pr.custom_date_shipped <= '{filters.get('to_date')}'"

	data = frappe.db.sql(f"""
			Select pr.name,
			pri.warehouse,
			item.custom_sub_family_name,
			pri.serial_no,
			pr.customer_batch,
			pr.custom_tracking_number,
			pri.qty,
			pri.custom_date_shipped,
			pr.custom_order_reference,
			w.custom_warehouse_description,
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
			"fieldname":"custom_warehouse_description",
			"label":"Sub Family Name",
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
			"fieldname":"custom_order_reference",
			"label":"ORDER REFERENCE",
			"fieldtype":"Data",
			"width":150,
		},
		{
			"fieldname":"custom_tracking_number",
			"label":"AWB/GCN #",
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
			"fieldname":"custom_date_shipped",
			"label":"DATE SHIPPED",
			"fieldtype":"Date",
			"width":150,
		}

	]

	return columns , data