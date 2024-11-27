from pydantic import BaseModel

class MaterialCreate(BaseModel):
    material_csr_code: str
    material_name: str
    material_measure: str

    class Config:
        orm_mode = True




# Material uchun Pydantic model
class MaterialResponse(BaseModel):
    material_csr_code: str
    material_name: str
    material_measure: str

    class Config:
        orm_mode = True  # SQLAlchemy obyektlarini serialize qilishga imkon beradi

# Javob modeli
class PaginatedResponse(BaseModel):
    total_count: int
    materials: list[MaterialResponse]