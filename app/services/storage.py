import cloudinary
import cloudinary.uploader
from PIL import Image
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.media import MediaRepository
from app.core.config import settings
import io
import os

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.CLOUD_API_KEY,
    api_secret=settings.CLOUD_API_SECRET,
    secure=True
)

class StorageService:
    def __init__(self, db_session: AsyncSession):
        self.repository = MediaRepository(db_session)

    async def _otimize(self, file: UploadFile):
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        image.thumbnail((1920, 1920))
        output = io.BytesIO()
        image.save(output, format="WEBP", quality=80)
        output.seek(0)
        return output

    async def upload_and_save(self, file: UploadFile, user_id: str) -> dict:
        try:
            otimized_image = await self._otimize(file)
            original_name, _ = os.path.splitext(file.filename)
            new_file_name = f"{original_name}.webp"

            upload_result = cloudinary.uploader.upload(
                otimized_image.read(),
                folder="uploads",
                format="webp"
            )
            secure_url = upload_result.get("secure_url")
            saved_media = await self.repository.save(
                filename=new_file_name,
                user_id=user_id,
                url=secure_url
            )
            return saved_media.to_dict()
            
        except Exception as e:
            print(f"Erro ao realizar upload de imagem")
            raise e
        