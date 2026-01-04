# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.mail import send_mail
# from django.conf import settings
# from .serializers import ContactSerializer


# @csrf_exempt
# @api_view(["POST"])
# def contact_api(request):
#     serializer = ContactSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()

#     return Response(
#         {"status": "success"},
#         status=200
#     )




# # @csrf_exempt
# # @api_view(["POST","OPTIONS"])
# # def contact_api(request):
# #     serializer = ContactSerializer(data=request.data)

# #     if not serializer.is_valid():
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #     # ✅ Save contact first (fast, safe)
# #     contact = serializer.save()

# #     # 🚫 NEVER block API for email
# #     try:
# #         send_mail(
# #             subject="New Contact Message",
# #             message=f"""
# # Name: {contact.name}
# # Email: {contact.email}
# # Phone: {contact.phone}

# # Message:
# # {contact.message}
# # """,
# #             from_email=settings.EMAIL_HOST_USER,
# #             recipient_list=[settings.EMAIL_HOST_USER],
# #             fail_silently=True,  # 🔥 CRITICAL
# #         )

# #         send_mail(
# #             subject="Thanks for contacting Welfare Healthtech",
# #             message="We received your message and will contact you shortly.",
# #             from_email=settings.EMAIL_HOST_USER,
# #             recipient_list=[contact.email],
# #             fail_silently=True,  # 🔥 CRITICAL
# #         )

# #     except Exception as e:
# #         # ❌ Do NOT crash API
# #         print("Email error:", e)

# #     # ✅ ALWAYS return success fast
# #     return Response(
# #         {"status": "success"},
# #         status=status.HTTP_200_OK
# #     )

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from .serializers import ContactSerializer


def send_email(to_email, subject, content):
    try:
        message = Mail(
            from_email=("noreply@welfarehealthtech.com", "Welfare Healthtech"),
            to_emails=to_email,
            subject=subject,
            html_content=content,
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)

    except Exception as e:
        print("Email failed:", e)  # never crash API


@csrf_exempt
@api_view(["POST"])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    contact = serializer.save()

    # 1️⃣ Email to CUSTOMER
    send_email(
        to_email=contact.email,
        subject="We received your message",
        content=f"""
        <p>Hi {contact.name},</p>
        <p>Thank you for contacting Welfare Healthtech.</p>
        <p>Our team will get back to you shortly.</p>
        """
    )

    # 2️⃣ Email to ADMIN
    send_email(
        to_email=os.getenv("ADMIN_EMAIL"),
        subject="New Contact Form Submission",
        content=f"""
        <p><b>Name:</b> {contact.name}</p>
        <p><b>Email:</b> {contact.email}</p>
        <p><b>Phone:</b> {contact.phone}</p>
        <p><b>Message:</b><br>{contact.message}</p>
        """
    )

    return Response({"status": "success"}, status=200)





























