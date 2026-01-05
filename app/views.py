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


def send_template_email(to_email, template_id, data):
    try:
        message = Mail(
            from_email="tlepubwelfare@gmail.com",  # VERIFIED sender
            to_emails=to_email,
        )

        message.template_id = template_id
        message.dynamic_template_data = data

        sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        response = sg.send(message)

        print("SendGrid status:", response.status_code)

    except Exception as e:
        print("Email failed:", e)
  # never crash API


@csrf_exempt
@api_view(["POST"])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    contact = serializer.save()

    # 1️⃣ CUSTOMER EMAIL
    send_template_email(
        to_email=contact.email,
        template_id=os.getenv("SENDGRID_CUSTOMER_TEMPLATE_ID"),
        data={
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
        }
    )

    # 2️⃣ ADMIN EMAIL
    send_template_email(
        to_email=os.getenv("ADMIN_EMAIL"),
        template_id=os.getenv("SENDGRID_ADMIN_TEMPLATE_ID"),
        data={
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "message": contact.message,
        }
    )

    return Response({"status": "success"}, status=200)

































