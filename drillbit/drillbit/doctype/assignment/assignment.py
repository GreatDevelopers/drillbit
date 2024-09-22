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
        drillbit_settings = frappe.get_single("Drillbit Settings")
        username = drillbit_settings.username
        password = drillbit_settings.get_password('password')
        frappe.msgprint(f"Username: {username}, Password: {password}")

    def on_submit(self):
        # Assuming upload_assignment is a field of type 'Attach'
        uploaded_file = self.upload_assignment
        file_path=get_absolute_path(uploaded_file)
        drillbit_settings = frappe.get_single("Drillbit Settings")
        student_email = self.student
        student_name = self.student_name
        mentor_name = self.mentor_name
        title = self.title
        assignment_type = self.assignment_type
        student_email=self.student_email

        # frappe.msgprint(f"Student Email: {student_email}")
        # frappe.msgprint(f"Student Name: {student_name}")
        # frappe.msgprint(f"Mentor Name: {mentor_name}")
        # frappe.msgprint(f"Title: {title}")
        # frappe.msgprint(f"Assignment Type: {assignment_type}")
        # Extract username and password
        username = drillbit_settings.username
        password = drillbit_settings.get_password('password')
        # current_directory = os.getcwd()
        # frappe.msgprint(current_directory)
        # Authenticate with Drillbit API
        base_url = "https://s1.drillbitplagiarismcheck.com"
        api = DrillbitAPI(base_url)
        if (api.is_token_valid()):
            print("Token is valid")
        else:
            api.authenticate(username, password, frappe)
        # api.authenticate(username, password, frappe)
        # api.create_folder("New Folder")
        frappe.msgprint(f"{student_name}, {title},{assignment_type},{student_email} ,{ mentor_name}, {file_path}")
        # api.upload_file(student_name, title,assignment_type,student_email , mentor_name, "YES", "NO", "English", file_path)


        # frappe.msgprint(f"This is the Uploaded file: {file_path}")
        frappe.msgprint(f"Username: {username}, Password: {password}")
