"""Email service for sending password reset emails using Flask-Mail."""

from flask_mail import Mail, Message
from flask import url_for

# Mail instance will be initialized in app.py
mail = None


def init_mail(app):
    """Initialize Flask-Mail with app configuration."""
    global mail
    mail = Mail(app)


def send_password_reset_email(user_email: str, reset_token: str, base_url: str):
    """
    Send password reset email to user.
    
    Args:
        user_email: Recipient email address
        reset_token: Password reset token
        base_url: Base URL of the application (e.g., http://127.0.0.1:5000)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    if mail is None:
        return False, "Email service not configured"
    
    try:
        # Create reset link
        reset_link = f"{base_url}/reset-password/{reset_token}"
        
        # Email subject
        subject = "Password Reset Request - JNTU EduAssist"
        
        # HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                    line-height: 1.6;
                    color: #1d1d1f;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background: #f5f5f7;
                    border: 1px solid #d2d2d7;
                    padding: 40px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 24px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 10px;
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border: 1px solid #d2d2d7;
                }}
                .button {{
                    display: inline-block;
                    background: #2d2d2d;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    text-transform: uppercase;
                    font-size: 12px;
                    font-weight: 600;
                    letter-spacing: 1px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #86868b;
                }}
                .warning {{
                    background: #fef2f2;
                    border-left: 3px solid #ef4444;
                    padding: 15px;
                    margin: 20px 0;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">JNTU EduAssist</div>
                    <p>Educational Platform</p>
                </div>
                
                <div class="content">
                    <h2 style="margin-top: 0;">Password Reset Request</h2>
                    
                    <p>Hello,</p>
                    
                    <p>We received a request to reset your password for your JNTU EduAssist account. Click the button below to reset your password:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">RESET PASSWORD</a>
                    </div>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; background: #f5f5f7; padding: 10px; font-family: monospace; font-size: 12px;">
                        {reset_link}
                    </p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul style="margin: 10px 0;">
                            <li>This link will expire in <strong>1 hour</strong></li>
                            <li>If you didn't request this reset, please ignore this email</li>
                            <li>Never share this link with anyone</li>
                        </ul>
                    </div>
                    
                    <p>If you have any questions, please contact our support team.</p>
                    
                    <p>Best regards,<br>
                    <strong>JNTU EduAssist Team</strong></p>
                </div>
                
                <div class="footer">
                    <p>© 2025 JNTU EduAssist | Educational Platform</p>
                    <p>This is an automated message, please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version (fallback)
        text_body = f"""
        Password Reset Request - JNTU EduAssist
        
        Hello,
        
        We received a request to reset your password for your JNTU EduAssist account.
        
        Click this link to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this reset, please ignore this email.
        
        Best regards,
        JNTU EduAssist Team
        """
        
        # Create message
        msg = Message(
            subject=subject,
            sender=('JNTU EduAssist', mail.default_sender),
            recipients=[user_email],
            body=text_body,
            html=html_body
        )
        
        # Send email
        mail.send(msg)
        
        return True, "Password reset email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
