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

@frappe.whitelist()
def hello(assignment, mentor_name, mentor_email):
    current_path = os.getcwd()
    assignment_name = frappe.parse_json(assignment).get("name")
    assignment_doc = frappe.get_doc("Assignment", assignment_name)
    drillbit_settings = frappe.get_single("Drillbit Settings")
    username = drillbit_settings.username
    password = drillbit_settings.get_password('password')

    file_path=get_absolute_path(assignment_doc.upload_assignment)
    drillbit_settings = frappe.get_single("Drillbit Settings")
    student_name = assignment_doc.student_name
    title = assignment_doc.title
    assignment_type = assignment_doc.assignment_type
    student_email=assignment_doc.student_email
    username = drillbit_settings.username
    password = drillbit_settings.get_password('password')
    guide_name = "Amrinder Singh"
    guide_email = "amrinder2676@gmail.com"
    assignment_doc.title = "Newasfsf asfasfas"
    assignment_doc.save()
    assignment_doc.reload()
    return assignment_doc.title
    

    # base_url = "https://s1.drillbitplagiarismcheck.com"
    # api = DrillbitAPI(base_url)
    # if (api.is_token_valid()):
    #     frappe.msgprint("Token is valid")
    # else:
    #     api.authenticate(username, password, frappe)
    
    # uploaded_file = api.upload_file(student_name, title,assignment_type,mentor_email, mentor_name, "YES", "NO", "English", file_path)
    #                   upload_file(author_name, title, document_type, guide_email, guide_name, plagiarism_check, grammar_check, language, file_path)

    # frappe.msgprint(f"assignment name: {assignment_name}, user: {mentor_name}, email: {mentor_email} state: {assignment_doc.get_db_value('workflow_state')} {username} {password}")
    # frappe.get_doc({})
    # return f"hello, current path: {current_path}"

class Assignment(Document):
    def on_change(self):
        status = self.get_db_value("workflow_state")
        user = frappe.session.user
        user_fullname = frappe.utils.get_fullname(user)
        user_email = frappe.db.get_value("User", user, "email")
        frappe.msgprint(f"Status: {status}, Plagiarism Check: {self.check_plagiarism}, Grammar Check: {self.check_grammar}, user: {user_fullname}, email: {user_email}")

    def on_save(self):
        # frappe.msgprint(f"Plagiarism Check: {self.check_plagiarism}, Grammar Check: {self.check_grammar}")
        print("on_save called")
        # drillbit_settings = frappe.get_single("Drillbit Settings")
        # username = drillbit_settings.username
        # password = drillbit_settings.get_password('password')
        # frappe.msgprint(f"Username: {username}, Password: {password}")
    
    def on_submit(self):
        print("on_submit called")
