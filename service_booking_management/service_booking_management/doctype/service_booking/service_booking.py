# Copyright (c) 2025, sessions.Abhimanyu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.email.doctype.email_template.email_template import get_email_template
import requests


class ServiceBooking(Document):

    def on_update(self):

        if self.workflow_state == "Approved":
            self.send_booking_confirmation_email()
            self.push_booking_details_to_webhook()

    def send_booking_confirmation_email(self):
        # Fetching customer's email from the customer's contact
        email = frappe.db.get_value(
            "Customer", self.customer_name, "email_id")

        if not email:
            frappe.log_error(
                f"Customer '{self.customer_name}' has no email_id set.")
            frappe.throw(
                f"Please set email_id for sending confirmation email to customer {self.customer_name}")
            return

        # Rendering Email Template "Booking Confirmation" and passing dynamic values
        template = get_email_template(
            "Booking Confirmation", self.as_dict())

        frappe.sendmail(
            recipients=email,
            subject=template.get("subject"),
            message=template.get("message"),
            delayed=False
        )
        frappe.msgprint(
            msg="Email Notification Sent Successfully", alert=True, indicator="green")

    def push_booking_details_to_webhook(self):
        payload = {
            "customer_name": self.customer_name,
            "service_type": self.service_type,
            "preferred_datetime": str(self.preferred_datetime),
            "status": self.workflow_state,
            "other_services": self.other_services
        }

        # This can be dynamic aswell it can be fetched from front end by adding a field in front end.
        webhook_url = "https://webhook.site/your-temp-url"

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Webhook Push Failed")
