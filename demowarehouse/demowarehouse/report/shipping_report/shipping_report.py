# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe

from frappe import _

def execute(filters=None):
	columns, data = [], []
	cond = ''
	if filters.get('from_date'):
		cond += f" and pr.posting_date >= '{filters.get('from_date')}'"
	if filters.get('to_date'):
		cond += f" and pr.posting_date <= '{filters.get('to_date')}'"
	data = frappe.db.sql(f"""
		Select pr.set_warehouse,
		pr.custom_order_type,
		pr.custom_order_type_description,
		pr.custom_order_reference,
		pr.custom_tracking_number,
		pr.custom_ship_to_code,
		pr.custom_ship_to_name,
		pr.custom_date_created,
		item.custom__item_detailed_description,
		pr.custom_date_shipped,
		pr.customer_address as address,
		pr.custom_date_time_shipped,
		pri.item_code,
		pri.description,
		item.custom_family_name,
		item.custom_sub_family_name,
		item.custom_manufacturer_item_code,
		pr.posting_date as DATE_RECEIVED,
		pr.custom_date_inventoried,
		pri.qty,
		item.custom_isn,
		item.custom_atn,
		pri.serial_no,
		item.custom_rfid,
		pr.custom_condition_code,
		pr.supplier as owner_group,
		pr.custom_owner_code,
		pr.custom_owner_category,
		pri.custom_workflow_code
		From `tabPurchase Receipt` as pr
		Left Join `tabPurchase Receipt Item` as pri ON pri.parent = pr.name
		Left Join `tabItem` as item ON pri.item_code = item.name
		Where pr.docstatus = 1 {cond}

	
	""",as_dict=1)
	warehouse = frappe.db.sql(f"""
		SELECT name, custom_warehouse_description
		From `tabWarehouse`
	""",as_dict = 1)
	
	warehouse_map  = {}
	
	for row in warehouse:
		warehouse_map[row.name] = row

	for row in data:
		if warehouse_map.get(row.set_warehouse):
			row.update({'warehouse_name':warehouse_map.get(row.set_warehouse).get('custom_warehouse_description')})

	final_data = []
	for row in data:
		serial_no = row.serial_no.split('\n')
		demo_row = row
		for d in serial_no:
			demo_row.update({"serial_no":d})
			final_data.append(demo_row)
	
	columns = [
		{
			'fieldname': 'set_warehouse',
			'label': _('WAREHOUSE_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'warehouse_name',
			'label': _('WAREHOUSE_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_order_type',
			'label': _('ORDER_TYPE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_order_type_description',
			'label': _('ORDER_TYPE_DESCRIPTION'),
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
			'fieldname': 'custom_tracking_number',
			'label': _('TRACKING_NUMBER'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_ship_to_code',
			'label': _('SHIP_TO_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_ship_to_name',
			'label': _('SHIP_TO_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'address',
			'label': _('SHIP_TO_ADDRESS'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_date_created',
			'label': _('DATE_CREATED'),
			'fieldtype': 'Date',
			'width': 150
		},
		{
			'fieldname': 'custom_date_shipped',
			'label': _('DATE_SHIPPED'),
			'fieldtype': 'Date',
			'width': 150
		},
		{
			'fieldname': 'custom_date_time_shipped',
			'label': _('DATE_TIME_SHIPPED'),
			'fieldtype': 'Datetime',
			'width': 150
		},
		{
			'fieldname': 'item_code',
			'label': _('ITEM_CODE'),
			'fieldtype': 'Link',
			"options":"Item",
			'width': 150
		},
		{
			'fieldname': 'custom__item_detailed_description',
			'label': _('ITEM_DESCRIPTION'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_manufacturer_item_code',
			'label': _('MANUFACTURER_ITEM_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_family_name',
			'label': _('FAMILY_NAME'),
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
			'fieldname': 'DATE_RECEIVED',
			'label': _('DATE_RECEIVED'),
			'fieldtype': 'Date',
			'width': 150
		},
		{
			'fieldname': 'custom_date_inventoried',
			'label': _('DATE_INVENTORIED'),
			'fieldtype': 'Date',
			'width': 150
		},
		
		{
			'fieldname': 'qty',
			'label': _('QUANTITY'),
			'fieldtype': 'Float',
			'width': 150
		},
		{
			'fieldname': 'custom_isn',
			'label': _('ISN'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'serial_no',
			'label': _('MSN'),
			'fieldtype': 'Link',
			'options':"Serial No",
			'width': 150
		},
		{
			'fieldname': 'custom_atn',
			'label': _('ATN'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_rfid',
			'label': _('RFID'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'owner_group',
			'label': _('OWNER_GROUP'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_owner_code',
			'label': _('OWNER_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_owner_category',
			'label': _('OWNER_CATEGORY'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_workflow_code',
			'label': _('WORKFLOW_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_condition_code',
			'label': _('CONDITION_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_classification',
			'label': _('CLASSIFICATION'),
			'fieldtype': 'Data',
			'width': 100
		},
		

	]
	
	
	
	return columns, final_data
