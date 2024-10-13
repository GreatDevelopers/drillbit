# Copyright (c) 2024, Amrinder Singh and contributors
# For license information, please see license.txt
import os
import frappe
from frappe.model.document import Document
from assets.drillbit.drillbit_api import DrillbitAPI

@frappe.whitelist()
def hello(assignment):
    current_path = os.getcwd()
    assignment_name = frappe.parse_json(assignment).get("name")
    assignment_doc = frappe.get_doc("Assignment", assignment_name)
    drillbit_settings = frappe.get_single("Drillbit Settings")
    username = drillbit_settings.username
    password = drillbit_settings.get_password('password')

    frappe.msgprint(f"assignment name: {assignment_name}, current path: {current_path}, state: {assignment_doc.get_db_value('workflow_state')} {username} {password}")
    # frappe.get_doc({})
    # return f"hello, current path: {current_path}"

def get_absolute_path(file_name):
    if(file_name.startswith('/files/')):
        file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public{file_name}'
    if(file_name.startswith('/private/')):
        file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}{file_name}'
    return file_path

class Assignment(Document):
    def on_change(self):
        status = self.get_db_value("workflow_state")
        frappe.msgprint(f"Status: {status}")

        file_path=get_absolute_path(self.upload_assignment)
        drillbit_settings = frappe.get_single("Drillbit Settings")
        student_name = self.student_name
        title = self.title
        assignment_type = self.assignment_type
        student_email=self.student_email
        username = drillbit_settings.username
        password = drillbit_settings.get_password('password')
        guide_name = "Amrinder Singh"
        guide_email = "amrinder2676@gmail.com"
        

        base_url = "https://s1.drillbitplagiarismcheck.com"
        api = DrillbitAPI(base_url)
        if (api.is_token_valid()):
            frappe.msgprint("Token is valid")
        else:
            api.authenticate(username, password, frappe)
        # api.authenticate(username, password, frappe)
        # api.create_folder("New Folder")
        frappe.msgprint(f"{student_name}, {title},{assignment_type},{student_email} ,{guide_name}, {file_path}")
        # api.upload_file(student_name, title,assignment_type,student_email , mentor_name, "YES", "NO", "English", file_path)

        # frappe.msgprint(f"This is the Uploaded file: {file_path}")
        frappe.msgprint(f"Username: {username}, Password: {password}")
        # Change the attachment
        # new_attachment_path = "/path/to/new/attachment"
        # self.upload_assignment = new_attachment_path
        # self.save()
        # frappe.msgprint(f"Attachment changed to {new_attachment_path}")

    @frappe.whitelist()
    def button_press_action(self):
        frappe.msgprint("Button was pressed!")
    def on_save(self):
        drillbit_settings = frappe.get_single("Drillbit Settings")
        username = drillbit_settings.username
        password = drillbit_settings.get_password('password')
        frappe.msgprint(f"Username: {username}, Password: {password}")
    


    def on_submit(self):
        # Assuming upload_assignment is a field of type 'Attach'

        # frappe.msgprint(f"Student Email: {student_email}")
        # frappe.msgprint(f"Student Name: {student_name}")
        # frappe.msgprint(f"Mentor Name: {mentor_name}")
        # frappe.msgprint(f"Title: {title}")
        # frappe.msgprint(f"Assignment Type: {assignment_type}")
        # Extract username and password

        # current_directory = os.getcwd()
        # frappe.msgprint(current_directory)
        # Authenticate with Drillbit API
