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

def handleUpload(doc, pliagiarism, grammar):
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
        if int(pliagiarism) == 1:
            check_plagiarism = "YES"
        else:
            check_plagiarism = "NO"
        if int(grammar) == 1: 
            check_grammar = "YES"
        else:
            check_grammar = "NO"
        frappe.msgprint(f"Plagiarism Check: {check_plagiarism}, Grammar Check: {check_grammar}")


        api = DrillbitAPI(base_url)
        frappe.msgprint(f"jwt_token: {api.jwt_token}")
        if (api.is_token_valid()):
            print("Token is valid")
        else:
            api.authenticate(username, password, frappe)
        if str(doc.paper_id) == '0':
            print("nel")
            frappe.msgprint(f"Uploading file: {file_path} for plagiarism check")
            uploaded_file = api.upload_file(student_name, title,assignment_type,"amrinder2676@gmail.com", "Amrinder Singh", check_plagiarism, check_grammar, "English", file_path)
            if uploaded_file.get("status") == 200:
                paper_id = uploaded_file["submissions"]["paper_id"]
                d_key = uploaded_file["submissions"]["d_key"]
                doc.paper_id = int(paper_id)
                doc.d_key = str(d_key)
                doc.save()
                frappe.msgprint(f"File uploaded successfully for plagiarism check. Result can be viewed at: {base_url}/drillbit-analysis/analysis/{api.jwt_token}")
            else:
                frappe.msgprint("Upload failed.")
                print(f"Upload failed with status:", uploaded_file.get("status"), "and message:", uploaded_file.get("message"))
        else:
            frappe.msgprint(f"File already uploaded for plagiarism check. Result can be viewed at: {base_url}/drillbit-analysis/analysis/{doc.paper_id}/{doc.d_key}/{api.jwt_token}")


@frappe.whitelist()
def refresh_plagiarism_status(assignment, mentor_name, mentor_email, plagiarism, grammar):
    
    assignment_name = frappe.parse_json(assignment).get("name")
    assignment_doc = frappe.get_doc("Assignment", assignment_name)
    handleUpload(assignment_doc, plagiarism, grammar)
    # frappe.msgprint(assignment_name)
    # assignment_doc.paper_id = 123456
    # assignment_doc.d_key = "123456"
    # assignment_doc.save()

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
        print("on_update called")
        # status = self.get_db_value("workflow_state")
        # if(status == "In Review"):
        #     handleUpload(self)
    
    def on_submit(self):
        print("on_submit called")
        # status = self.get_db_value("workflow_state")

        # if(status == "In Review"):
        #     handleUpload(self)

        # frappe.msgprint(f"Status: {status}, Plagiarism Check: {self.check_plagiarism}, Grammar Check: {self.check_grammar}, user: {user_fullname}, email: {user_email}")
