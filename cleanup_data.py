from db import get_connection

def cleanup_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Membersihkan data yang mungkin menyebabkan constraint violations...")
        
        # Hapus semua data dari cart
        cursor.execute("DELETE FROM cart")
        print("✓ Cart dibersihkan")
        
        # Hapus semua data dari transaction_items
        cursor.execute("DELETE FROM transaction_items")
        print("✓ Transaction items dibersihkan")
        
        # Hapus semua data dari transactions
        cursor.execute("DELETE FROM transactions")
        print("✓ Transactions dibersihkan")
        
        # Hapus semua data dari payments
        cursor.execute("DELETE FROM payments")
        print("✓ Payments dibersihkan")
        
        # Hapus semua data dari products
        cursor.execute("DELETE FROM products")
        print("✓ Products dibersihkan")
        
        # Reset auto increment
        cursor.execute("ALTER TABLE products AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE cart AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE payments AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE transactions AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE transaction_items AUTO_INCREMENT = 1")
        print("✓ Auto increment direset")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Data berhasil dibersihkan!")
        
    except Exception as e:
        print(f"Error cleaning data: {str(e)}")

if __name__ == "__main__":
    cleanup_data() 