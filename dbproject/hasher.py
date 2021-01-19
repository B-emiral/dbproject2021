from passlib.hash import pbkdf2_sha256 as hasher
admin_password = "adminpw"
admin_hashed = hasher.hash(admin_password)
print(admin_hashed)

print("hello")