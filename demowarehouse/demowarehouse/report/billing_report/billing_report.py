# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.utils import flt


def execute(filters=None):
	columns, data = [], []
	columns , data = get_data(filters)
	return columns, data



def get_data(filters):
	cond = ''
	if filters.get("from_date"):
		cond += f" and pr.posting_date >= '{filters.get('from_date')}'"

	if filters.get("to_date"):
		cond += f" and pr.posting_date <= '{filters.get('to_date')}'"
	if filters.get("supplier"):
		cond += f" and pr.supplier = '{filters.get('supplier')}'"

	data = frappe.db.sql(f"""
			Select pr.name , pr.is_return , pr.total_qty
			From `tabPurchase Receipt` as pr
			Where pr.docstatus = 1  {cond}
	""", as_dict = 1)

	pr_data_map = {}

	for row in data:
		pr_data_map[row.name] = row

	version_data = frappe.db.sql(f"""
			Select vr.ref_doctype , vr.docname, vr.data , pr.is_return
			From `tabVersion` as vr
			Left Join `tabPurchase Receipt` as pr ON pr.name = vr.docname
			Where ref_doctype = 'Purchase Receipt' and pr.docstatus = 1
	""", as_dict = 1)

	vr_final_data = []

	for row in version_data:
		if pr_data_map.get(row.docname):
			vr_final_data.append(row)
	I1W_charges_data = []
	ram_charges = []

	for row in vr_final_data:
		vr_data = json.loads(row.data)
		if vr_data.get('row_changed'):
			for d in vr_data.get('row_changed'):
				if d[0] == "items":
					for r in d[3]:
						if r[0] in ["custom_workflow_code", "custom_preset_workflow_code"] and (r[-1] == "I1W"):
							I1W_charges_data.append(d)

	inbound = []
	outbound = []
	stg_per_met = []
	for row in data:
		if not row.is_return:
			total_qty  = get_inbound_qty(row.name)
			inbound.append(total_qty)
		if row.is_return:
			outbound.append(row.total_qty)
			stg_per_met.append(row.total_qty)

	doc = frappe.get_doc("Cargo Billing Settings", None)

	cond = ''
	if filters.get("from_date"):
		cond += f" and pr.posting_date >= '{filters.get('from_date')}'"

	if filters.get("to_date"):
		cond += f" and pr.posting_date <= '{filters.get('to_date')}'"
	if filters.get("supplier"):
		cond += f" and pr.supplier = '{filters.get('supplier')}'"

	rme_charges = frappe.db.sql(f"""
			Select sum(qty) as qty
			From `tabPurchase Receipt Item` as pri
			Left Join `tabPurchase Receipt` as pr On pr.name = pri.parent
			Where pr.docstatus = 1 and pr.is_return != 1 and pri.custom_workflow_code = 'I1W' {cond}
	""",as_dict = 1)
	rme = 0
	if rme_charges:
		rme = rme_charges[0].get('qty')
	columns = [
		{
			"fieldname" : "charges",
			"fieldtype" : "Data",
			"label" : "Charges Type",
			'width': 200
		},
		{
			"fieldname" : "qty",
			"fieldtype" : "Float",
			"label" : "Quantity",
			'width': 100
		},
		{
			"fieldname" : "rate",
			"fieldtype" : "Currency",
			"label" : "Rate",
			'width': 100
		},
		{
			"fieldname" : "amount",
			"fieldtype" : "Currency",
			"label" : "Amount",
			'width': 100
		},
	]

	res = []

	res.append({
		"charges": "Inbound Charges",
		'amount' : sum(inbound) * doc.inbound,
		"qty" : sum(inbound), 
		"rate" : doc.inbound
		})
	
	res.append({
		"charges": "Outbound Charges", 
		"amount" : sum(outbound) * doc.outbound * -1, 
		'qty' : sum(outbound) * -1, 
		"rate" : doc.outbound
		})

	res.append({
		"charges": "RMA Charges", 
		"amount" : flt(rme) * flt(doc.rma) if flt(rme) else 0, 
		'qty' : rme , 
		"rate" : doc.rma
	})

	res.append({
		"charges": "Software Installation", 
		"amount" : sum(outbound) * doc.software_installation * -1, 
		'qty' : sum(outbound) * -1, 
		"rate" : doc.software_installation
		})

	res.append({
		"charges": "Storage Per Sq Meters", 
		"amount" : 1 * doc.storage_per_sq_meters , 
		'qty' : 1, 
		"rate" : doc.storage_per_sq_meters
		})
	
	res.append({
		"charges": "Admin Cost", 
		"amount" : 1 * doc.admin_cost , 
		'qty' : 1 , 
		"rate" : doc.admin_cost
		})

	

	return columns , res


def get_inbound_qty(pr):
	data = frappe.db.sql(f"""
						Select pri.qty
						From `tabPurchase Receipt Item` as pri
						Where pri.parent = '{pr}' and docstatus = 1 
	""", as_dict=1)
	total_qty = 0
	if data:
		for row in data:
			total_qty += row.qty
		return total_qty
	return 0 
