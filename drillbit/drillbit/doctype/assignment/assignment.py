# Copyright (c) 2024, Amrinder Singh and contributors
# For license information, please see license.txt
import os
import frappe
from frappe.model.document import Document
from assets.drillbit.drillbit_api import DrillbitAPI


def get_absolute_path(file_name):
    if(file_name.startswith('/files/')):
        file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public{file_name}'
    if(file_name.startswith('/private/')):
        file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}{file_name}'
    return file_path

class Assignment(Document):
    def on_save(self):
        print("hi")

    def on_submit(self):
        # Assuming upload_assignment is a field of type 'Attach'
        uploaded_file = self.upload_assignment
        
        # Retrieve the Drillbit Settings
        drillbit_settings = frappe.get_single("Drillbit Settings")
        
        # Extract username and password
        username = drillbit_settings.username
        password = drillbit_settings.get_password('password')
        # current_directory = os.getcwd()
        # frappe.msgprint(current_directory)
        # Authenticate with Drillbit API
        base_url = "https://s1.drillbitplagiarismcheck.com"
        api = DrillbitAPI(base_url)
        # api.authenticate(username, password, frappe)
        # api.create_folder("New Folder")
        folder_id=450824
        file_path=get_absolute_path(uploaded_file)
        author_name="Amrinder Singh"
        title="Effects of Air Space in ABF"
        document_type="Thesis"
        api.upload_file("Amrinder Singh", "Effects of Air Space in ABF 2004", "Thesis", "amrinder2676@gmail.com", "Amrinder", "YES", "NO", "English", file_path)


        frappe.msgprint(f"This is the Uploaded file: {file_path}")
        frappe.msgprint(f"Username: {username}, Password: {password}")
