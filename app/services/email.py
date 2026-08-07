from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from app.core.email import mail_config
from app.core.config import settings

class EmailService:
    @staticmethod
    async def send_reset_password(email_to: EmailStr, token: str):
        reset_link = f"{settings.APP_URL}/reset-password?token={token}"

        message = MessageSchema(
            subject="Recuperação de Senha",
            recipients=[email_to],
            body=f"""
            <div style="font-family: sans-serif; padding: 20px;">
                <h2>Redefinição de Senha</h2>
                <p>Clique no link abaixo para alterar sua senha:</p>
                <a href="{reset_link}" style="display: inline-block; padding: 10px 15px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 5px;">Redefinir Senha</a>
            </div>
            """,
            subtype=MessageType.html
        )

        fm = FastMail(mail_config)
        await fm.send_message(message)