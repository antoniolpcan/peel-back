from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from app.services.storage import StorageService
from app.api.deps import get_storage_service, get_current_user 
from app.models.users import User

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(
        file: UploadFile = File(...), 
        service: StorageService = Depends(get_storage_service),
        current_user: User = Depends(get_current_user)
    ):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem válida.")
    try:
        result = await service.upload_and_save(file, current_user.id)
        return {"message": "Upload realizado com sucesso!", "data": result}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro ao processar o upload."
        )