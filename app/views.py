from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer

@csrf_exempt
@api_view(["POST","OPTIONS"])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Save contact first (fast, safe)
    contact = serializer.save()

    # 🚫 NEVER block API for email
    try:
        send_mail(
            subject="New Contact Message",
            message=f"""
Name: {contact.name}
Email: {contact.email}
Phone: {contact.phone}

Message:
{contact.message}
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,  # 🔥 CRITICAL
        )

        send_mail(
            subject="Thanks for contacting Welfare Healthtech",
            message="We received your message and will contact you shortly.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[contact.email],
            fail_silently=True,  # 🔥 CRITICAL
        )

    except Exception as e:
        # ❌ Do NOT crash API
        print("Email error:", e)

    # ✅ ALWAYS return success fast
    return Response(
        {"status": "success"},
        status=status.HTTP_200_OK
    )


