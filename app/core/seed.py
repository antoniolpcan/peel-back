from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.colors import Color 

DEFAULT_COLORS = [
    {"name": "yellow", "hex_code": "#FEF08A"},
    {"name": "pink",   "hex_code": "#FBCFE8"},
    {"name": "blue",   "hex_code": "#BAE6FD"},
    {"name": "green",  "hex_code": "#BBF7D0"},
    {"name": "purple", "hex_code": "#E9D5FF"},
    {"name": "orange", "hex_code": "#FED7AA"},
]

async def seed_colors():
    async with SessionLocal() as db:
        try:
            result = await db.execute(select(Color))
            existing_colors = {color.name: color for color in result.scalars().all()}
            for color_data in DEFAULT_COLORS:
                name = color_data["name"]
                new_hex = color_data["hex_code"]
                if name in existing_colors:
                    existing_colors[name].hex_code = new_hex
                else:
                    db_color = Color(name=name, hex_code=new_hex)
                    db.add(db_color)
            await db.commit()
        except Exception as e:
            print(f"Erro ao popular o banco: {e}")
            await db.rollback()