from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    auth, users, karyawan, kategori_menu, menu,
    meja, pesanan, transaksi, pembayaran, stok_harian
)

app = FastAPI(
    title="RestoApp API",
    description="Restaurant Management System API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(karyawan.router)
app.include_router(kategori_menu.router)
app.include_router(menu.router)
app.include_router(meja.router)
app.include_router(pesanan.router)
app.include_router(transaksi.router)
app.include_router(pembayaran.router)
app.include_router(stok_harian.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to RestoApp API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
