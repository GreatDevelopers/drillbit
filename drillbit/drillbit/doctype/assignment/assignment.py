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

def handleUpload(doc):
        user = frappe.session.user
        mentor_name = frappe.utils.get_fullname(user)
        mentor_email = frappe.db.get_value("User", user, "email")
        frappe.msgprint(f"{mentor_name} {mentor_email}")

        username = frappe.get_single("Drillbit Settings").username
        password = frappe.get_single("Drillbit Settings").get_password('password')
        file_path=get_absolute_path(doc.upload_assignment)
        student_name = doc.student_name
        title = doc.title
        assignment_type = doc.assignment_type
        base_url = "https://s1.drillbitplagiarismcheck.com"
        if doc.check_plagiarism == 1:
            check_plagiarism = "YES"
        else:
            check_plagiarism = "NO"
        if doc.check_grammar == 1: 
            check_grammar = "YES"
        else:
            check_grammar = "NO"
        # frappe.msgprint(f"Plagiarism Check: {check_plagiarism}, Grammar Check: {check_grammar}")
        doc.paper_id = "123456"
        doc.d_key = "123456"
        # doc.save()
        # api = DrillbitAPI(base_url)
        # if (api.is_token_valid()):
        #     print("Token is valid")
        # else:
        #     api.authenticate(username, password, frappe)
        # uploaded_file = api.upload_file(student_name, title,assignment_type,"amrinder2676@gmail.com", "Amrinder Singh", check_plagiarism, check_grammar, "English", file_path)
        # if uploaded_file.get("status") == 200:
        #     paper_id = uploaded_file["submissions"]["paper_id"]
        #     d_key = uploaded_file["submissions"]["d_key"]
            
        #     # Print the values
        #     # frappe.msgprint(f"Paper ID: {paper_id}, D Key: {d_key}")
        #     self.paper_id = paper_id
        #     self.d_key = d_key
        #     self.save()
        #     self.reload()
        # else:
        #     print("Upload failed with status:", uploaded_file.get("status"), "and message:", uploaded_file.get("message"))
        # frappe.msgprint(f"File uploaded: {uploaded_file}")



@frappe.whitelist()
def refresh_plagiarism_status(assignment, mentor_name, mentor_email):
    
    assignment_name = frappe.parse_json(assignment).get("name")
    frappe.msgprint(assignment_name)
    assignment_doc = frappe.get_doc("Assignment", assignment_name)
    assignment_doc.paper_id = 123456
    assignment_doc.d_key = "123456"
    assignment_doc.save()
    # drillbit_settings = frappe.get_single("Drillbit Settings")
    # username = drillbit_settings.username
    # password = drillbit_settings.get_password('password')

    # file_path=get_absolute_path(assignment_doc.upload_assignment)
    # drillbit_settings = frappe.get_single("Drillbit Settings")
    # student_name = assignment_doc.student_name
    # title = assignment_doc.title
    # assignment_type = assignment_doc.assignment_type
    # student_email=assignment_doc.student_email
    # username = drillbit_settings.username
    # password = drillbit_settings.get_password('password')
    # assignment_doc.save()
    # assignment_doc.reload()
    # frappe.msgprint(f"Document: {assignment_doc.upload_assignment}")
    frappe.msgprint(f"{assignment_doc.d_key}")

    # base_url = "https://s1.drillbitplagiarismcheck.com"
    # api = DrillbitAPI(base_url)
    # if (api.is_token_valid()):
    #     frappe.msgprint("Token is valid")
    # else:
    #     api.authenticate(username, password, frappe)
    
    # uploaded_file = api.upload_file(student_name, title,assignment_type,mentor_email, mentor_name, "YES", "NO", "English", file_path)

    # frappe.msgprint(f"assignment name: {assignment_name}, user: {mentor_name}, email: {mentor_email} state: {assignment_doc.get_db_value('workflow_state')} {username} {password}")
    return assignment_doc.title

class Assignment(Document):
    def on_change(self):
        print("on_change called")

    def on_save(self):
        # frappe.msgprint(f"Plagiarism Check: {self.check_plagiarism}, Grammar Check: {self.check_grammar}")
        print("on_save called")
        # drillbit_settings = frappe.get_single("Drillbit Settings")
        # username = drillbit_settings.username
        # password = drillbit_settings.get_password('password')
        # frappe.msgprint(f"Username: {username}, Password: {password}")
    
    def on_update(self):
        status = self.get_db_value("workflow_state")
        if(status == "In Review"):
            handleUpload(self)
    
    def on_submit(self):
        print("on_submit called")
        # status = self.get_db_value("workflow_state")

        # if(status == "In Review"):
        #     handleUpload(self)

        # frappe.msgprint(f"Status: {status}, Plagiarism Check: {self.check_plagiarism}, Grammar Check: {self.check_grammar}, user: {user_fullname}, email: {user_email}")
