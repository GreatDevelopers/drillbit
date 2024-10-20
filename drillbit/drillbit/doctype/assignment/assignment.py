# Copyright (c) 2024, Amrinder Singh and contributors
# For license information, please see license.txt
import os
import frappe
from frappe.model.document import Document
from assets.drillbit.drillbit_api import DrillbitAPI


def attach_file_to_assignment(file_path, assignment_name):
    # Create a new File document
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": file_path.split('/')[-1],  # Get the file name
        "file_url": f"/private/files/{file_path.split('/')[-1]}",  # URL of the file
        "is_private": 1,  # Set to 1 if the file is private
        "attached_to_doctype": "Assignment",  # Specify the Assignment doctype
        "attached_to_name": assignment_name,  # Specify the name or ID of the Assignment document
    })
    
    # Save the file document
    file_doc.insert()
    frappe.db.commit()
    
    # Link the file to the report field in the Assignment doctype
    assignment_doc = frappe.get_doc("Assignment", assignment_name)
    assignment_doc.report = file_doc.file_url  # Assuming 'report' is an Attach field
    assignment_doc.save()
    return file_doc.file_url

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

        username = frappe.get_single("Drillbit Settings").username
        password = frappe.get_single("Drillbit Settings").get_password('password')
        file_path=get_absolute_path(doc.upload_assignment)
        student_name = doc.student_name
        title = doc.title
        assignment_type = doc.assignment_type
        folder_id = str(frappe.get_doc("Drillbit Folder", doc.folder).folder_id)
        base_url = "https://s1.drillbitplagiarismcheck.com"
        if int(pliagiarism) == 1:
            check_plagiarism = "YES"
        else:
            check_plagiarism = "NO"
        if int(grammar) == 1: 
            check_grammar = "YES"
        else:
            check_grammar = "NO"

        api = DrillbitAPI(base_url)
        if (api.is_token_valid()):
            print("Token is valid")
        else:
            api.authenticate(username, password, frappe)
        if doc.changed_bool == 1:
            doc.paper_id = 0
            doc.d_key = ""
            doc.changed_bool = 0
        if str(doc.paper_id) == '0':
            print("nel")
            # frappe.msgprint(f"Uploading file: {file_path} for plagiarism check")
            uploaded_file = api.upload_file(student_name, title,assignment_type,mentor_email, mentor_name, check_plagiarism, check_grammar, "English", file_path, folder_id)
            if uploaded_file.get("status") == 200:
                paper_id = uploaded_file["submissions"]["paper_id"]
                d_key = uploaded_file["submissions"]["d_key"]
                doc.paper_id = int(paper_id)
                doc.d_key = str(d_key)
                doc.save()
                frappe.msgprint(f"File uploaded successfully for plagiarism check. Please check back after some time for the results.")
            else:
                message = uploaded_file.get("message")
                frappe.msgprint(f"Upload failed. {message}. Please contact the administrator.")
        else:
            site_path = os.path.abspath(frappe.utils.get_site_path()) + '/private/files/'
            file_url = ""
            if(doc.report != None):
                file_url = doc.report
            else:
                file = api.download_file(doc.paper_id, doc.d_key, site_path)
                if (file != None):
                    file_url = attach_file_to_assignment(file, doc.name)
                else:
                    frappe.throw("Download failed. Please wait until results or contact the administrator if it's been too long.")
            frappe.msgprint(f"File already uploaded for plagiarism check. Result can be viewed at: <a href=\"{file_url}\">Here</a> If not visble check back later.")

@frappe.whitelist()
def refresh_plagiarism_status(assignment, mentor_name, mentor_email, plagiarism, grammar):
    assignment_name = frappe.parse_json(assignment).get("name")
    assignment_doc = frappe.get_doc("Assignment", assignment_name)
    # password = frappe.get_single("Drillbit Settings").get_password('password');       frappe.msgprint(password)
    if(assignment_doc.folder == None):
        frappe.throw("Please select a folder for the assignment.")
    handleUpload(assignment_doc, plagiarism, grammar)


class Assignment(Document):
    def before_save(self):
        if self.has_value_changed('upload_assignment') and self.get_db_value("workflow_state") not in ["Pending", None]:
            frappe.throw(f"Cannot change the attached file after submission.")
        if self.has_value_changed('title') and self.get_db_value("workflow_state") not in ["Pending", None]:
            frappe.throw("Cannot change the title after submission.")
        if self.has_value_changed("assignment_type") and self.get_db_value("workflow_state") not in ["Pending", None]:
            frappe.throw("Cannot change the assignment type after submission.")
        if self.has_value_changed('folder'):
            self.changed_bool = 1