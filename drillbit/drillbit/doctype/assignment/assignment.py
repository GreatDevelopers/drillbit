# Copyright (c) 2024, Amrinder Singh and contributors
# For license information, please see license.txt
import os
import frappe
from frappe.model.document import Document
from assets.drillbit.drillbit_api import DrillbitAPI

class Assignment(Document):
    def on_submit(self):
        # Assuming upload_assignment is a field of type 'Attach'
        uploaded_file = self.upload_assignment
        
        # Retrieve the Drillbit Settings
        drillbit_settings = frappe.get_single("Drillbit Settings")
        
        # Extract username and password
        username = drillbit_settings.username
        password = drillbit_settings.get_password('password')
        current_directory = os.getcwd()
        frappe.msgprint(current_directory)
        # Authenticate with Drillbit API
        base_url = "https://s1.drillbitplagiarismcheck.com"
        # api = DrillbitAPI(base_url)
        # api.authenticate(username, password, frappe)
        # api.create_folder("New Folder")

        frappe.msgprint(f"This is the Uploaded file: {frappe.get_site_path()}{uploaded_file}")
        frappe.msgprint(f"Username: {username}, Password: {password}")
