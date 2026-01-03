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

    data = serializer.save()

    try:
        # Email to admin
        send_mail(
            subject="New Contact Message",
            message=f"""
Name: {data.name}
Email: {data.email}
Phone: {data.phone}

Message:
{data.message}
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Email to user
        send_mail(
            subject="We received your message",
            message="Thank you for contacting Welfare Healthtech. We will get back to you shortly.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data.email],
            fail_silently=False,
        )

    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({"status": "success"}, status=status.HTTP_200_OK)
