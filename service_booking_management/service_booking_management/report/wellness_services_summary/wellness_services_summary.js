// Copyright (c) 2025, sessions.Abhimanyu and contributors
// For license information, please see license.txt

frappe.query_reports["Wellness Services Summary"] = {
	filters: [
		{
			fieldname: "service_type",
			label: "Service Type",
			fieldtype: "Select",
			options: ["", "Therapy", "Spa", "Others"],
		},
		{
			fieldname: "workflow_state",
			label: "Status",
			fieldtype: "Select",
			options: ["", "Requested", "Approved", "Completed"],
		},
	],
	onload: function (report) {
		report.page.add_inner_button("New Service Booking", function () {
			frappe.set_route("form", "Service Booking", "new");
		});
	},
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "workflow_state") {
			const colorMap = {
				Requested: "orange",
				Approved: "blue",
				Completed: "green",
			};

			const color = colorMap[data.workflow_state] || "gray";

			return `<span class="indicator-pill ${color} no-indicator-dot ellipsis">${data.workflow_state}</span>`;
		}

		return value;
	},
};
