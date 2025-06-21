import frappe
from frappe.utils import format_datetime


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        {
            "label": "Service Booking ID",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Service Booking",
            "width": 200
        },
        {
            "label": "Customer",
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Service",
            "fieldname": "service_type",
            "fieldtype": "Data",
            "width": 150
        }
    ]

    # Only include 'Other Services' column if filter is not applied or is set to "Others"
    if not filters or filters.get("service_type") == "Others":
        columns.append({
            "label": "Other Services",
            "fieldname": "other_services",
            "fieldtype": "Small Text",
            "width": 350
        })

    columns.extend([
        {
            "label": "Status",
            "fieldname": "workflow_state",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Date/Time",
            "fieldname": "preferred_datetime",
            "fieldtype": "Data",
            "width": 180
        }
    ])

    return columns


def get_data(filters):
    fields = ["name", "customer_name", "service_type",
              "workflow_state", "preferred_datetime"]

    # Only fetch 'other_services' if needed
    if not filters or filters.get("service_type") == "Others":
        fields.append("other_services")

    service_booked_records = frappe.get_all(
        "Service Booking",
        fields=fields,
        filters=filters
    )

    for row in service_booked_records:
        if row.get("preferred_datetime"):
            row["preferred_datetime"] = format_datetime(
                # e.g. 3, Jul, 2025 | 12:30
                row["preferred_datetime"], "d, MMM, yyyy | hh:mm"
            )

    return service_booked_records
