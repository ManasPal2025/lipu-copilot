"""Plain-text and HTML copy for consultation email."""

import html
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RenderedEmail:
    purpose: str
    recipient: str
    subject: str
    text: str
    html: str


def project_label(project_type: str) -> str:
    return project_type.replace("_", " ").title()


def format_submitted(submitted_at: datetime) -> str:
    return submitted_at.strftime("%d %B %Y, %H:%M UTC")


def internal_notification(
    *,
    recipient: str,
    name: str,
    email: str,
    phone: str | None,
    city: str,
    project_type: str,
    message: str,
    consultation_id: str,
    lead_id: str,
    submitted_at: datetime,
) -> RenderedEmail:
    label = project_label(project_type)
    submitted = format_submitted(submitted_at)
    phone_line = f"Phone: {phone}\n" if phone else ""
    text = (
        "New Consultation Request\n\n"
        "Customer\n"
        "--------\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"{phone_line}"
        f"City: {city}\n"
        f"Project Type: {label}\n\n"
        "Message\n"
        "-------\n"
        f"{message}\n\n"
        "Reference\n"
        "---------\n"
        f"Consultation ID: {consultation_id}\n"
        f"Lead ID: {lead_id}\n"
        f"Submitted: {submitted}\n"
    )
    phone_row = _row("Phone", phone) if phone else ""
    body = (
        _row("Name", name)
        + _row("Email", email)
        + phone_row
        + _row("City", city)
        + _row("Project type", label)
        + _block("Message", message)
        + _row("Consultation ID", consultation_id)
        + _row("Lead ID", lead_id)
        + _row("Submitted", submitted)
    )
    return RenderedEmail(
        purpose="internal_notification",
        recipient=recipient,
        subject=f"New Consultation Request — {name}",
        text=text,
        html=_document("New Consultation Request", body),
    )


def customer_acknowledgement(
    *,
    recipient: str,
    name: str,
    city: str,
    project_type: str,
    message: str,
    consultation_id: str,
) -> RenderedEmail:
    label = project_label(project_type)
    text = (
        f"Dear {name},\n\n"
        "Thank you. Ecotech has received your consultation request.\n\n"
        "A member of the team will review it and may contact you "
        "using the details you provided.\n\n"
        "Your request\n"
        "------------\n"
        f"City: {city}\n"
        f"Project type: {label}\n"
        f"{message}\n\n"
        f"Reference: {consultation_id}\n\n"
        "Ecotech Window Systems\n"
    )
    body = (
        f"<p>Dear {html.escape(name)},</p>"
        "<p>Thank you. Ecotech has received your consultation request.</p>"
        "<p>A member of the team will review it and may contact you "
        "using the details you provided.</p>"
        + _block("Your request", f"{city}\n{label}\n\n{message}")
        + _row("Reference", consultation_id)
    )
    return RenderedEmail(
        purpose="customer_acknowledgement",
        recipient=recipient,
        subject="We received your Ecotech consultation request",
        text=text,
        html=_document("Ecotech", body),
    )


def _row(label: str, value: str) -> str:
    return (
        "<p style=\"margin:0 0 8px;font-size:15px;line-height:1.5;\">"
        f"<span style=\"color:#78716c;\">{html.escape(label)}</span><br>"
        f"{html.escape(value)}</p>"
    )


def _block(label: str, value: str) -> str:
    return (
        "<p style=\"margin:20px 0 8px;font-size:12px;letter-spacing:0.08em;"
        "text-transform:uppercase;color:#78716c;\">"
        f"{html.escape(label)}</p>"
        "<p style=\"margin:0 0 8px;font-size:15px;line-height:1.6;white-space:pre-wrap;\">"
        f"{html.escape(value)}</p>"
    )


def _document(heading: str, body: str) -> str:
    return (
        "<!DOCTYPE html><html><body style=\"margin:0;padding:24px;background:#f6f4f1;\">"
        "<div style=\"max-width:560px;margin:0 auto;background:#ffffff;padding:32px;"
        "font-family:Georgia,'Times New Roman',serif;color:#1c1917;\">"
        f"<p style=\"margin:0 0 24px;font-size:22px;\">{html.escape(heading)}</p>"
        f"{body}"
        "<p style=\"margin:32px 0 0;font-size:13px;color:#78716c;\">Ecotech Window Systems</p>"
        "</div></body></html>"
    )
