# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 

def execute(filters=None):
	columns, data = [], []
	data =  get_data(filters)
	columns = get_columns(filters)
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
		pr.customer_batch,
		pr.custom_customer_shipping_reference_1,
		pr.custom_customer_shipping_reference_2, 
		pr.custom_owner_code,
		pr.custom_hu_id,
		pr.custom_hu_type_code,
		item.description,
		pr.custom_hu_type_name,
		pr.custom_hu_gross_weight,
		pr.custom_owner_category,
		pr.supplier as owner_group,
		pri.item_code,
		item.custom_inventory_user_name,
		item.custom_manufacturer_item_code,
		item.custom_brand_code,
		item.custom_brand_name,
		item.custom_machine_type,
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
		pri.custom_rfid,
		item.custom_vendor_part_number,
		pri.custom_isn,
		pri.custom_length,
		pri.custom_weight,
		pri.manufacturer_part_no,
		pr.custom_date_time_inventoried,
		pri.custom_height,
		pri.custom_width,
		pr.custom_po_uploaded,
		pr.custom_default_activity,
		pri.custom_preset_workflow_code,
		pr.custom__first_activity,
		pr.custom__damage_code_inventory,
		pri.custom_workflow_code,
		pri.custom_category,
		item.custom_product_link_manufacturer_website
		From `tabPurchase Receipt` as pr
		Left Join `tabPurchase Receipt Item` as pri ON pri.parent = pr.name
		Left Join `tabItem` as item ON pri.item_code = item.name
		Where pr.docstatus = 1 and pri.custom_preset_workflow_code = 'INS' {cond}
	""", as_dict= 1)

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

	return data

def get_columns(filters):
	return [
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
			'fieldname': 'customer_batch',
			'label': _('BOL_NUMBER'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_customer_shipping_reference_1',
			'label': _('CUSTOMER_SHIPPING_REFERENCE_1'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_customer_shipping_reference_2',
			'label': _('CUSTOMER_SHIPPING_REFERENCE_2'),
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
			'fieldname': 'custom_preset_workflow_code',
			'label': _('PreSet WORKFLOW_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'item_code',
			'label': _('ITEM_CODE'),
			'fieldtype': 'Link',
			"options" : "Item",
			'width': 150
		},
		{
			'fieldname': 'description',
			'label': _('ITEM_DESCRIPTION'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_vendor_part_number',
			'label': _('VENDOR_PART_NUMBER'),
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
			'fieldname': 'custom_brand_code',
			'label': _('BRAND_CODE'),
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
			'fieldname': 'custom_machine_type',
			'label': _('MACHINE_TYPE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_model_no',
			'label': _('MODEL_NUMBER'),
			'fieldtype': 'Data',
			'width': 150
		},
		
		
		
		{
			'fieldname': 'custom_family_code',
			'label': _('FAMILY_CODE'),
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
			'fieldname': 'custom_sub_family_code',
			'label': _('SUB_FAMILY'),
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
			'fieldname': 'custom_date_time_inventoried',
			'label': _('DATE_TIME_INVENTORIED'),
			'fieldtype': 'Datetime',
			'width': 150
		},
		{
			'fieldname': 'qty',
			'label': _('QUANTITY'),
			'fieldtype': 'Float',
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
			'fieldname': 'custom_isn',
			'label': _('ISN'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_release_date',
			'label': _('RELEASE_DATE'),
			'fieldtype': 'Date',
			'width': 150
		},
		{
			'fieldname': 'custom_end_of_sales_date',
			'label': _('END_OF_SALES_DATE'),
			'fieldtype': 'Date',
			'width': 150
		},
		{
			'fieldname': 'custom_end_of_support_date',
			'label': _('END_OF_SUPPORT_DATE'),
			'fieldtype': 'Date',
			'width': 150
		},
		{
			'fieldname': 'custom_hu_id',
			'label': _('HU_ID'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_hu_type_code',
			'label': _('HU_TYPE_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_hu_type_name',
			'label': _('HU_TYPE_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_hu_gross_weight',
			'label': _('HU_GROSS_WEIGHT'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_lease_code',
			'label': _('LEASE_CODE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_po_uploaded',
			'label': _('PO_UPLOADED'),
			'fieldtype': 'Datetime',
			'width': 150
		},
		{
			'fieldname': 'custom_default_activity',
			'label': _('DEFAULT_ACTIVITY '),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom__first_activity',
			'label': _('FIRST_ACTIVITY '),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom__damage_code_inventory',
			'label': _('DAMAGE_CODE_INVENTORY'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_inventory_user_name',
			'label': _('INVENTORY_USER_NAME'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_product_link_manufacturer_website',
			'label': _('PRODUCT_LINK_MANUFACTURER_WEBSITE'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_length',
			'label': _('LENGHT'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_width',
			'label': _('WIDTH'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_height',
			'label': _('HEIGHT'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_weight',
			'label': _('WEIGHT'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'custom_category',
			'label': _('CATEGORY'),
			'fieldtype': 'Data',
			'width': 150
		}
	]
