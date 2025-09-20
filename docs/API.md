# WealthTech Smart Search API API Documentation

**Version:** 1.0.0  
**Description:** Smart search API for client documents and meeting notes

## Base URL
`http://localhost:8000`

## Endpoints

### POST /clients/{client_id}/documents

**Summary:** Create Document

**Parameters:**
- `client_id` (path) (required): N/A

**Request Body:**
Content-Type: application/json

**Responses:**
- `201`: Successful Response
- `422`: Validation Error

---

### POST /clients/{client_id}/notes

**Summary:** Create Note

**Parameters:**
- `client_id` (path) (required): N/A

**Request Body:**
Content-Type: application/json

**Responses:**
- `201`: Successful Response
- `422`: Validation Error

---

### GET /search

**Summary:** Search

**Parameters:**
- `q` (query) (required): Search query
- `type` (query): Filter by type: document or note

**Responses:**
- `200`: Successful Response
- `422`: Validation Error

---

### GET /health

**Summary:** Health Check

**Responses:**
- `200`: Successful Response

---

