from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
def contact_form(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        message = request.data.get('message')

        if not name or not email or not message:
            return Response(
                {"status": "error", "message": "Missing required fields"},
                status=400
            )

        # =========================
        # ADMIN EMAIL (CLEAN HTML)
        # =========================
        admin_html_message = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0; padding:0; background:#f4f6f8; font-family:Arial, sans-serif;">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td align="center" style="padding:30px 15px;">
                <table width="600" cellpadding="0" cellspacing="0"
                  style="background:#ffffff; border-radius:8px; padding:24px;">
                  
                  <tr>
                    <td style="font-size:20px; font-weight:600; color:#111;">
                      New Contact Form Submission
                    </td>
                  </tr>

                  <tr><td height="16"></td></tr>

                  <tr>
                    <td style="font-size:14px; color:#333; line-height:1.6;">
                      <strong>Name:</strong> {name}<br/>
                      <strong>Email:</strong> {email}<br/>
                      <strong>Phone:</strong> {phone or "Not provided"}
                    </td>
                  </tr>

                  <tr><td height="16"></td></tr>

                  <tr>
                    <td style="font-size:14px; color:#333;">
                      <strong>Message:</strong>
                    </td>
                  </tr>

                  <tr><td height="8"></td></tr>

                  <tr>
                    <td style="font-size:14px; color:#555; background:#f7f7f7;
                      padding:12px; border-radius:6px; line-height:1.6;">
                      {message}
                    </td>
                  </tr>

                  <tr><td height="24"></td></tr>

                  <tr>
                    <td style="font-size:12px; color:#888;">
                      Welfare Healthtech · Contact Notification
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        send_mail(
            subject=f"New Contact Form - {name}",
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            html_message=admin_html_message,
            fail_silently=False,
        )

        # =========================
        # USER EMAIL (CLEAN HTML)
        # =========================
        user_html_message = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0; padding:0; background:#f4f6f8; font-family:Arial, sans-serif;">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td align="center" style="padding:30px 15px;">
                <table width="600" cellpadding="0" cellspacing="0"
                  style="background:#ffffff; border-radius:8px; padding:24px;">
                  
                  <tr>
                    <td style="font-size:20px; font-weight:600; color:#111;">
                      Thanks for contacting Welfare Healthtech
                    </td>
                  </tr>

                  <tr><td height="16"></td></tr>

                  <tr>
                    <td style="font-size:14px; color:#333; line-height:1.6;">
                      Hi <strong>{name}</strong>,<br/><br/>
                      We’ve received your message and our team will contact you shortly.
                    </td>
                  </tr>

                  <tr><td height="16"></td></tr>

                  <tr>
                    <td style="font-size:14px; color:#333;">
                      <strong>Your message:</strong>
                    </td>
                  </tr>

                  <tr><td height="8"></td></tr>

                  <tr>
                    <td style="font-size:14px; color:#555; background:#f7f7f7;
                      padding:12px; border-radius:6px; line-height:1.6;">
                      {message}
                    </td>
                  </tr>

                  <tr><td height="24"></td></tr>

                  <tr>
                    <td style="font-size:14px; color:#333;">
                      Regards,<br/>
                      <strong>Welfare Healthtech Team</strong>
                    </td>
                  </tr>

                  <tr><td height="16"></td></tr>

                  <tr>
                    <td style="font-size:12px; color:#888;">
                      This is an automated email. Please do not reply.
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        send_mail(
            subject="Thanks for contacting Welfare Healthtech",
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=user_html_message,
            fail_silently=False,
        )

        return Response({"status": "success"})

    except Exception as e:
        print("CONTACT FORM ERROR:", e)
        return Response(
            {"status": "error", "message": "Server error"},
            status=500
        )
