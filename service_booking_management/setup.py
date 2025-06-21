import frappe

# After migrate hooks will create new Email Template at the first time if it not created
def execute():
    template_name = "Booking Confirmation"

    # Check if it already exists
    if frappe.db.exists("Email Template", template_name):
        return

    # Create the Email Template
    template = frappe.new_doc("Email Template")
    template.name = template_name
    template.use_html = 1
    template.subject = "Your Booking Confirmation with Wellness Center"
    template.response_html = """Hi {{ customer_name }},<br><br>

Your <strong>
{% if service_type == "Others" and other_services %}
    {{ other_services }}
{% else %}
    {{ service_type }}
{% endif %}
</strong> booking is confirmed for <strong>{{ frappe.utils.format_datetime(preferred_datetime, "d, MMM, yyyy | hh:mm") }}</strong>.<br><br>

We look forward to seeing you soon!<br><br>

Regards,<br>
Wellness Center Team
"""

    template.insert()
    frappe.db.commit()