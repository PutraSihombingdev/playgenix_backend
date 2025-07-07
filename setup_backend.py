#!/usr/bin/env python3
"""
Setup script untuk PlayGenix Backend
"""

import os
import subprocess
import sys

def create_env_file():
    """Membuat file .env dari template"""
    if not os.path.exists('.env'):
        print("📝 Membuat file .env...")
        with open('env_example.txt', 'r') as template:
            content = template.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        print("✅ File .env berhasil dibuat")
    else:
        print("ℹ️  File .env sudah ada")

def check_dependencies():
    """Cek apakah semua dependencies terinstall"""
    print("🔍 Mengecek dependencies...")
    try:
        import flask
        import flask_cors
        import mysql.connector
        import jwt
        import dotenv
        print("✅ Semua dependencies terinstall")
        return True
    except ImportError as e:
        print(f"❌ Dependency missing: {e}")
        print("💡 Jalankan: pip install -r requirements.txt")
        return False

def test_database_connection():
    """Test koneksi database"""
    print("🔍 Testing koneksi database...")
    try:
        from db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        print("✅ Koneksi database berhasil")
        return True
    except Exception as e:
        print(f"❌ Koneksi database gagal: {e}")
        print("💡 Pastikan:")
        print("   - MySQL server berjalan")
        print("   - Database 'playgenix' sudah dibuat")
        print("   - Konfigurasi di .env sudah benar")
        return False

def create_database_schema():
    """Membuat schema database"""
    print("🗄️  Membuat schema database...")
    try:
        # Baca file schema
        with open('models/schema.sql', 'r') as f:
            schema = f.read()
        
        # Import schema ke database
        from db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Split dan execute setiap statement
        statements = schema.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Schema database berhasil dibuat")
        return True
    except Exception as e:
        print(f"❌ Gagal membuat schema: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setup PlayGenix Backend")
    print("=" * 40)
    
    # 1. Buat file .env
    create_env_file()
    
    # 2. Cek dependencies
    if not check_dependencies():
        return False
    
    # 3. Test database connection
    if not test_database_connection():
        return False
    
    # 4. Buat schema database
    if not create_database_schema():
        return False
    
    print("\n" + "=" * 40)
    print("✅ Setup selesai!")
    print("🚀 Jalankan backend dengan: python run.py")
    print("🧪 Test dengan Postman menggunakan file collection yang disediakan")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 