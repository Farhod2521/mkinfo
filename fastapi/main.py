from fastapi import FastAPI, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from models import Base,  Material, MaterialsCustomer
from schemas import MaterialCreate, MaterialResponse, PaginatedResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.future import select  # select ishlatilmoqda
from sqlalchemy import func  # Total natijalar sonini hisoblash uchun


# MySQL ma'lumotlar bazasiga ulanish uchun DATABASE_URL
DATABASE_URL = "mysql+pymysql://{user}:{password}@{host}:{port}/{name}".format(
    user='mkinfouser',
    password='mkinfo123456',
    host='localhost',
    port='3306',
    name='mkinfo'
)




# SQLAlchemy konfiguratsiyasi
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)  # Pool parametrlarini qo'shish
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# OAuth2PasswordBearer instance for security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI ilovasini yaratish
app = FastAPI(
    title="KLASSIFIKATOR",
    description="This is a project for managing materials with FastAPI.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "http://yourwebsite.com",
        "email": "yourname@domain.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "https://backend-market.tmsiti.uz",  # Sizning veb-saytingiz yoki kerakli domenlar
    "http://localhost:3000",
    "https://new-catalog.vercel.app",
    "https://mk.mkinfo.uz",
    "https://www.mk.mkinfo.uz",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ma'lumotlar bazasidan sessiya olish uchun dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Funksiya: Materialni qidirish

@app.get("/search_material/", response_model=PaginatedResponse)
async def search_material(
    query: str,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),  # Default: 1
    size: int = Query(20, ge=1, le=100)  # Default: 50, Max: 100
):
    # Offset va limitni hisoblash
    offset = (page - 1) * size
    
    # Qidiruv natijalari (sahifalanadi)
    results = db.execute(
        select(Material)
        .filter(Material.material_name.ilike(f"%{query}%"))
        .limit(size)
        .offset(offset)
    ).scalars().all()

    # Umumiy natijalar soni
    total_count = db.execute(
        select(func.count(Material.material_csr_code))  # Umumiy sonini hisoblash
        .filter(Material.material_name.ilike(f"%{query}%"))
    ).scalar()

    if not results:
        raise HTTPException(status_code=404, detail="No materials found with the provided name")
    
    # Sahifalanib qaytgan natijalar
    return {
        "total_count": total_count,  # Jami natijalar soni
        "materials": results,  # Natijalar serialize qilinadi
    }
# Funksiya: Materialni yaratish
@app.post("/create_material/", response_model=MaterialCreate)
async def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    existing_material = db.query(Material).filter(Material.material_csr_code == material.material_csr_code).first()
    existing_material_name = db.query(Material).filter(Material.material_name == material.material_name).first()
    if existing_material:
        raise HTTPException(status_code=400, detail="Bu kod bazada mavjud")
    if existing_material_name:
        csr = existing_material_name.material_csr_code
        raise HTTPException(status_code=400, detail=f"Bu nom bu kod----{csr}----uchun qo'yilgan")

    new_material = Material(
        material_csr_code=material.material_csr_code,
        material_name=material.material_name,
        material_measure=material.material_measure
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

# Funksiya: Material_customer yaratish (faqat login qilgan foydalanuvchi uchun)


@app.post("/create_material_or_customer/")
async def create_material_or_customer(
    material_csr_code: str,
    material_name: str,
    material_measure: str = 'kg',
    customer: str = None,
    db: Session = Depends(get_db)
):
    # Check if material with the same CSR code already exists
    existing_material = db.query(Material).filter(Material.material_csr_code == material_csr_code).first()
    existing_material_name = db.query(Material).filter(Material.material_name == material_name).first()

    if existing_material:
        raise HTTPException(status_code=400, detail="Bu kod bazada mavjud")
    if existing_material_name:
        csr = existing_material_name.material_csr_code
        raise HTTPException(status_code=400, detail=f"Bu nom bu kod----{csr}----uchun qo'yilgan")

    # Agar customer mavjud bo'lsa, faqat Material va MaterialsCustomer yaratilsin
    if customer:
        print("bazaga saqlandi ------------------------------------------------------------------------>")
        # Create a new Material object
        new_material = Material(
            material_csr_code=material_csr_code,
            material_name=material_name,
            material_measure=material_measure
        )
        db.add(new_material)

        # Create and add a MaterialsCustomer object
        new_material_customer = MaterialsCustomer(
            material_csr_code=material_csr_code,
            material_name=material_name,
            material_measure=material_measure,
            customer=customer,
        )
        db.add(new_material_customer)

        # Commit the changes to the database
        db.commit()

        # Refresh objects to get the latest data from the database
        db.refresh(new_material)
        db.refresh(new_material_customer)

        return {"message": "Material and customer successfully added", "material": new_material_customer}

    # Agar customer bo'lmasa, faqat Material yaratilsin
    return {"message": "Material added without customer"}
