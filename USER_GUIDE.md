# Slack ERPNext Integration - User Guide

Welcome to the Slack ERPNext Integration! This guide will help you set up and use Slack notifications in your ERPNext system.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setting Up Slack App](#setting-up-slack-app)
4. [Configuring ERPNext](#configuring-erpnext)
5. [Creating Notifications](#creating-notifications)
6. [Testing Your Setup](#testing-your-setup)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

## Overview

The Slack ERPNext Integration allows you to send real-time notifications from ERPNext to your Slack channels. This is useful for:
- Alerting your team about new sales orders
- Notifying about payment receipts
- Monitoring inventory levels
- Tracking project milestones
- And much more!

## Prerequisites

- A Slack workspace (create one at [slack.com](https://slack.com))
- Admin access to your Slack workspace
- ERPNext installation with this app installed
- System Manager role in ERPNext

## Setting Up Slack App

### Step 1: Create a Slack App

1. Visit [Slack API Apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Fill in the details:
   - **App Name**: `ERPNext Notifications` (or any name you prefer)
   - **Pick a workspace**: Select your Slack workspace
5. Click **"Create App"**

### Step 2: Enable Incoming Webhooks

1. In your app settings, navigate to **"Features" → "Incoming Webhooks"**
2. Toggle **"Activate Incoming Webhooks"** to **ON**
3. Scroll down to **"Webhook URLs for Your Workspace"**
4. Click **"Add New Webhook to Workspace"**
5. Select the channel where notifications should be posted
6. Click **"Allow"**
7. **Copy the Webhook URL** - it will look like:
   ```
   https://hooks.slack.com/services/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
   ```

### Step 3: Optional - Customize Your App

You can customize your Slack app:
- **App Icon**: Upload a custom icon (e.g., your company logo)
- **App Name**: Change the display name
- **Description**: Add a description for your app

## Configuring ERPNext

### Step 1: Access Slack Integration Workspace

1. Log in to your ERPNext instance
2. Search for **"Slack Integration"** in the awesome bar (top search)
3. Or navigate to: **Home → Integrations → Slack Integration**

### Step 2: Create a Slack Webhook URL

1. In the Slack Integration workspace, click on **"Slack Webhook URL"**
2. Click **"New"**
3. Fill in the following details:
   - **Webhook Name**: A friendly name (e.g., "Sales Channel", "General Alerts")
   - **Webhook URL**: Paste the URL you copied from Slack
   - **Show Document Link**: Check this to include clickable links to documents
4. Click **"Save"**

You can create multiple webhook URLs for different channels!

## Creating Notifications

### Step 1: Create a New Notification

1. Go to **"Notification"** list (search for it in the awesome bar)
2. Click **"New"**

### Step 2: Configure the Notification

Fill in the following fields:

1. **Basic Information**:
   - **Subject**: Enter a subject line (supports Jinja templates)
     - Example: `New Sales Order: {{ doc.name }}`

2. **Trigger Settings**:
   - **Document Type**: Select which DocType to monitor (e.g., "Sales Order")
   - **Send Alert On**: Choose when to trigger:
     - **New**: When a new document is created
     - **Save**: When a document is saved
     - **Submit**: When a document is submitted
     - **Cancel**: When a document is cancelled
     - **Value Change**: When a specific field changes
     - **Days Before/After**: For date-based alerts

3. **Channel Settings**:
   - **Channel**: Select **"Slack"** from the dropdown
   - **Slack Channel**: Select the webhook you created earlier

4. **Message**:
   - Enter your message using Markdown and Jinja2 templates
   - You can use `{{ doc.fieldname }}` to insert field values

### Step 3: Example Notification Message

Here's a sample message for a Sales Order notification:

```jinja
🎉 *New Sales Order Created!*

*Order Number:* {{ doc.name }}
*Customer:* {{ doc.customer }}
*Total Amount:* {{ doc.currency }} {{ doc.grand_total }}
*Status:* {{ doc.status }}

{% if doc.delivery_date %}
*Expected Delivery:* {{ doc.delivery_date }}
{% endif %}

{% if doc.sales_team %}
*Sales Team:*
{% for member in doc.sales_team %}
  • {{ member.sales_person }}
{% endfor %}
{% endif %}

_Notification sent from ERPNext via Slack Integration_
```

### Step 4: Advanced Options (Optional)

- **Condition**: Add a Python expression to filter when notifications are sent
  - Example: `doc.grand_total > 10000` (only for orders over 10,000)

- **Recipients**: For email notifications (not applicable for Slack)

- **Set Property After Alert**: Automatically update a field after sending

### Step 5: Save and Enable

1. Click **"Save"**
2. Make sure **"Enabled"** is checked
3. Your notification is now active!

## Testing Your Setup

### Method 1: Create a Test Document

1. Create a new document of the type you configured (e.g., Sales Order)
2. Fill in the required fields
3. Save or Submit (depending on your trigger)
4. Check your Slack channel - you should see the notification!

### Method 2: Use the Test Function

If you have the utility functions enabled:

```python
# From ERPNext Console
from slack_erpnext_integration.slack_erpnext_integration.utils import test_slack_webhook

test_slack_webhook("Your Webhook Name")
```

## Advanced Usage

### Multiple Channels

You can create multiple webhook URLs for different purposes:
- **Sales Channel**: For sales-related notifications
- **Support Channel**: For customer support tickets
- **Inventory Channel**: For stock alerts
- **General Channel**: For general updates

### Custom Conditions

Use conditions to fine-tune when notifications are sent:

```python
# Only for high-value orders
doc.grand_total > 50000

# Only for specific customer groups
doc.customer_group == "VIP Customers"

# Only during business hours
import datetime
datetime.datetime.now().hour >= 9 and datetime.datetime.now().hour <= 18

# Only for specific status
doc.status in ["Pending", "Overdue"]
```

### Rich Formatting

Use Slack's markdown for rich messages:

```markdown
*Bold text*
_Italic text_
~Strikethrough~
`code`
```code block```

• Bullet points
1. Numbered lists

> Blockquote
```

### Document Links

When "Show Document Link" is enabled, Slack will include a button to view the document in ERPNext. This makes it easy for your team to quickly access the relevant information.

## Troubleshooting

### Issue: Notifications Not Appearing in Slack

**Possible Causes:**
1. **Webhook URL is incorrect**
   - Solution: Verify the webhook URL in ERPNext matches the one from Slack

2. **Webhook is not enabled**
   - Solution: Check that the Slack Webhook URL document has "Enabled" checked

3. **Notification is disabled**
   - Solution: Ensure the Notification document has "Enabled" checked

4. **Trigger condition not met**
   - Solution: Review your event type and condition settings

### Issue: Permission Denied

**Cause:** Your user doesn't have access to create/modify notifications

**Solution:**
- Contact your System Manager
- Ensure you have the "System Manager" role

### Issue: Invalid Webhook URL Error

**Cause:** The webhook URL doesn't start with `https://hooks.slack.com/`

**Solution:**
- Copy the complete webhook URL from Slack
- Make sure you didn't copy any extra spaces or characters

### Issue: Template Errors

**Cause:** Invalid Jinja2 syntax in your message

**Solution:**
- Check your template syntax
- Make sure all `{{ }}` and `{% %}` tags are properly closed
- Verify field names are correct (use "View Properties" button)

### Issue: Slack App Not Posting to Channel

**Cause:** The Slack app wasn't granted permission to post to the channel

**Solution:**
1. Go back to your Slack App settings
2. Remove and re-add the webhook URL
3. Make sure to select the correct channel and authorize it

## Tips and Best Tricks

### 1. Test First
Always test your notifications with a test document before enabling them in production.

### 2. Use Conditions
Use conditions to avoid spam and only send relevant notifications.

### 3. Keep Messages Concise
Slack works best with concise, actionable messages. Include only the most important information.

### 4. Use Emojis
Emojis make notifications more visible and easier to scan:
- ✅ for success
- ⚠️ for warnings
- 🎉 for celebrations
- 📊 for reports

### 5. Set Up Multiple Channels
Create different channels for different types of notifications to keep things organized.

### 6. Monitor Slack Activity
Keep an eye on your Slack channels to ensure notifications are working as expected.

### 7. Document Your Setup
Keep a record of which notifications you've set up and for what purpose.

## Need Help?

If you encounter issues not covered in this guide:

1. Check the ERPNext logs: `bench --site [sitename] logs`
2. Check Frappe/ERPNext forums
3. Review Slack webhook documentation
4. Contact your system administrator

## Next Steps

Now that you have Slack notifications set up, consider:

- Creating notifications for other important DocTypes
- Setting up different channels for different departments
- Using conditions to create smart, context-aware notifications
- Training your team on how to interpret and act on notifications

Happy notifying! 🚀
