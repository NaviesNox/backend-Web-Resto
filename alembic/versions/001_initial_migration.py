"""Initial migration with admin user

Revision ID: 001
Revises: 
Create Date: 2026-02-17

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime
import bcrypt

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'MANAGER', 'KASIR', 'PRAMUSAJI', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create karyawan table
    op.create_table('karyawan',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nama', sa.String(), nullable=False),
        sa.Column('alamat', sa.String(), nullable=True),
        sa.Column('no_telepon', sa.String(), nullable=True),
        sa.Column('posisi', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_karyawan_id'), 'karyawan', ['id'], unique=False)

    # Create kategori_menu table
    op.create_table('kategori_menu',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nama', sa.String(), nullable=False),
        sa.Column('deskripsi', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nama')
    )
    op.create_index(op.f('ix_kategori_menu_id'), 'kategori_menu', ['id'], unique=False)

    # Create menu table
    op.create_table('menu',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nama', sa.String(), nullable=False),
        sa.Column('deskripsi', sa.String(), nullable=True),
        sa.Column('harga', sa.Float(), nullable=False),
        sa.Column('kategori_id', sa.Integer(), nullable=False),
        sa.Column('gambar_url', sa.String(), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['kategori_id'], ['kategori_menu.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menu_id'), 'menu', ['id'], unique=False)

    # Create meja table
    op.create_table('meja',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nomor_meja', sa.String(), nullable=False),
        sa.Column('kapasitas', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('TERSEDIA', 'TERISI', 'RESERVED', name='statusmeja'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nomor_meja')
    )
    op.create_index(op.f('ix_meja_id'), 'meja', ['id'], unique=False)

    # Create pesanan table
    op.create_table('pesanan',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meja_id', sa.Integer(), nullable=False),
        sa.Column('karyawan_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED', name='statuspesanan'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['karyawan_id'], ['karyawan.id'], ),
        sa.ForeignKeyConstraint(['meja_id'], ['meja.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pesanan_id'), 'pesanan', ['id'], unique=False)

    # Create detail_pesanan table
    op.create_table('detail_pesanan',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pesanan_id', sa.Integer(), nullable=False),
        sa.Column('menu_id', sa.Integer(), nullable=False),
        sa.Column('jumlah', sa.Integer(), nullable=False),
        sa.Column('harga_satuan', sa.Float(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('catatan', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
        sa.ForeignKeyConstraint(['pesanan_id'], ['pesanan.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_detail_pesanan_id'), 'detail_pesanan', ['id'], unique=False)

    # Create transaksi table
    op.create_table('transaksi',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pesanan_id', sa.Integer(), nullable=False),
        sa.Column('total_harga', sa.Float(), nullable=False),
        sa.Column('pajak', sa.Float(), nullable=True),
        sa.Column('diskon', sa.Float(), nullable=True),
        sa.Column('total_bayar', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['pesanan_id'], ['pesanan.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pesanan_id')
    )
    op.create_index(op.f('ix_transaksi_id'), 'transaksi', ['id'], unique=False)

    # Create pembayaran table
    op.create_table('pembayaran',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transaksi_id', sa.Integer(), nullable=False),
        sa.Column('metode_pembayaran', sa.Enum('CASH', 'DEBIT', 'CREDIT', 'QRIS', 'TRANSFER', name='metodepembayaran'), nullable=False),
        sa.Column('jumlah_bayar', sa.Float(), nullable=False),
        sa.Column('kembalian', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['transaksi_id'], ['transaksi.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaksi_id')
    )
    op.create_index(op.f('ix_pembayaran_id'), 'pembayaran', ['id'], unique=False)

    # Create stok_harian table
    op.create_table('stok_harian',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('menu_id', sa.Integer(), nullable=False),
        sa.Column('tanggal', sa.Date(), nullable=True),
        sa.Column('stok_tersedia', sa.Integer(), nullable=False),
        sa.Column('stok_terjual', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('menu_id')
    )
    op.create_index(op.f('ix_stok_harian_id'), 'stok_harian', ['id'], unique=False)

    # Insert admin user "Nox" with password "HaruYama"
    hashed_password = bcrypt.hashpw("HaruYama".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    op.execute(f"""
        INSERT INTO users (username, email, hashed_password, role, is_active, created_at, updated_at)
        VALUES ('Nox', 'nox@restoapp.com', '{hashed_password}', 'ADMIN', true, '{datetime.utcnow()}', '{datetime.utcnow()}')
    """)


def downgrade() -> None:
    op.drop_index(op.f('ix_stok_harian_id'), table_name='stok_harian')
    op.drop_table('stok_harian')
    op.drop_index(op.f('ix_pembayaran_id'), table_name='pembayaran')
    op.drop_table('pembayaran')
    op.drop_index(op.f('ix_transaksi_id'), table_name='transaksi')
    op.drop_table('transaksi')
    op.drop_index(op.f('ix_detail_pesanan_id'), table_name='detail_pesanan')
    op.drop_table('detail_pesanan')
    op.drop_index(op.f('ix_pesanan_id'), table_name='pesanan')
    op.drop_table('pesanan')
    op.drop_index(op.f('ix_meja_id'), table_name='meja')
    op.drop_table('meja')
    op.drop_index(op.f('ix_menu_id'), table_name='menu')
    op.drop_table('menu')
    op.drop_index(op.f('ix_kategori_menu_id'), table_name='kategori_menu')
    op.drop_table('kategori_menu')
    op.drop_index(op.f('ix_karyawan_id'), table_name='karyawan')
    op.drop_table('karyawan')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
