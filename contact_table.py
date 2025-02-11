import MySQLdb

# Connect to MySQL Database
conn = MySQLdb.connect(
    host="localhost",
    user="root",          # Your MySQL username
    passwd="password",    # Your MySQL password
    db="contactDB"       # Your database name
)
cursor = conn.cursor()

# Create a table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    address TEXT NOT NULL,
    contact_number VARCHAR(15) NOT NULL UNIQUE
)
""")
conn.commit()
conn.close()
print("success")
