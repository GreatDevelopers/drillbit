# Copyright (c) 2024, Amrinder Singh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DrillbitSettings(Document):
    def on_update(self):
        #docSettings = frappe.get_single("Drillbit Settings")
        #strPassword = docSettings.get_password('password')
        frappe.msgprint("Your settings have been saved")
