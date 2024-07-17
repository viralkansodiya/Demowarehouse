// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Process Report"] = {
	"filters": [
		{
			'fieldname':'from_date',
			'label':__('From Date'),
			'fieldtype':'Date',
			'width':100,
			'default':frappe.datetime.add_months(frappe.datetime.get_today(),-1)
		},
		{
			'fieldname':'to_date',
			'label':__('To Date'),
			'fieldtype':'Date',
			'width':100,
			'default':frappe.datetime.get_today()
		}
	]
};
