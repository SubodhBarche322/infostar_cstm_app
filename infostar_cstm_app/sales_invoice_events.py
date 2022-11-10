# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _, msgprint, throw
from frappe.contacts.doctype.address.address import get_address_display
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils import (
	add_days,
	add_months,
	cint,
	cstr,
	flt,
	formatdate,
	get_link_to_form,
	getdate,
	nowdate,
)
from six import iteritems

import erpnext
from erpnext.accounts.deferred_revenue import validate_service_stop_date
from erpnext.accounts.doctype.loyalty_program.loyalty_program import (
	get_loyalty_program_details_with_points,
	validate_loyalty_points,
)
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import (
	get_party_tax_withholding_details,
)
from erpnext.accounts.general_ledger import get_round_off_account_and_cost_center
from erpnext.accounts.party import get_due_date, get_party_account, get_party_details
from erpnext.accounts.utils import get_account_currency
from erpnext.assets.doctype.asset.depreciation import (
	get_disposal_account_and_cost_center,
	get_gl_entries_on_asset_disposal,
	get_gl_entries_on_asset_regain,
	make_depreciation_entry,
)
from erpnext.controllers.accounts_controller import validate_account_head
from erpnext.controllers.selling_controller import SellingController
from erpnext.healthcare.utils import manage_invoice_submit_cancel
from erpnext.projects.doctype.timesheet.timesheet import get_projectwise_timesheet_data
from erpnext.setup.doctype.company.company import update_company_current_month_sales
from erpnext.stock.doctype.batch.batch import set_batch_nos
from erpnext.stock.doctype.delivery_note.delivery_note import update_billed_amount_based_on_so
from erpnext.stock.doctype.serial_no.serial_no import (
	get_delivery_note_serial_no,
	get_serial_nos,
	update_serial_nos_after_submit,
)


def generate_series(self,doc):
		
		print("************************************************************************************")
		print("Submitted")
		self.string_series = "CS-INS-"
		self.first_num = 10001
		self.first_num_str = str(self.first_num)
		first_series = self.string_series + self.first_num_str
		print(first_series)
		print(self.name)
		exists_or_not = frappe.db.sql(""" select custom_series from `tabSales Invoice` where custom_series = %s """,(first_series),as_dict=1)
		print(exists_or_not)
		is_empty = bool(exists_or_not)
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print(is_empty)

		if(is_empty == False):
			print("FFFFFFFFFFFFFFFFAAAAAAAALLLLLLLLLLLSSSSSSSEEEEEEEEEEEEE")
			frappe.db.sql(""" UPDATE `tabSales Invoice` SET custom_series=%s where name=%s""",(first_series,self.name))
			frappe.db.commit()
			print("First Series Created Successfully :) ")
			print("%%%%%%%%%%%%%% HERE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

		else:
			print("TTTTTTTTTTTTRRRRRRRRRRRRRRRUUUUUUUUUUUUUUUEEEEEEEEEEE")
			all_custom_series = frappe.db.sql(""" select max(custom_series) from `tabSales Invoice` where custom_series is not null """)
			print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
			print(all_custom_series)
			print(type(all_custom_series))
			t_to_string = str(all_custom_series)
			print(t_to_string[3:15])
			numerical_val= t_to_string[10:15]
			print("**********************")
			num_counter = int(numerical_val)
			print(type(num_counter))
			#print(num_counter)
			after_dash = self.name[13:15]
			if after_dash == "":
				num_counter += 1
				print(num_counter)
			else:
				num_counter = num_counter

			
			self.s_series = "CS-INS-"
			self.next_num = num_counter
			self.str_next_num = str(self.next_num)
			final_series = self.s_series + self.str_next_num + after_dash
			print(final_series)
			print("*******After Dash******************")
			
			print(after_dash)
			#print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
			#old_prev_num = num_counter
			#old_prev_num -= 1
			#self.prev_str_num = str(old_prev_num)
			#old_series = self.s_series + self.prev_str_num
			#series_exists_or_not = frappe.db.sql(""" select max(name) from `tabSales Invoice` where custom_series=%s""",(old_series),as_dict=1)
			#print(series_exists_or_not)
			#print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

			#cancelled or not = frappe.db.sql(""" select cancel_counter,custom_series,name from `tabSales Invoice` where """,as_dict=1)

			frappe.db.sql(""" UPDATE `tabSales Invoice` SET custom_series=%s where name=%s""",(final_series,self.name))
			print("%%%%%%%%%%%%%%%%%%HERE2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			frappe.db.commit()
			print("###### NEXT SERIES ADDED ######################")
			print("************************************************************************************")





