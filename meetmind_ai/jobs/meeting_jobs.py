import os
import frappe

from meetmind_ai.constants.status import MeetingStatus
from meetmind_ai.services.audio_service import extract_audio_from_video
from meetmind_ai.ai.transcription_service import transcribe_audio
from meetmind_ai.ai.summary_service import generate_summary


def publish_status(meeting_doc, status):

    meeting_doc.db_set(
        "status",
        status
    )

    frappe.publish_realtime(
        event="meeting_status_update",
        message={
            "meeting": meeting_doc.name,
            "status": status
        },
        user=meeting_doc.owner
    )


def process_meeting(meeting_name):

    meeting_doc = frappe.get_doc(
        "Meeting",
        meeting_name
    )

    try:

        publish_status(
            meeting_doc,
            MeetingStatus.TRANSCRIBING
        )

        file_url = meeting_doc.uploaded_file

        file_path = frappe.get_site_path(
            file_url.replace(
                "/private/files/",
                "private/files/"
            )
        )

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension in [".mp3", ".wav"]:

            audio_path = file_path

        else:

            audio_path = extract_audio_from_video(
                file_path
            )

        transcript = transcribe_audio(
            audio_path
        )

        meeting_doc.db_set(
            "transcript",
            transcript
        )

        publish_status(
            meeting_doc,
            MeetingStatus.SUMMARIZING
        )

        summary = generate_summary(
            transcript
        )

        meeting_doc.db_set(
            "summary",
            summary
        )

        publish_status(
            meeting_doc,
            MeetingStatus.COMPLETED
        )

    except Exception as e:

        publish_status(
            meeting_doc,
            MeetingStatus.FAILED
        )

        meeting_doc.db_set(
            "error_log",
            str(e)
        )

        frappe.log_error(
            title=f"{meeting_doc.name} Processing Failed",
            message=frappe.get_traceback()
        )