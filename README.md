### Slack ERPNext Integration

A comprehensive Slack integration app for ERPNext that enables sending notifications to Slack channels directly from ERPNext's notification system.

## Features

- **Easy Slack Webhook Management**: Create and manage multiple Slack webhook URLs for different channels
- **Seamless Notification Integration**: Use Slack as a notification channel in ERPNext's built-in Notification system
- **Dynamic Configuration**: Easily configure and test Slack webhooks
- **Workspace Integration**: Dedicated workspace for managing all Slack-related settings
- **Test Functionality**: Send test messages to verify webhook configurations

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench --site [your-site-name] install-app slack_erpnext_integration
```

## Setup Guide

### Step 1: Create a Slack App

1. Go to [Slack API](https://api.slack.com/apps) and click "Create New App"
2. Choose "From scratch"
3. Enter an App Name (e.g., "ERPNext Notifications")
4. Select your Slack Workspace
5. Click "Create App"

### Step 2: Enable Incoming Webhooks

1. In your Slack App settings, go to "Features" > "Incoming Webhooks"
2. Toggle "Activate Incoming Webhooks" to **On**
3. Scroll down and click "Add New Webhook to Workspace"
4. Select the channel where you want notifications to be sent
5. Click "Allow"
6. Copy the Webhook URL (it should look like: `https://hooks.slack.com/services/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`)

### Step 3: Configure in ERPNext

1. Log in to your ERPNext instance
2. Go to "Slack Integration" workspace (or search for "Slack Webhook URL")
3. Click "New" to create a new Slack Webhook URL
4. Enter:
   - **Webhook Name**: A friendly name for this webhook (e.g., "Sales Channel")
   - **Webhook URL**: Paste the webhook URL from Step 2
   - **Show Document Link**: Check this to include a link to the document in Slack messages
5. Save the webhook

### Step 4: Create Slack Notifications

1. Go to "Notification" list (Setup > Notifications or search for "Notification")
2. Click "New" to create a new notification
3. Configure the notification:
   - **Subject**: Enter a subject for your notification
   - **Document Type**: Select the DocType you want to monitor (e.g., "Sales Order")
   - **Send Alert On**: Choose when to send (e.g., "New", "Save", "Submit")
   - **Channel**: Select **"Slack"** from the dropdown
   - **Slack Channel**: Select the webhook you created in Step 3
   - **Message**: Enter your message template (supports Jinja2)
4. Save and enable the notification

### Step 5: Test Your Integration

Your Slack notifications are now configured! When the specified event occurs on the selected DocType, a notification will be sent to your Slack channel.

## Example Notification Message

```jinja
New Sales Order Created!

Order: {{ doc.name }}
Customer: {{ doc.customer }}
Total: {{ doc.grand_total }}

{% if doc.delivery_date %}
Expected Delivery: {{ doc.delivery_date }}
{% endif %}
```

## Troubleshooting

- **Messages not appearing in Slack**: Check that the webhook URL is correct and the webhook is enabled
- **Permission errors**: Ensure your user role has access to create/modify Slack Webhook URLs and Notifications
- **Invalid webhook**: Verify the webhook URL starts with `https://hooks.slack.com/`

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/slack_erpnext_integration
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
