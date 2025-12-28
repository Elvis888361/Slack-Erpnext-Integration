# Copyright (c) 2025, Slack ERPNext Integration and contributors
# For license information, please see license.txt

import frappe
import requests
import json


def check_configuration():
	"""Check webhook and notification configuration"""

	# Check webhook
	if not frappe.db.exists("Slack Webhook URL", "Sales Update Channel"):
		return {"success": False, "error": "Webhook 'Sales Update Channel' not found"}

	webhook = frappe.get_doc("Slack Webhook URL", "Sales Update Channel")

	# Check notification
	if not frappe.db.exists("Notification", "Slack - New Sales Order"):
		return {"success": False, "error": "Notification 'Slack - New Sales Order' not found"}

	notification = frappe.get_doc("Notification", "Slack - New Sales Order")

	return {
		"success": True,
		"webhook": {
			"name": webhook.webhook_name,
			"url": webhook.webhook_url[:50] + "...",
			"show_link": webhook.show_document_link
		},
		"notification": {
			"name": notification.name,
			"enabled": notification.enabled,
			"channel": notification.channel,
			"webhook": notification.slack_webhook_url,
			"doctype": notification.document_type,
			"event": notification.event
		}
	}


def send_test_message():
	"""Send a test message directly to Slack using Frappe's built-in function"""
	from frappe.integrations.doctype.slack_webhook_url.slack_webhook_url import send_slack_message

	try:
		result = send_slack_message(
			webhook_url="Sales Update Channel",
			message="🧪 *TEST MESSAGE FROM ERPNEXT*\n\nThis is a test notification to verify your Slack integration is working!\n\n✅ If you see this message, your webhook is configured correctly.",
			reference_doctype="Slack Webhook URL",
			reference_name="Sales Update Channel"
		)

		if result == "success":
			return {
				"success": True,
				"message": "Test message sent successfully! Check your Slack channel.",
				"result": result
			}
		else:
			return {
				"success": False,
				"message": f"Failed to send message. Result: {result}",
				"result": result
			}

	except Exception as e:
		return {
			"success": False,
			"message": "Error sending message",
			"error": str(e)
		}


def test_notification_trigger():
	"""Test if notification can be triggered"""

	notification = frappe.get_doc("Notification", "Slack - New Sales Order")

	# Check if it's enabled
	if not notification.enabled:
		return {
			"success": False,
			"error": "Notification is disabled. Please enable it first."
		}

	# Check channel
	if notification.channel != "Slack":
		return {
			"success": False,
			"error": f"Channel is set to '{notification.channel}', should be 'Slack'"
		}

	# Check webhook link
	if not notification.slack_webhook_url:
		return {
			"success": False,
			"error": "Slack webhook URL is not set in the notification"
		}

	return {
		"success": True,
		"message": "Notification is properly configured",
		"details": {
			"triggers_on": f"{notification.event} - {notification.document_type}",
			"webhook": notification.slack_webhook_url
		}
	}


def get_webhook_url():
	"""Get the webhook URL for debugging"""
	webhook = frappe.get_doc("Slack Webhook URL", "Sales Update Channel")
	return {
		"webhook_name": webhook.webhook_name,
		"webhook_url": webhook.webhook_url
	}


def create_test_sales_order():
	"""Create a test Sales Order to trigger the notification"""

	# Check if customer exists
	if not frappe.db.exists("Customer", "Test Customer"):
		customer = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": "Test Customer",
			"customer_type": "Company",
			"customer_group": "Commercial",
			"territory": "All Territories"
		})
		customer.insert()
		frappe.db.commit()

	# Check if item exists
	if not frappe.db.exists("Item", "Test Item"):
		item = frappe.get_doc({
			"doctype": "Item",
			"item_code": "Test Item",
			"item_name": "Test Item",
			"item_group": "Products",
			"stock_uom": "Nos"
		})
		item.insert()
		frappe.db.commit()

	# Create Sales Order
	so = frappe.get_doc({
		"doctype": "Sales Order",
		"customer": "Test Customer",
		"delivery_date": frappe.utils.add_days(frappe.utils.nowdate(), 7),
		"items": [{
			"item_code": "Test Item",
			"qty": 1,
			"rate": 1000
		}]
	})

	so.insert()
	frappe.db.commit()

	return {
		"success": True,
		"message": f"Test Sales Order created: {so.name}",
		"sales_order": so.name,
		"customer": so.customer,
		"total": so.grand_total
	}

def manually_trigger_notification():
	"""Manually trigger the notification for testing"""
	from frappe.email.doctype.notification.notification import evaluate_alert
	
	# Get the notification
	notification = frappe.get_doc("Notification", "Slack - New Sales Order")
	
	# Get the latest sales order
	so_list = frappe.get_all("Sales Order", limit=1, order_by="creation desc")
	
	if not so_list:
		return {"error": "No Sales Orders found"}
	
	so = frappe.get_doc("Sales Order", so_list[0].name)
	
	try:
		# Manually evaluate and send
		evaluate_alert(so, notification.name, notification.event)
		
		return {
			"success": True,
			"message": f"Notification manually triggered for {so.name}",
			"sales_order": so.name
		}
	except Exception as e:
		frappe.log_error(title="Manual Notification Trigger Error", message=str(e))
		return {
			"success": False,
			"error": str(e),
			"sales_order": so.name
		}
