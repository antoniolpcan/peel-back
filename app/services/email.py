from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from app.core.email import mail_config
from app.core.config import settings

class EmailService:

    @staticmethod
    async def send_reset_password(email_to: EmailStr, token: str):
        reset_link = f"{settings.APP_URL}/reset-password?token={token}"

        message = MessageSchema(
            subject="Recupere seu acesso ao Peel",
            recipients=[email_to],
            body=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 30px; color: #333333; line-height: 1.6; border: 1px solid #EAEAEA; border-radius: 8px;">
                <h2 style="color: #2C3E50; margin-top: 0;">Redefinição de Senha 🔒</h2>
                <p>Olá,</p>
                <p>Recebemos uma solicitação para redefinir a senha da sua conta no <strong>Peel</strong>. Se foi você, clique no botão abaixo para criar uma nova senha:</p>
                
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{reset_link}" style="display: inline-block; padding: 14px 28px; background-color: #4F46E5; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;">Redefinir Minha Senha</a>
                </div>
                
                <p style="font-size: 14px; color: #555555;">
                    Se o botão não funcionar, copie e cole o link abaixo no seu navegador:
                    <br>
                    <a href="{reset_link}" style="color: #4F46E5; word-break: break-all;">{reset_link}</a>
                </p>
                
                <hr style="border: none; border-top: 1px solid #EEEEEE; margin: 30px 0;">
                
                <p style="font-size: 12px; color: #888888;">
                    <strong>Não solicitou esta alteração?</strong><br>
                    Fique tranquilo(a). Você pode simplesmente ignorar este e-mail. Sua senha não será alterada e sua conta continua segura.
                </p>
                <p style="font-size: 12px; color: #888888;">
                    Abraços,<br><strong>Equipe Peel</strong>
                </p>
            </div>
            """,
            subtype=MessageType.html
        )

        fm = FastMail(mail_config)
        await fm.send_message(message)

    @staticmethod
    async def send_registry_token(email_to: EmailStr, token: str):
        
        message = MessageSchema(
            subject="🎉 Seu código de boas-vindas ao Peel chegou!",
            recipients=[email_to],
            body=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 30px; color: #333333; line-height: 1.6; border: 1px solid #EAEAEA; border-radius: 8px;">
                <h2 style="color: #2C3E50; margin-top: 0;">Boas-vindas ao Peel! 🎉</h2>
                <p>Olá,</p>
                <p>Estamos muito felizes em ter você com a gente. Para finalizar o seu cadastro e acessar a plataforma, utilize o código de verificação abaixo:</p>
                
                <div style="margin: 30px 0; padding: 20px; background-color: #F8F9FA; border-radius: 8px; text-align: center; border: 1px dashed #B0BEC5;">
                    <span style="font-size: 28px; font-weight: bold; letter-spacing: 4px; color: #1976D2;">{token}</span>
                </div>
                
                <p style="font-size: 14px;">Basta copiar e colar este código na tela de confirmação.</p>
                
                <hr style="border: none; border-top: 1px solid #EEEEEE; margin: 30px 0;">
                
                <p style="font-size: 12px; color: #888888;">
                    Se você não solicitou este cadastro, por favor, desconsidere este e-mail. Nenhuma outra ação é necessária.
                </p>
                <p style="font-size: 12px; color: #888888;">
                    Abraços,<br><strong>Equipe Peel</strong>
                </p>
            </div>
            """,
            subtype=MessageType.html
        )

        fm = FastMail(mail_config)
        await fm.send_message(message)