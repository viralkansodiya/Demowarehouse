# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from frappe import _
import json


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

	cond += " and pri.custom_workflow_code = 'I1W' "

	data = frappe.db.sql(f"""
		Select pr.name,
		pr.set_warehouse,
		pr.customer_batch,
		pr.custom_customer_shipping_reference_1,
		pr.custom_customer_shipping_reference_2, 
		pr.custom_owner_code,
		item.description,
		pr.custom_owner_category,
		pr.supplier as owner_group,
		pri.item_code,
		item.custom_brand_code,
		item.custom_brand_name,
		item.custom_family_code,
		item.custom_family_name,
		item.custom_sub_family_code,
		item.custom_sub_family_name,
		pr.posting_date as DATE_RECEIVED,
		pr.custom_date_inventoried,
		pri.serial_no,
		pr.modified as last_activity_date_time,
		pri.custom_atn,
		pr.custom_current_activity,
		ca.current_activity_name,
		pri.custom_rfid,
		pri.custom_isn,
		pri.custom_workflow_code,
		item.custom_product_link_manufacturer_website
		From `tabPurchase Receipt` as pr
		Left Join `tabPurchase Receipt Item` as pri ON pri.parent = pr.name
		Left Join `tabItem` as item ON pri.item_code = item.name
		left join `tabCurrent Activity` as ca ON ca.name = pr.custom_current_activity
		Where pr.docstatus = 1 and is_return != 1 {cond}
	""", as_dict= 1)

	warehouse = frappe.db.sql(f"""
		SELECT name, custom_warehouse_description
		From `tabWarehouse`
	""",as_dict = 1)
	
	warehouse_map  = {}
	
	for row in warehouse:
		warehouse_map[row.name] = row

	for row in data:
		row.update({"last_activity_date":getdate(row.last_activity_date_time)})
		if warehouse_map.get(row.set_warehouse):
			row.update({'warehouse_name':warehouse_map.get(row.set_warehouse).get('custom_warehouse_description')})

	version_data = frappe.db.sql("""
				Select v.name, v.data, v.ref_doctype, v.docname, v.creation, u.full_name
				From `tabVersion`  as v
				Left Join `tabUser` as u ON u.name = v.owner
				Where ref_doctype = 'Purchase Receipt'
	""",as_dict=1)

	version_data_map = {}
	for row in version_data:
		row.update({"data" :json.loads(row.data) })
		if not version_data_map.get(row.docname):
			version_data_map[row.docname] = []
			version_data_map[row.docname].append(row)
		else:
			version_data_map[row.docname].append(row)

	final_data = []
	for row in data:
		final_data.append(row)
		if version_data_map.get(row.name):
			for d in version_data_map[row.name]:
				for r in d['data']['changed']:
					if r[0] == 'custom_current_activity':
						final_data.append(
											{
												'custom_current_activity' : r[2], 
												'last_activity_date_time':d['creation'], 
												'last_activity_date':getdate(d['creation']), 
												"current_activity_name":frappe.db.get_value('Current Activity', r[2], "current_activity_name"),
												"user" : d['full_name']
											}
										)

	return final_data

def get_columns(filters):
	return [
		{
			'fieldname': 'set_warehouse',
			'label': _('WAREHOUSE_CODE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'warehouse_name',
			'label': _('WAREHOUSE_NAME'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'customer_batch',
			'label': _('BOL_NUMBER'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_customer_shipping_reference_1',
			'label': _('CUSTOMER_SHIPPING_REFERENCE_1'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_customer_shipping_reference_2',
			'label': _('CUSTOMER_SHIPPING_REFERENCE_2'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'owner_group',
			'label': _('OWNER_GROUP'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_owner_category',
			'label': _('OWNER_CATEGORY'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_owner_code',
			'label': _('OWNER_CODE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_workflow_code',
			'label': _('WORKFLOW_CODE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'item_code',
			'label': _('Item Code'),
			'fieldtype': 'Link',
			"options":"Item",
			'width': 150
		},
		{
			'fieldname': 'description',
			'label': _('ITEM_DESCRIPTION'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_brand_code',
			'label': _('BRAND_CODE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_brand_name',
			'label': _('BRAND_NAME'),
			'fieldtype': 'Data',
			'width': 170
		},	
		{
			'fieldname': 'custom_family_code',
			'label': _('FAMILY_CODE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_family_name',
			'label': _('FAMILY_NAME'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_sub_family_code',
			'label': _('SUB_FAMILY_CODE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_sub_family_name',
			'label': _('SUB_FAMILY_NAME'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'DATE_RECEIVED',
			'label': _('DATE_RECEIVED'),
			'fieldtype': 'Date',
			'width': 170
		},
		{
			'fieldname': 'custom_date_inventoried',
			'label': _('DATE_INVENTORIED'),
			'fieldtype': 'Date',
			'width': 170
		},
		{
			'fieldname': 'serial_no',
			'label': _('MANUFACTURER_SERIAL_NUMBER'),
			'fieldtype': 'Link',
			'options':"Serial No",
			'width': 170
		},
		{
			'fieldname': 'custom_atn',
			'label': _('ATN'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_rfid',
			'label': _('RFID'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_isn',
			'label': _('INTERNAL_SERIAL_NUMBER'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'custom_current_activity',
			'label': _('CURRENT_ACTIVITY'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'current_activity_name',
			'label': _('CURRENT_ACTIVITY_NAME'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'last_activity_date',
			'label': _('LAST_ACTIVITY_DATE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'last_activity_date_time',
			'label': _('LAST_ACTIVITY_DATE_TIME'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'user',
			'label': _('USER'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'current_condition_code',
			'label': _('CURRENT_CONDITION_CODE'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'current_classification',
			'label': _('CURRENT_CLASSIFICATION'),
			'fieldtype': 'Data',
			'width': 170
		},
		{
			'fieldname': 'condition_code',
			'label': _('CONDITION_CODE'),
			'fieldtype': 'Data',
			'width': 170
		}
	]