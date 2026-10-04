
# API Reference

## Base URL

```text
http://127.0.0.1:5000
```

All request and response bodies use JSON unless otherwise stated.

## 1. Health Check

**GET** `/health`

Checks whether the application is running.

Example:

```bash
curl http://127.0.0.1:5000/health
```

## 2. Password Analysis

**POST** `/api/analyze`

Analyzes a supplied password and returns its strength assessment.

Request:

```json
{
  "password": "Demo-Password-2026!"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{\"password\":\"Demo-Password-2026!\"}"
```

A successful response contains:

- `success`
- `data`
- Overall score and strength classification.
- Individual analyzer results.
- Findings and recommendations.
- Privacy information.

The submitted password is not intentionally returned in the response.

## 3. Secure Password Generation

**POST** `/api/generate`

Generates a password using Python's `secrets` module.

Request:

```json
{
  "length": 20,
  "include_lowercase": true,
  "include_uppercase": true,
  "include_digits": true,
  "include_symbols": true
}
```

All options are optional. Defaults:

- Length: 20.
- Lowercase: enabled.
- Uppercase: enabled.
- Digits: enabled.
- Symbols: enabled.

A successful response contains:

- `success`
- `data.password`
- `data.length`
- `data.message`

The generated password is intentionally returned to the caller. The endpoint does not save it.

## 4. Password Policy Checker

**POST** `/api/policy/check`

Checks a password against the application's default policy.

Request:

```json
{
  "password": "Demo-Password-2026!"
}
```

The default policy evaluates:

- Minimum length.
- Lowercase characters.
- Uppercase characters.
- Digits.
- Symbols.
- Common password usage.
- Sequential patterns.
- Keyboard patterns.
- Repeated patterns.
- Predictable patterns.

The response includes compliance status, passed and failed checks, and recommendations.

## 5. Save Analysis History

**POST** `/api/history`

This endpoint requires explicit user action. It accepts only approved analysis metadata.

Request:

```json
{
  "score": 90,
  "strength": "VERY STRONG",
  "findings_count": 0,
  "character_types_count": 4,
  "analysis_completed": true
}
```

Successful response status: `201 Created`.

Unknown fields are rejected. Passwords and hashes are not accepted.

## 6. Retrieve Analysis History

**GET** `/api/history`

Returns the latest saved analysis metadata.

Example:

```bash
curl http://127.0.0.1:5000/api/history
```

Response structure:

```json
{
  "success": true,
  "total_records": 1,
  "data": []
}
```

The data contains metadata records, not passwords.

## 7. Clear Analysis History

**DELETE** `/api/history`

Deletes all saved analysis metadata.

Example:

```bash
curl -X DELETE http://127.0.0.1:5000/api/history
```

## 8. Argon2id Hash Demonstration

**POST** `/api/hash-demo/hash`

Creates an educational Argon2id password hash.

Request:

```json
{
  "password": "Synthetic-Demo-Password!"
}
```

The response contains the encoded hash and:

```json
{
  "algorithm": "Argon2id",
  "stored": false
}
```

The hash is returned for demonstration only. It is not persisted by this endpoint.

## 9. Argon2id Verification Demonstration

**POST** `/api/hash-demo/verify`

Verifies a password against an Argon2id encoded hash.

Request:

```json
{
  "password": "Synthetic-Demo-Password!",
  "encoded_hash": "PASTE_THE_HASH_RETURNED_BY_THE_HASH_ENDPOINT"
}
```

The response includes:

- `success`
- `matches`
- `algorithm`
- `stored`

No password or hash is saved.

## 10. API Documentation

Swagger UI:

```text
/apidocs
```

OpenAPI JSON:

```text
/openapi.json
```

## Rate Limiting

The application applies route-level rate limits:

| Endpoint | Limit |
|---|---|
| `/api/analyze` | 10 requests/minute |
| `/api/generate` | 10 requests/minute |
| `/api/policy/check` | 10 requests/minute |
| History POST | 10 requests/minute |
| History GET | 30 requests/minute |
| History DELETE | 5 requests/minute |
| Argon2id hash | 10 requests/minute |
| Argon2id verify | 10 requests/minute |

The current limiter uses in-memory storage. Its counters reset when the application restarts.

## Common HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request completed successfully |
| 201 | Metadata created successfully |
| 400 | Invalid request data |
| 404 | Endpoint not found |
| 413 | Request too large |
| 415 | Unsupported content type |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

## Security Note

Use synthetic demonstration passwords when experimenting with these endpoints. Avoid sending real account credentials to an educational application.
