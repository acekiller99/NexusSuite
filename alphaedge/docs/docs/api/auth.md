# Authentication API

## Register

```http
POST /api/v1/auth/register
Content-Type: application/json
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "StrongPass123!",
  "full_name": "John Doe"
}
```

**Response (201):**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2026-01-01T00:00:00Z"
  },
  "message": "User registered successfully"
}
```

## Login

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded
```

**Request Body:**  `username=user@example.com&password=StrongPass123!`

**Response (200):**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
  },
  "message": "Login successful"
}
```

## Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```
