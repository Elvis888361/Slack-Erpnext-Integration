# Slack ERPNext Integration - Quick Start Guide

Get up and running with Slack notifications in 5 minutes!

## 🚀 Quick Setup (5 Steps)

### 1️⃣ Create Slack Webhook (2 minutes)

1. Go to https://api.slack.com/apps → Create New App
2. Choose "From scratch" → Name it "ERPNext Notifications"
3. Go to "Incoming Webhooks" → Toggle ON
4. Click "Add New Webhook to Workspace"
5. Select channel → Copy the webhook URL

### 2️⃣ Add Webhook to ERPNext (1 minute)

1. In ERPNext, search for "Slack Webhook URL"
2. Click "New"
3. Paste the webhook URL
4. Give it a name (e.g., "Sales Channel")
5. Save

### 3️⃣ Create Notification (2 minutes)

1. Search for "Notification" → Click "New"
2. Set:
   - **Subject**: `New Order: {{ doc.name }}`
   - **Document Type**: Sales Order
   - **Send Alert On**: New
   - **Channel**: Slack
   - **Slack Channel**: Select your webhook
   - **Message**: Enter your message
3. Check "Enabled" → Save

### 4️⃣ Test It!

Create a new Sales Order and check your Slack channel!

### 5️⃣ Customize

Edit the message to include the fields you need:
- `{{ doc.customer }}` - Customer name
- `{{ doc.grand_total }}` - Total amount
- `{{ doc.status }}` - Order status

---

## 📝 Sample Message Templates

### Sales Order
```markdown
🎉 New Sales Order!

Order: {{ doc.name }}
Customer: {{ doc.customer }}
Amount: {{ doc.currency }} {{ doc.grand_total }}
```

### Payment Entry
```markdown
💰 Payment Received!

Amount: {{ doc.paid_amount }} {{ doc.paid_to_account_currency }}
From: {{ doc.party_name }}
Reference: {{ doc.reference_no }}
```

### Support Ticket
```markdown
🎫 New Support Ticket

Ticket: {{ doc.name }}
Subject: {{ doc.subject }}
Priority: {{ doc.priority }}
Raised By: {{ doc.raised_by }}
```

### Stock Alert
```markdown
⚠️ Low Stock Alert!

Item: {{ doc.item_name }}
Warehouse: {{ doc.warehouse }}
Actual Qty: {{ doc.actual_qty }}
```

---

## 🎯 Common Use Cases

### 1. Sales Notifications
- **DocType**: Sales Order
- **Event**: New / Submit
- **Channel**: #sales

### 2. Payment Alerts
- **DocType**: Payment Entry
- **Event**: Submit
- **Channel**: #finance

### 3. Support Tickets
- **DocType**: Issue
- **Event**: New
- **Channel**: #support

### 4. Inventory Alerts
- **DocType**: Stock Entry
- **Event**: Submit
- **Condition**: `doc.stock_entry_type == "Material Issue"`
- **Channel**: #warehouse

---

## 🔧 Pro Tips

### Use Conditions
Only notify for important events:
```python
doc.grand_total > 10000  # Only big orders
doc.priority == "High"   # Only urgent tickets
```

### Add Emojis
Make notifications stand out:
- 🎉 New order
- ✅ Completed
- ⚠️ Warning
- 💰 Payment
- 📦 Shipment

### Multiple Channels
Create different webhooks for:
- Sales team → #sales
- Finance team → #finance
- Management → #executive-updates

### Format with Markdown
```markdown
*Bold*
_Italic_
`Code`
> Quote
• Lists
```

---

## ⚡ Troubleshooting

| Problem | Solution |
|---------|----------|
| No notifications | Check "Enabled" is checked |
| Wrong channel | Verify webhook URL |
| Template error | Check field names exist |
| Permission denied | Need System Manager role |

---

## 📚 More Information

- Full guide: See [USER_GUIDE.md](USER_GUIDE.md)
- Jinja templates: https://jinja.palletsprojects.com/
- Slack formatting: https://api.slack.com/reference/surfaces/formatting

---

## 🎓 Your Webhook URL

Your webhook was created! Here's what you need:

```
Webhook Name: Sales Update Channel
Webhook URL: https://hooks.slack.com/services/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
```

A sample notification "Slack - New Sales Order" has been created for you!

---

**Need help?** Check the [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions.

**Ready to go?** Start creating notifications! 🚀
