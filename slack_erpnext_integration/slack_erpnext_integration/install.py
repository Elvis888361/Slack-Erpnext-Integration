# Copyright (c) 2025, Slack ERPNext Integration and contributors
# For license information, please see license.txt

import frappe


def create_demo_webhook():
	"""Create a demo Slack webhook for testing"""
	if not frappe.db.exists("Slack Webhook URL", "Sales Update Channel"):
		webhook = frappe.get_doc({
			"doctype": "Slack Webhook URL",
			"webhook_name": "Sales Update Channel",
			"webhook_url": "https://hooks.slack.com/services/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",
			"show_document_link": 1
		})
		webhook.insert()
		frappe.db.commit()
		return webhook.name
	return "Sales Update Channel"


def create_demo_notification():
	"""Create a demo Slack notification for Sales Order"""
	if not frappe.db.exists("Notification", "Slack - New Sales Order"):
		notification = frappe.get_doc({
			"doctype": "Notification",
			"name": "Slack - New Sales Order",
			"subject": "New Sales Order: {{ doc.name }}",
			"document_type": "Sales Order",
			"event": "New",
			"enabled": 1,
			"channel": "Slack",
			"slack_webhook_url": "Sales Update Channel",
			"message": """🎉 *New Sales Order Created!*

*Order:* {{ doc.name }}
*Customer:* {{ doc.customer }}
*Total Amount:* {{ doc.currency }} {{ doc.grand_total }}
*Status:* {{ doc.status }}

{% if doc.delivery_date %}
*Expected Delivery:* {{ doc.delivery_date }}
{% endif %}

_This notification was sent via Slack ERPNext Integration_"""
		})
		notification.insert()
		frappe.db.commit()
		return notification.name
	return "Slack - New Sales Order"
