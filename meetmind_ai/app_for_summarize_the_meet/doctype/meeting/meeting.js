frappe.ui.form.on("Meeting", {

    refresh(frm) {

        if (frm.realtime_event_added) return

        frm.realtime_event_added = true

        frappe.realtime.on(
            "meeting_status_update",
            (data) => {

                if (data.meeting === frm.doc.name) {

                    frm.set_value(
                        "status",
                        data.status
                    )

                    frm.refresh_field(
                        "status"
                    )

                    if (data.status === "Completed") {

                        frm.reload_doc()

                    }

                }

            }
        )

    }

})