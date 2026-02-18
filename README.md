# RestoApp - Restaurant Management System

Aplikasi manajemen restoran lengkap dengan backend FastAPI dan frontend Vue.js yang responsive dan siap dikonversi ke Ionic Vue untuk aplikasi mobile.

## 🚀 Fitur

### CRUD Operations
- **Menu** - Kelola menu makanan dan minuman
- **Kategori Menu** - Organisasi menu berdasarkan kategori
- **Karyawan** - Manajemen data karyawan
- **User** - Sistem pengguna dengan role-based access
- **Meja** - Manajemen meja restoran
- **Transaksi** - Pencatatan transaksi penjualan
- **Pesanan** - Sistem pemesanan (satu pesanan bisa memiliki multiple item)
- **Detail Pesanan** - Detail item dalam pesanan
- **Pembayaran** - Sistem pembayaran dengan berbagai metode
- **Update Stok Harian** - Manajemen stok harian menu

### Role-Based Access Control
- **Admin** - Full access ke semua fitur
- **Manager** - Access ke manajemen Menu, Kategori, Karyawan, User
- **Kasir** - Handle Transaksi, Pesanan, Meja, dan Update Stok
- **Pramusaji** - Handle Pesanan, Meja, dan Update Stok

## 📁 Struktur Proyek

```
RestoApp/
├── backend/                 # FastAPI Backend
│   ├── alembic/            # Database migrations
│   │   ├── versions/       # Migration files
│   │   └── env.py
│   ├── app/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── auth.py         # Authentication logic
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database connection
│   │   └── main.py         # FastAPI application
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/               # Vue.js Frontend
    ├── src/
    │   ├── assets/        # CSS and static assets
    │   ├── components/    # Reusable components
    │   ├── layouts/       # Layout components
    │   ├── router/        # Vue Router
    │   ├── services/      # API services
    │   ├── stores/        # Pinia stores
    │   ├── views/         # Page components
    │   ├── App.vue
    │   └── main.js
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── .env.example
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database (via Supabase)
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Bcrypt** - Password hashing
- **JWT** - Authentication tokens

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Build tool
- **Pinia** - State management
- **Vue Router** - Routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Vue Toastification** - Toast notifications

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (Supabase account)
- Git

## 🔧 Setup Instructions

### 1. Backend Setup

#### a. Navigate to backend directory
```bash
cd backend
```

#### b. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### c. Install dependencies
```bash
pip install -r requirements.txt
```

#### d. Configure environment variables
```bash
# Copy .env.example to .env
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env` file and add your Supabase PostgreSQL connection string:
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Cara mendapatkan Supabase DATABASE_URL:**
1. Login ke https://supabase.com
2. Buat project baru atau gunakan yang sudah ada
3. Pergi ke Settings → Database
4. Copy Connection String (URI) di bagian "Connection string"
5. Replace `[YOUR-PASSWORD]` dengan password database Anda
6. Paste ke file `.env`

#### e. Run database migrations
```bash
alembic upgrade head
```

**Note:** Migration pertama sudah include pembuatan user admin:
- Username: `Nox`
- Password: `HaruYama`
- Role: `admin`

#### f. Start backend server
```bash
uvicorn app.main:app --reload
```

Backend akan berjalan di `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### 2. Frontend Setup

#### a. Navigate to frontend directory
```bash
cd frontend
```

#### b. Install dependencies
```bash
npm install
```

#### c. Configure environment variables
```bash
# Copy .env.example to .env
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

#### d. Start development server
```bash
npm run dev
```

Frontend akan berjalan di `http://localhost:3000`

## 👤 Default Admin User

Setelah menjalankan migrasi, user admin berikut sudah tersedia:

- **Username:** Nox
- **Password:** HaruYama
- **Role:** admin

## 📝 API Endpoints

### Authentication
- `POST /api/auth/login` - Login user

### Users
- `GET /api/users/` - Get all users
- `GET /api/users/{id}` - Get user by ID
- `POST /api/users/` - Create user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Karyawan
- `GET /api/karyawan/` - Get all karyawan
- `GET /api/karyawan/{id}` - Get karyawan by ID
- `POST /api/karyawan/` - Create karyawan
- `PUT /api/karyawan/{id}` - Update karyawan
- `DELETE /api/karyawan/{id}` - Delete karyawan

### Kategori Menu
- `GET /api/kategori-menu/` - Get all categories
- `GET /api/kategori-menu/{id}` - Get category by ID
- `POST /api/kategori-menu/` - Create category
- `PUT /api/kategori-menu/{id}` - Update category
- `DELETE /api/kategori-menu/{id}` - Delete category

### Menu
- `GET /api/menu/` - Get all menu items
- `GET /api/menu/{id}` - Get menu by ID
- `POST /api/menu/` - Create menu
- `PUT /api/menu/{id}` - Update menu
- `DELETE /api/menu/{id}` - Delete menu

### Meja
- `GET /api/meja/` - Get all tables
- `GET /api/meja/{id}` - Get table by ID
- `POST /api/meja/` - Create table
- `PUT /api/meja/{id}` - Update table
- `DELETE /api/meja/{id}` - Delete table

### Pesanan
- `GET /api/pesanan/` - Get all orders
- `GET /api/pesanan/{id}` - Get order by ID
- `POST /api/pesanan/` - Create order with items
- `PUT /api/pesanan/{id}` - Update order
- `DELETE /api/pesanan/{id}` - Delete order

### Transaksi
- `GET /api/transaksi/` - Get all transactions
- `GET /api/transaksi/{id}` - Get transaction by ID
- `POST /api/transaksi/` - Create transaction
- `PUT /api/transaksi/{id}` - Update transaction
- `DELETE /api/transaksi/{id}` - Delete transaction

### Pembayaran
- `GET /api/pembayaran/` - Get all payments
- `GET /api/pembayaran/{id}` - Get payment by ID
- `POST /api/pembayaran/` - Create payment
- `DELETE /api/pembayaran/{id}` - Delete payment

### Stok Harian
- `GET /api/stok-harian/` - Get all daily stocks
- `GET /api/stok-harian/{id}` - Get stock by ID
- `POST /api/stok-harian/` - Create stock record
- `PUT /api/stok-harian/{id}` - Update stock
- `DELETE /api/stok-harian/{id}` - Delete stock

## 🔐 Role Permissions

### Admin
- Full access to all features
- Can create/edit/delete: Users, Karyawan, Menu, Kategori Menu, Meja, Pesanan, Transaksi, Pembayaran, Stok Harian

### Manager
- Can manage: Users, Karyawan, Menu, Kategori Menu
- Can view: Transaksi, Pembayaran
- Cannot delete critical data

### Kasir (Cashier)
- Can manage: Meja, Pesanan, Transaksi, Pembayaran, Stok Harian
- Cannot access: Users, Karyawan, Menu, Kategori Menu management

### Pramusaji (Waiter)
- Can manage: Meja, Pesanan, Stok Harian
- Cannot access: Users, Karyawan, Menu, Kategori Menu, Transaksi, Pembayaran management

## 🎨 Frontend Features

- **Mobile Responsive** - Siap untuk konversi ke Ionic Vue
- **Role-Based UI** - Menu navigation disesuaikan dengan role user
- **Toast Notifications** - Feedback untuk setiap aksi
- **Modal Dialogs** - Untuk create/edit operations
- **Modern Design** - Menggunakan Tailwind CSS
- **State Management** - Pinia stores untuk data management
- **API Integration** - Axios dengan interceptors untuk authentication

## 🔄 Database Migrations

### Create new migration
```bash
cd backend
alembic revision --autogenerate -m "description"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## 📱 Ionic Vue Conversion

Aplikasi sudah didesain dengan mobile-responsive design menggunakan Tailwind CSS. Untuk mengkonversi ke Ionic Vue:

1. Install Ionic CLI
```bash
npm install -g @ionic/cli
```

2. Create Ionic project with Vue
```bash
ionic start restoapp-mobile blank --type=vue
```

3. Copy komponen Vue dari folder `src/` ke project Ionic
4. Install dependencies yang sama
5. Sesuaikan routing dengan Ionic Router
6. Ganti Tailwind components dengan Ionic Components

## 🧪 Testing

### Test Backend
```bash
cd backend
# Install pytest
pip install pytest pytest-asyncio httpx

# Run tests (buat test files terlebih dahulu)
pytest
```

### Test Frontend
```bash
cd frontend
npm run test  # Perlu setup Vitest terlebih dahulu
```

## 🚀 Production Deployment

### Backend (FastAPI)
1. Set environment variables di production
2. Gunakan PostgreSQL production dari Supabase
3. Deploy ke:
   - Heroku
   - Railway
   - DigitalOcean
   - AWS/GCP/Azure

### Frontend (Vue.js)
1. Build production
```bash
npm run build
```

2. Deploy folder `dist/` ke:
   - Vercel
   - Netlify
   - Firebase Hosting
   - AWS S3 + CloudFront

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Ionic Vue Documentation](https://ionicframework.com/docs/vue/overview)

## 🐛 Troubleshooting

### Backend tidak bisa connect ke database
- Pastikan DATABASE_URL sudah benar
- Cek apakah Supabase project sudah running
- Pastikan IP address Anda di-whitelist di Supabase (Settings → Database → Connection Pooling)

### Frontend tidak bisa hit API
- Pastikan backend sudah running di port 8000
- Cek VITE_API_URL di file `.env`
- Buka browser console untuk melihat error details

### Migration error
- Pastikan sudah di virtual environment
- Cek DATABASE_URL
- Hapus folder `alembic/versions/` dan buat ulang migration

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created for school project - Semester 2

---

**Happy Coding! 🎉**
