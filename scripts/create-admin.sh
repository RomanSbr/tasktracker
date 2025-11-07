#!/bin/bash
set -e

echo "👤 Creating admin user..."

read -p "Email: " email
read -p "Username: " username
read -sp "Password: " password
echo ""

curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$email\",
    \"username\": \"$username\",
    \"password\": \"$password\",
    \"first_name\": \"Admin\",
    \"last_name\": \"User\"
  }"

echo ""
echo "✅ Admin user created successfully!"
