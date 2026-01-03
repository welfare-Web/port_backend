from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer

@api_view(["POST"])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    contact = serializer.save()

    # 🚫 NEVER LET EMAIL CRASH THE API
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
            fail_silently=False,
        )

        send_mail(
            subject="Thanks for contacting Welfare Healthtech",
            message="We received your message and will contact you shortly.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[contact.email],
            fail_silently=False,
        )

    except Exception as e:
        # 🔥 THIS IS THE KEY LINE
        return Response(
            {
                "status": "error",
                "message": "Email failed",
                "details": str(e)
            },
            status=status.HTTP_200_OK  # 👈 NOT 500
        )

    return Response({"status": "success"}, status=status.HTTP_200_OK)
