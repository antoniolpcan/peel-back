from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.colors import Color 

DEFAULT_COLORS = [
    {"name": "yellow", "hex_code": "#FEF9C3"},
    {"name": "blue", "hex_code": "#E0F2FE"},
    {"name": "green", "hex_code": "#DCFCE7"},
    {"name": "pink", "hex_code": "#FCE7F3"},
    {"name": "purple", "hex_code": "#F3E8FF"},
    {"name": "peach", "hex_code": "#FFEDD5"},
    {"name": "gray", "hex_code": "#E2E4E9"},
]

async def seed_colors():
    async with SessionLocal() as db:
        try:
            result = await db.execute(select(Color))
            existing_colors = result.scalars().all()
            if len(existing_colors) == 0:
                for color_data in DEFAULT_COLORS:
                    db_color = Color(name=color_data["name"], hex_code=color_data["hex_code"])
                    db.add(db_color)
                await db.commit()
        except Exception as e:
            print(f"Erro ao popular o banco: {e}")
            await db.rollback()