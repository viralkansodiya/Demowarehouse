# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	cond = ''
	if filters.get('from_date'):
		cond += f" and pr.posting_date >= '{filters.get('from_date')}'"
	if filters.get('to_date'):
		cond += f" and pr.posting_date <= '{filters.get('to_date')}'"

	data = frappe.db.sql(f"""
		Select pr.set_warehouse,
		pr.supplier,
		pri.warehouse,
		pr.customer_batch,
		pr.custom_customer_shipping_reference_1,
		pr.custom_customer_shipping_reference_2, 
		pr.custom_owner_code,
		pr.custom_hu_id,
		pr.custom_hu_type_code,
		pr.custom_hu_type_name,
		pr.custom_hu_gross_weight,
		pr.custom_owner_category,
		pr.supplier as owner_group,
		pri.item_code,
		item.custom_inventory_user_name,
		pri.description,
		item.custom_manufacturer_item_code,
		item.custom_brand_code,
		item.custom_brand_name,
		item.custom_machine_type,
		pr.custom_date_time_stock_entry,
		pr.custom_configuration_memory,
		item.custom_model_no,
		item.custom_family_code,
		item.custom_family_name,
		item.custom_sub_family_code,
		item.custom_sub_family_name,
		item.custom_end_of_sales_date,
		item.custom_end_of_support_date,
		pr.posting_date as DATE_RECEIVED,
		pr.custom_date_inventoried,
		pri.qty,
		pri.serial_no,
		pri.custom_atn,
		item.custom_vendor_part_number,
		pri.custom_rfid,
		pri.custom_isn,
		pri.custom_length,
		pr.custom_store_description,
		pri.custom_weight,
		pri.custom_height,
		pr.custom_store_code,
		pri.custom_width,
		pri.manufacturer_part_no,
		pr.custom_po_uploaded,
		pr.custom_default_activity,
		pr.custom__first_activity,
		pr.custom__damage_code_inventory,
		pri.custom_workflow_code,
		pr.custom_configuration_os,
		pr.custom_date_stock_entry,
		pri.custom_current_classification_code,
		pri.custom_current_condition_code,
		pr.custom_condition_code,
		pri.serial_no,
		pri.custom_category,
		item.custom_product_link_manufacturer_website
		From `tabPurchase Receipt` as pr
		Left Join `tabPurchase Receipt Item` as pri On pri.parent = pr.name
		Left Join `tabItem` as item ON pri.item_code = item.name
		Where pr.docstatus = 1 {cond}
	""",as_dict =1 )

	final_data = []
	for row in data:
		serial_no = row.serial_no.split('\n')
		demo_row = row
		for d in serial_no:
			demo_row.update({"serial_no":d})
			final_data.append(demo_row)
	
	warehouse = frappe.db.sql(f"""
		SELECT name, custom_warehouse_description
		From `tabWarehouse`
	""",as_dict = 1)
	
	warehouse_map  = {}
	
	for row in warehouse:
		warehouse_map[row.name] = row

	for row in final_data:
		if warehouse_map.get(row.set_warehouse):
			row.update({'warehouse_name':warehouse_map.get(row.set_warehouse).get('custom_warehouse_description')})

	return columns, final_data




def get_columns(filters):
	columns = [
		{
			'fieldname': 'set_warehouse',
			'label': _('WAREHOUSE_CODE'),
			'fieldtype': 'Link',
			"options":"Warehouse",
			'width': 150
		},
		{
			'fieldname': 'warehouse_name',
			'label': _('WAREHOUSE_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'supplier',
			'label': _('OWNER_GROUP'),
			'fieldtype': 'Link',
			"options":"Supplier",
			'width': 150
		},
		{
			'fieldname': 'custom_owner_category',
			'label': _('OWNER_CATEGORY'),
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
			'fieldname': 'custom_workflow_code',
			'label': _('WORKFLOW_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'item_code',
			'label': _('Item Code'),
			'fieldtype': 'Link',
			"options":"Item",
			'width': 150
		},
		{
			'fieldname': 'manufacturer_part_no',
			'label': _('MANUFACTURER_PART_NUMBER'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': "description",
			'label': _('ITEM_DESCRIPTION'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_brand_name',
			'label': _('BRAND_NAME'),
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
			'label': _('SUBFAMILY_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_default_activity',
			'label': _('CURRENT_ACTIVITY_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_current_condition_code',
			'label': _('CURRENT_CONDITION_CODE'),
			'fieldtype': 'Data',
			'width': 200
		},
		{
			'fieldname': 'custom_current_classification_code',
			'label': _('CURRENT_CLASSIFICATION_CODE'),
			'fieldtype': 'Data',
			'width': 200
		},
		{
			'fieldname': 'serial_no',
			'label': _('MSN'),
			'fieldtype': 'Data',
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
			'fieldname': 'custom_isn',
			'label': _('ISN'),
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
			'fieldname': 'custom_store_code',
			'label': _('STORE_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_store_description',
			'label': _('STORE_DESCRIPTION'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_date_stock_entry',
			'label': _('DATE_STOCK_ENTRY'),
			'fieldtype': 'Date',
			'width': 150
		},
		{
			'fieldname': 'custom_date_time_stock_entry',
			'label': _('DATE_TIME_STOCK_ENTRY'),
			'fieldtype': 'Datetime',
			'width': 150
		},
		{
			'fieldname': 'custom_configuration_memory',
			'label': _('CONFIGURATION_MEMORY'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_configuration_os',
			'label': _('CONFIGURATION_OS'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_condition_code',
			'label': _('CONDITION_CODE'),
			'fieldtype': 'Data',
			'width': 150
		}
		
	]
	return columns