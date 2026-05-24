# Copyright (c) 2026, anirudhra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from meetmind_ai.constants.status import MeetingStatus
from meetmind_ai.jobs.meeting_jobs import process_meeting


class Meeting(Document):
	def after_insert(self):
		self.db_set("status", MeetingStatus.QUEUED)

		frappe.enqueue(
			process_meeting,
			queue = "default",
			timeout = 600,
			meeting_name = self.name,
			enqueue_after_commit = True
		)
