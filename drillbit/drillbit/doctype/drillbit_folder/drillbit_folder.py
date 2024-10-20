# Copyright (c) 2024, Amrinder Singh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from assets.drillbit.drillbit_api import DrillbitAPI

def check_value(value):
	if str(value) == "1":
		return "YES"
	return "NO"

def handle_folder_create(self):
		base_url = "https://s1.drillbitplagiarismcheck.com"
		username = frappe.get_single("Drillbit Settings").username
		password = frappe.get_single("Drillbit Settings").get_password('password')
		api = DrillbitAPI(base_url)
		# frappe.msgprint(f"jwt_token: {api.jwt_token}")
		if (api.is_token_valid()):
			print("Token is valid")
		else:
			api.authenticate(username, password, frappe)
		exclude_phrases_value = "NO" if self.exclude_phrases is None else "YES"
		phrases = {}
		if self.exclude_phrases is not None:
			phrases = {f"p{index + 1}": line for index, line in enumerate(self.exclude_phrases.splitlines())}
		# frappe.msgprint(f"Phrases: {phrases}")
		response = api.create_folder(
			folder_name=self.folder_name,
			exclude_reference=check_value(self.exclude_reference__bibliography),
			exclude_quotes=check_value(self.exclude_quotes),
			exclude_small_sources=check_value(self.exclude_small_sources),
			grammar_check=check_value(self.grammar_check),
			exclude_phrases=exclude_phrases_value,
			db_studentpaper=check_value(self.student_papers),
			db_publications=check_value(self.journals_and_publishers),
			db_internet=check_value(self.internet_or_web),
			institution_repository=check_value(self.institution_repository),
			email_notifications=check_value(self.email_notification),
			phrases=phrases
		)
		if(response.status_code != 201):
			frappe.msgprint(str(response.status_code))
			frappe.msgprint(response.json()['message'])
			self.cancel()
		if(response and response.status_code==201):
			self.created_at = response.json()['timeStamp']
			self.folder_id = int(response.json()['_links']['self']['href'].split('/')[-1])
			self.name = self.folder_name + "-" + str(self.folder_id)
		else:
			frappe.errprint("Error creating folder")

def handle_folder_edit(self):
		base_url = "https://s1.drillbitplagiarismcheck.com"
		username = frappe.get_single("Drillbit Settings").username
		password = frappe.get_single("Drillbit Settings").get_password('password')
		api = DrillbitAPI(base_url)
		# frappe.msgprint(f"jwt_token: {api.jwt_token}")
		if (api.is_token_valid()):
			print("Token is valid")
		else:
			api.authenticate(username, password, frappe)
		exclude_phrases_value = "NO" if self.exclude_phrases is None else self.exclude_phrases
		phrases = {}
		if self.exclude_phrases is not None:
			phrases = {f"p{index + 1}": line for index, line in enumerate(self.exclude_phrases.splitlines())}
		response = api.edit_folder(
			folder_id=self.folder_id,
			folder_name=self.folder_name,
			exclude_reference=check_value(self.exclude_reference__bibliography),
			exclude_quotes=check_value(self.exclude_quotes),
			exclude_small_sources=check_value(self.exclude_small_sources),
			grammar_check=check_value(self.grammar_check),
			exclude_phrases=exclude_phrases_value,
			db_studentpaper=check_value(self.student_papers),
			db_publications=check_value(self.journals_and_publishers),
			db_internet=check_value(self.internet_or_web),
			institution_repository=check_value(self.institution_repository),
			email_notifications=check_value(self.email_notification),
			phrases=phrases
		)
		if(response.status_code != 201):
			frappe.msgprint(str(response.status_code))
			frappe.msgprint(response.json()['message'])
			self.cancel()
		if(response and response.status_code==201):
			frappe.msgprint(f"updated the folder {self.name}")
			frappe.rename_doc("Drillbit Folder", self.name, self.folder_name + "-" + str(self.folder_id))
			frappe.msgprint(f"Visit the updated folder: <a href=\"/app/drillbit-folder/{self.folder_name}-{str(self.folder_id)}\">Here</a>")
		else:
			frappe.errprint("Error updating folder")


class DrillbitFolder(Document):
	def autoname(self):
		handle_folder_create(self)

	def on_update(self):
		if self.is_new() == False:
			return
		else:
			handle_folder_edit(self)
