"""
Email Service
Handles email sending for verification, password reset, and notifications
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service with SMTP backend"""
    
    def __init__(self):
        self.smtp_host = getattr(settings, 'SMTP_HOST', '')
        self.smtp_port = getattr(settings, 'SMTP_PORT', 587)
        self.smtp_username = getattr(settings, 'SMTP_USERNAME', '')
        self.smtp_password = getattr(settings, 'SMTP_PASSWORD', '')
        self.smtp_from_email = getattr(settings, 'SMTP_FROM_EMAIL', 'noreply@medinova.ai')
        self.smtp_from_name = getattr(settings, 'SMTP_FROM_NAME', 'MediNova AI')
        self.enabled = all([self.smtp_host, self.smtp_username, self.smtp_password])
        
        if not self.enabled:
            logger.warning(
                "Email service not configured. Set SMTP_HOST, SMTP_USERNAME, "
                "and SMTP_PASSWORD in environment variables. "
                "Emails will be logged but not sent."
            )
        else:
            logger.info(f"Email service configured with SMTP host: {self.smtp_host}")
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email via SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text fallback (optional)
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.smtp_from_name} <{self.smtp_from_email}>"
            message['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                message.attach(part1)
            
            part2 = MIMEText(html_content, 'html')
            message.attach(part2)
            
            if not self.enabled:
                # Development mode - log email instead of sending
                logger.info(
                    f"[DEV MODE] Email not sent (SMTP not configured)\n"
                    f"To: {to_email}\n"
                    f"Subject: {subject}\n"
                    f"Content: {text_content or html_content[:200]}"
                )
                return False  # Indicate email was not actually delivered
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    async def send_verification_email(
        self,
        to_email: str,
        verification_token: str,
        user_name: str
    ) -> bool:
        """Send email verification link"""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        
        subject = "Verify Your MediNova Account"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4F46E5; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #4F46E5; 
                          color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to MediNova AI</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name},</h2>
                    <p>Thank you for registering with MediNova AI. Please verify your email address to complete your registration.</p>
                    <p style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </p>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #4F46E5;">{verification_url}</p>
                    <p><strong>This link will expire in 24 hours.</strong></p>
                    <p>If you didn't create an account with MediNova, you can safely ignore this email.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 MediNova AI. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to MediNova AI
        
        Hi {user_name},
        
        Thank you for registering with MediNova AI. Please verify your email address by clicking the link below:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account with MediNova, you can safely ignore this email.
        
        © 2026 MediNova AI. All rights reserved.
        """
        
        return await self.send_email(to_email, subject, html_content, text_content)
    
    async def send_password_reset_email(
        self,
        to_email: str,
        reset_token: str,
        user_name: str
    ) -> bool:
        """Send password reset link"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        subject = "Reset Your MediNova Password"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #DC2626; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #DC2626; 
                          color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .warning {{ background: #FEF2F2; border-left: 4px solid #DC2626; padding: 10px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name},</h2>
                    <p>We received a request to reset your MediNova password.</p>
                    <p style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </p>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #DC2626;">{reset_url}</p>
                    <p><strong>This link will expire in 1 hour.</strong></p>
                    <div class="warning">
                        <p><strong>Security Notice:</strong></p>
                        <ul>
                            <li>If you didn't request this password reset, please ignore this email</li>
                            <li>Never share this link with anyone</li>
                            <li>MediNova will never ask for your password via email</li>
                        </ul>
                    </div>
                </div>
                <div class="footer">
                    <p>&copy; 2026 MediNova AI. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset Request
        
        Hi {user_name},
        
        We received a request to reset your MediNova password. Click the link below to reset your password:
        
        {reset_url}
        
        This link will expire in 1 hour.
        
        SECURITY NOTICE:
        - If you didn't request this password reset, please ignore this email
        - Never share this link with anyone
        - MediNova will never ask for your password via email
        
        © 2026 MediNova AI. All rights reserved.
        """
        
        return await self.send_email(to_email, subject, html_content, text_content)


# Global email service instance
email_service = EmailService()
