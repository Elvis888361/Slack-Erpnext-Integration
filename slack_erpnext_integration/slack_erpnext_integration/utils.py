# Copyright (c) 2025, Slack ERPNext Integration and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def create_slack_webhook(webhook_name, webhook_url, show_document_link=1):
	"""Helper function to create a Slack Webhook URL"""
	if frappe.db.exists("Slack Webhook URL", webhook_name):
		frappe.throw(_("A webhook with this name already exists"))

	doc = frappe.get_doc({
		"doctype": "Slack Webhook URL",
		"webhook_name": webhook_name,
		"webhook_url": webhook_url,
		"show_document_link": show_document_link
	})
	doc.insert()
	frappe.db.commit()

	return doc.name


@frappe.whitelist()
def get_slack_webhooks():
	"""Get all Slack Webhook URLs"""
	return frappe.get_all(
		"Slack Webhook URL",
		fields=["name", "webhook_name", "webhook_url", "show_document_link"],
		order_by="creation desc"
	)


@frappe.whitelist()
def test_slack_webhook(webhook_name):
	"""Send a test message to verify webhook configuration"""
	from frappe.integrations.doctype.slack_webhook_url.slack_webhook_url import send_slack_message

	test_message = "Hello from ERPNext! This is a test message from your Slack integration."

	try:
		result = send_slack_message(
			webhook_url=webhook_name,
			message=test_message,
			reference_doctype="Slack Webhook URL",
			reference_name=webhook_name
		)

		if result == "success":
			frappe.msgprint(_("Test message sent successfully to Slack!"), indicator="green")
		else:
			frappe.msgprint(_("Failed to send test message. Please check the webhook URL."), indicator="red")

	except Exception as e:
		frappe.log_error(title="Slack Test Error", message=str(e))
		frappe.throw(_("Failed to send test message: {0}").format(str(e)))
