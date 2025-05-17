from werkzeug.security import generate_password_hash

users = [
    ('john_doe', 'password123'),
    ('jane_smith', 'password456'),
    ('admin', 'admin123'),
    ('bob_wilson', '123123')
]

for login, password in users:
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    print(f"('{login}', '{hashed_password}'),")