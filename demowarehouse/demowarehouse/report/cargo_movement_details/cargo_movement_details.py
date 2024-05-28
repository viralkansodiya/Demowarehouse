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
		pri.warehouse,
		pr.customer_batch,
		pr.custom_customer_shipping_reference_1,
		pr.custom_customer_shipping_reference_2, 
		pr.custom_owner_code,
		pr.custom_owner_category,
		pr.supplier as owner_group,
		pri.item_code,
		pri.description,
		item.custom_manufacturer_item_code,
		item.custom_brand_code,
		item.custom_brand_name,
		item.custom_machine_type,
		item.custom_model_no,
		item.custom_family_code,
		item.custom_family_name,
		item.custom_sub_family_code,
		item.custom_sub_family_name,
		pr.posting_date as DATE_RECEIVED,
		pr.custom_date_inventoried,
		pri.qty,
		pri.serial_no,
		pri.custom_atn,
		pri.custom_rfid,
		pri.custom_isn,
		pri.custom_length,
		pri.custom_weight,
		pri.custom_height,
		pri.custom_width,
		pri.custom_workflow_code,
		pri.custom_category
		From `tabPurchase Receipt` as pr
		Left Join `tabPurchase Receipt Item` as pri ON pri.parent = pr.name
		Left Join `tabItem` as item ON pri.item_code = item.name
		Where pr.docstatus = 1 {cond}
	""", as_dict= 1)
	
	return data

def get_columns(filters):
	return [
		{
			'fieldname': 'warehouse',
			'label': _('Warehouse Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'customer_batch',
			'label': _('Bol Number'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_customer_shipping_reference_1',
			'label': _('CUSTOMER_SHIPPING_REFERENCE_1'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_customer_shipping_reference_2',
			'label': _('CUSTOMER_SHIPPING_REFERENCE_2'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'owner_group',
			'label': _('Owner Group'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_owner_code',
			'label': _('Owner Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_workflow_code',
			'label': _('Workflow Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_owner_category',
			'label': _('Owner Category'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'item_code',
			'label': _('Item Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'description',
			'label': _('Item Description'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_manufacturer_item_code',
			'label': _('Manufacturer Item Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_brand_code',
			'label': _('Brand Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_brand_name',
			'label': _('Brand Name'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_machine_type',
			'label': _('Machine Type'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_model_no',
			'label': _('Model No'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_family_code',
			'label': _('Family Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_family_name',
			'label': _('Family Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_sub_family_code',
			'label': _('Sub Family Code'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_sub_family_name',
			'label': _('Sub Family Name'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'DATE_RECEIVED',
			'label': _('Date Received'),
			'fieldtype': 'Date',
			'width': 100
		},
		{
			'fieldname': 'custom_date_inventoried',
			'label': _('Date Inventoried'),
			'fieldtype': 'Date',
			'width': 100
		},
		{
			'fieldname': 'qty',
			'label': _('Qty'),
			'fieldtype': 'Float',
			'width': 100
		},
		{
			'fieldname': 'serial_no',
			'label': _('Serial No'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_atn',
			'label': _('ATN'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_rfid',
			'label': _('RFID'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_length',
			'label': _('Length'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_weight',
			'label': _('Weight'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_height',
			'label': _('Height'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_width',
			'label': _('Width'),
			'fieldtype': 'Data',
			'width': 100
		},
		{
			'fieldname': 'custom_category',
			'label': _('Category'),
			'fieldtype': 'Data',
			'width': 100
		}
	]
