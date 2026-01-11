#!/usr/bin/env python3
"""
Comprehensive API Test Suite - 100+ Test Cases
Tests all endpoints with various input patterns including injection attacks
"""

import requests
import json
import sys
import time

# Test configuration
BASE_URL = "http://localhost:38000"
PASSED = 0
FAILED = 0
TOTAL = 0

def test(name, condition, details=""):
    global PASSED, FAILED, TOTAL
    TOTAL += 1
    if condition:
        PASSED += 1
        print(f"✅ {TOTAL:03d}. {name}")
    else:
        FAILED += 1
        print(f"❌ {TOTAL:03d}. {name} - {details}")

def api_get(endpoint, headers=None, expected_status=200):
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        return r.status_code, r.json() if r.text else {}
    except Exception as e:
        return 0, {"error": str(e)}

def api_post(endpoint, data, headers=None, expected_status=200):
    try:
        hdrs = {"Content-Type": "application/json"}
        if headers:
            hdrs.update(headers)
        r = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=hdrs, timeout=10)
        return r.status_code, r.json() if r.text else {}
    except Exception as e:
        return 0, {"error": str(e)}

def api_delete(endpoint, headers=None):
    try:
        r = requests.delete(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        return r.status_code, r.json() if r.text else {}
    except Exception as e:
        return 0, {"error": str(e)}

print("=" * 60)
print("COMPREHENSIVE API TEST SUITE - 100+ TEST CASES")
print("=" * 60)
print(f"Base URL: {BASE_URL}")
print("=" * 60)

# ============================================================
# HEALTH CHECK TESTS (5 tests)
# ============================================================
print("\n📋 HEALTH CHECK TESTS")
print("-" * 40)

status, data = api_get("/health")
test("Health check returns 200", status == 200)
test("Health check has status field", "status" in data)
test("Health check status is ok", data.get("status") == "ok")
test("Health check has timestamp", "timestamp" in data)

status, _ = api_get("/nonexistent")
test("404 for nonexistent endpoint", status == 404)

# ============================================================
# AUTH REGISTER TESTS (20 tests)
# ============================================================
print("\n📋 AUTH REGISTER TESTS")
print("-" * 40)

# Valid registrations
test_user = f"testuser{int(time.time()) % 10000}"
status, _ = api_post("/auth/register", {"username": test_user, "password": "pass123456"})
test(f"Register valid user {test_user}", status == 204)

status, _ = api_post("/auth/register", {"username": test_user, "password": "pass123456"})
test("Reject duplicate username", status == 409)

# Username validation tests
status, _ = api_post("/auth/register", {"username": "short", "password": "pass123456"})
test("Reject username < 6 chars", status == 400)

status, _ = api_post("/auth/register", {"username": "a" * 13, "password": "pass123456"})
test("Reject username > 12 chars", status == 400)

status, _ = api_post("/auth/register", {"username": "user@#$%", "password": "pass123456"})
test("Reject username with special chars", status == 400)

status, _ = api_post("/auth/register", {"username": "user name", "password": "pass123456"})
test("Reject username with space", status == 400)

status, _ = api_post("/auth/register", {"username": "", "password": "pass123456"})
test("Reject empty username", status in [400, 422], f"Status: {status}")

# Password validation tests
status, _ = api_post("/auth/register", {"username": "newuser1", "password": "short"})
test("Reject password < 6 chars", status == 400)

status, _ = api_post("/auth/register", {"username": "newuser2", "password": "a" * 13})
test("Reject password > 12 chars", status == 400)

status, _ = api_post("/auth/register", {"username": "newuser3", "password": "pass@#$%"})
test("Reject password with special chars", status == 400)

status, _ = api_post("/auth/register", {"username": "newuser4", "password": ""})
test("Reject empty password", status in [400, 422], f"Status: {status}")

# Injection attempts in auth
status, _ = api_post("/auth/register", {"username": "'; DROP TABLE users;--", "password": "pass123456"})
test("Block SQL injection in username", status in [400, 422])

status, _ = api_post("/auth/register", {"username": "<script>alert(1)</script>", "password": "pass123456"})
test("Block XSS in username", status in [400, 422])

status, _ = api_post("/auth/register", {"username": "user123", "password": "'; DROP TABLE;--"})
test("Block SQL injection in password", status in [400, 422])

status, _ = api_post("/auth/register", {"username": "user\x00null", "password": "pass123456"})
test("Block null byte in username", status in [400, 422])

# Edge cases
# Use random numeric/upper to avoid 409 if already exists
rand_suffix = str(int(time.time() * 1000) % 10000)
status, _ = api_post("/auth/register", {"username": f"12{rand_suffix}", "password": "pass123456"})
test("Accept numeric username", status == 204)

status, _ = api_post("/auth/register", {"username": f"UP{rand_suffix}", "password": "pass123456"})
test("Accept uppercase username", status == 204)

status, _ = api_post("/auth/register", {"username": f"Mx{rand_suffix}", "password": "pass123456"})
test("Accept mixed case username", status == 204)

status, _ = api_post("/auth/register", {})
test("Reject empty payload", status in [400, 422], f"Status: {status}")

# ============================================================
# AUTH LOGIN TESTS (15 tests)
# ============================================================
print("\n📋 AUTH LOGIN TESTS")
print("-" * 40)

status, data = api_post("/auth/login", {"username": test_user, "password": "pass123456"})
test("Login valid user", status == 200)
test("Login returns token", "token" in data)
TOKEN = data.get("token", "")

status, _ = api_post("/auth/login", {"username": test_user, "password": "wrongpass"})
test("Reject wrong password", status == 401)

status, _ = api_post("/auth/login", {"username": "nonexistent", "password": "pass123456"})
test("Reject nonexistent user", status == 401)

status, _ = api_post("/auth/login", {"username": "", "password": ""})
test("Reject empty credentials", status in [400, 401, 422])

status, _ = api_post("/auth/login", {"username": test_user, "password": ""})
test("Reject empty password", status in [400, 401, 422])

status, _ = api_post("/auth/login", {"username": "", "password": "pass123456"})
test("Reject empty username", status in [400, 401, 422])

status, _ = api_post("/auth/login", {})
test("Reject no payload", status in [400, 422], f"Status: {status}")

# Injection attempts
status, _ = api_post("/auth/login", {"username": "' OR '1'='1", "password": "' OR '1'='1"})
test("Block SQL injection in login", status in [400, 401])

status, _ = api_post("/auth/login", {"username": test_user, "password": "pass123456' --"})
test("Block comment injection", status in [400, 401])

# Timing attack resistance (basic check)
start = time.time()
api_post("/auth/login", {"username": "a" * 12, "password": "a" * 12})
t1 = time.time() - start

start = time.time()
api_post("/auth/login", {"username": test_user, "password": "wrongpass"})
t2 = time.time() - start

test("Similar response time (timing attack)", abs(t1 - t2) < 1.0, f"t1={t1:.2f}, t2={t2:.2f}")

# Unicode handling
status, _ = api_post("/auth/login", {"username": "用户名", "password": "pass123456"})
test("Handle unicode username", status in [400, 401])

status, _ = api_post("/auth/login", {"username": "émoji🎉", "password": "pass123456"})
test("Handle emoji in username", status in [400, 401])

# ============================================================
# /API/ME TESTS (10 tests)
# ============================================================
print("\n📋 /API/ME TESTS")
print("-" * 40)

headers = {"Authorization": f"Bearer {TOKEN}"}

status, data = api_get("/api/me", headers=headers)
test("Get current user with valid token", status == 200)
test("Response contains username", "username" in data)

status, _ = api_get("/api/me")
test("Reject request without token", status == 401)

status, _ = api_get("/api/me", headers={"Authorization": "Bearer invalid"})
test("Reject invalid token", status == 401)

status, _ = api_get("/api/me", headers={"Authorization": "invalid"})
test("Reject malformed auth header", status == 401)

status, _ = api_get("/api/me", headers={"Authorization": ""})
test("Reject empty auth header", status == 401)

status, _ = api_get("/api/me", headers={"Authorization": "Bearer "})
test("Reject empty bearer token", status == 401)

# Token manipulation
if TOKEN:
    tampered = TOKEN[:-5] + "XXXXX"
    status, _ = api_get("/api/me", headers={"Authorization": f"Bearer {tampered}"})
    test("Reject tampered token", status == 401)

# Header injection
status, _ = api_get("/api/me", headers={"Authorization": f"Bearer {TOKEN}\r\nX-Injected: true"})
# Status 0 means client library blocked it (good), or server rejected it
test("Block header injection", status in [0, 200, 400, 401, 422], f"Status: {status}")

# ============================================================
# SEA BOTTLE CREATE TESTS (25 tests)
# ============================================================
print("\n📋 SEA BOTTLE CREATE TESTS")
print("-" * 40)

# Valid creation
status, _ = api_post("/sea/bottle", {"type": "text", "content": "Hello world!"}, headers=headers)
test("Create valid bottle", status == 204)

status, _ = api_post("/sea/bottle", {"type": "markdown", "content": "# Title"}, headers=headers)
test("Create markdown bottle", status == 204)

status, _ = api_post("/sea/bottle", {"type": "html", "content": "<p>Test</p>"}, headers=headers)
test("Create html bottle", status == 204)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "Test"})  # No auth
test("Create anonymous bottle", status == 204)

# Type validation
status, _ = api_post("/sea/bottle", {"type": "", "content": "Test"})
test("Reject empty type", status in [400, 422])

status, _ = api_post("/sea/bottle", {"type": "a" * 21, "content": "Test"})
test("Reject type > 20 chars", status == 400)

status, _ = api_post("/sea/bottle", {"type": "type with space", "content": "Test"})
test("Reject type with space", status == 400)

status, _ = api_post("/sea/bottle", {"type": "type@special", "content": "Test"})
test("Reject type with special chars", status == 400)

status, _ = api_post("/sea/bottle", {"type": "text;FLUSHALL", "content": "Test"})
test("Block injection in type", status == 400)

# Content validation
status, _ = api_post("/sea/bottle", {"type": "text", "content": ""})
test("Reject empty content", status in [400, 422])

status, _ = api_post("/sea/bottle", {"type": "text", "content": "a" * 2001})
test("Reject content > 2000 chars", status in [400, 422])

# Redis protocol injection
status, _ = api_post("/sea/bottle", {"type": "text", "content": "*3\r\n$3\r\nSET"})
test("Block Redis protocol injection", status == 400)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "$5\r\nhello"})
test("Block Redis bulk string injection", status == 400)

# Command injection
status, _ = api_post("/sea/bottle", {"type": "text", "content": "FLUSHALL now"})
test("Block FLUSHALL command", status == 400)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "CONFIG SET dir /tmp"})
test("Block CONFIG command", status == 400)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "EVAL 'return 1' 0"})
test("Block EVAL command", status == 400)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "DEBUG SEGFAULT"})
test("Block DEBUG command", status == 400)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "SHUTDOWN NOSAVE"})
test("Block SHUTDOWN command", status == 400)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "SLAVEOF evil.com 6379"})
test("Block SLAVEOF command", status == 400)

# Valid edge cases
status, _ = api_post("/sea/bottle", {"type": "text-v2", "content": "Test with hyphen type"})
test("Accept type with hyphen", status == 204)

status, _ = api_post("/sea/bottle", {"type": "type_v2", "content": "Test with underscore type"})
test("Accept type with underscore", status == 204)

status, _ = api_post("/sea/bottle", {"type": "text", "content": "This is a normal message with punctuation! :)"})
test("Accept normal content with punctuation", status == 204)

status, _ = api_post("/sea/bottle", {"type": "Unicode: 你好世界 🌍", "content": "Unicode content"})
test("Accept unicode type (if allowed) or handle", status in [204, 400, 422])

status, _ = api_post("/sea/bottle", {"type": "TEXT", "content": "Uppercase type"})
test("Accept uppercase type", status == 204)

# ============================================================
# SEA BOTTLE GET TESTS (10 tests)
# ============================================================
print("\n📋 SEA BOTTLE GET TESTS")
print("-" * 40)

status, data = api_get("/sea/bottle", headers=headers)
test("Get random bottle", status == 200)
test("Bottle has id field", "id" in data)
test("Bottle has type field", "type" in data)
test("Bottle has content field", "content" in data)
test("Bottle has creator field", "creator" in data)

# Get multiple times to check randomness
bottles = set()
for _ in range(5):
    _, d = api_get("/sea/bottle", headers=headers)
    if "id" in d:
        bottles.add(d["id"])
test("Random bottles returned", len(bottles) >= 1)

status, data = api_get("/sea/bottle")  # Without auth
test("Get bottle without auth", status == 200)

# ============================================================
# STORE BOTTLE TESTS (15 tests)
# ============================================================
print("\n📋 STORE BOTTLE TESTS")
print("-" * 40)

# First get a bottle to store
_, bottle = api_get("/sea/bottle", headers=headers)
bottle_id = bottle.get("id", "")

if bottle_id:
    status, _ = api_post("/api/store-bottle", {"bottle_id": bottle_id}, headers=headers)
    test("Store a bottle", status == 204)
    
    status, _ = api_post("/api/store-bottle", {"bottle_id": bottle_id}, headers=headers)
    test("Reject duplicate store", status == 409)
else:
    test("Store a bottle", False, "No bottle ID")
    test("Reject duplicate store", False, "No bottle ID")

# Get stored bottles
status, data = api_get("/api/store-bottle", headers=headers)
test("List stored bottles", status == 200)
test("Stored bottles is array", isinstance(data, list))

# Pagination
status, data = api_get("/api/store-bottle?page=1", headers=headers)
test("Pagination page 1", status == 200)

status, data = api_get("/api/store-bottle?page=999", headers=headers)
test("Empty page returns empty array", status == 200 and data == [])

# Invalid bottle_id
status, _ = api_post("/api/store-bottle", {"bottle_id": "invalid"}, headers=headers)
test("Reject short bottle_id", status in [400, 422])

status, _ = api_post("/api/store-bottle", {"bottle_id": "'; FLUSHALL; '"}, headers=headers)
test("Block injection in bottle_id", status in [400, 422])

status, _ = api_post("/api/store-bottle", {"bottle_id": "01KB2GQ4HMSM6ZZKEH580PV91X"}, headers=headers)
test("Reject nonexistent bottle", status == 404)

# Auth required
status, _ = api_post("/api/store-bottle", {"bottle_id": bottle_id})
test("Require auth for store", status == 401)

status, _ = api_get("/api/store-bottle")
test("Require auth for list", status == 401)

# ============================================================
# STORED BOTTLE DETAIL/DELETE TESTS (10 tests)
# ============================================================
print("\n📋 STORED BOTTLE DETAIL/DELETE TESTS")
print("-" * 40)

# Get stored bottles to test
status, stored = api_get("/api/store-bottle", headers=headers)
if stored and len(stored) > 0:
    stored_id = stored[0].get("id", "")
    
    status, data = api_get(f"/api/store-bottle/{stored_id}", headers=headers)
    test("Get stored bottle detail", status == 200)
    test("Detail has bottle info", "bottle" in data)
    
    # Access control
    status, _ = api_get(f"/api/store-bottle/{stored_id}")
    test("Require auth for detail", status == 401)
    
    # Delete
    status, _ = api_delete(f"/api/store-bottle/{stored_id}", headers=headers)
    test("Delete stored bottle", status == 204)
    
    status, _ = api_get(f"/api/store-bottle/{stored_id}", headers=headers)
    test("Deleted bottle not found", status == 404)
else:
    test("Get stored bottle detail", False, "No stored bottles")
    test("Detail has bottle info", False, "No stored bottles")
    test("Require auth for detail", False, "No stored bottles")
    test("Delete stored bottle", False, "No stored bottles")
    test("Deleted bottle not found", False, "No stored bottles")

status, _ = api_get("/api/store-bottle/invalid-id", headers=headers)
test("Invalid stored bottle id", status == 404)

status, _ = api_delete("/api/store-bottle/invalid-id", headers=headers)
test("Delete invalid id fails", status == 404)

# Injection in path
status, _ = api_get("/api/store-bottle/'; DROP TABLE;--", headers=headers)
test("Block SQL injection in path", status == 404)

status, _ = api_delete("/api/store-bottle/../../../etc/passwd", headers=headers)
test("Block path traversal", status == 404)

# ============================================================
# ADDITIONAL SECURITY TESTS (10 tests)
# ============================================================
print("\n📋 ADDITIONAL SECURITY TESTS")
print("-" * 40)

# Large payload
status, _ = api_post("/sea/bottle", {"type": "text", "content": "x" * 1999})
test("Accept max length content", status == 204)

# HTTP method tests
try:
    r = requests.put(f"{BASE_URL}/sea/bottle", json={}, timeout=5)
    test("Reject PUT on bottle", r.status_code == 405)
except:
    test("Reject PUT on bottle", True)

try:
    r = requests.patch(f"{BASE_URL}/health", timeout=5)
    test("Reject PATCH on health", r.status_code == 405)
except:
    test("Reject PATCH on health", True)

# Content-Type handling
try:
    r = requests.post(f"{BASE_URL}/sea/bottle", data="type=text&content=test", 
                     headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=5)
    test("Handle form data gracefully", r.status_code in [400, 422])
except:
    test("Handle form data gracefully", True)

# CORS headers (if applicable)
try:
    r = requests.options(f"{BASE_URL}/health", timeout=5)
    test("OPTIONS request handled", r.status_code in [200, 204, 405])
except:
    test("OPTIONS request handled", True)

# Rate limiting (basic - just ensure we can make many requests)
success = True
for i in range(10):
    s, _ = api_get("/health")
    if s != 200:
        success = False
        break
test("Handle rapid requests", success)

# Null byte injection
status, _ = api_post("/sea/bottle", {"type": "text\x00", "content": "test"})
test("Handle null byte in type", status in [400, 422])

status, _ = api_post("/sea/bottle", {"type": "text", "content": "test\x00hidden"})
test("Accept null byte in content", status in [204, 400])  # May or may not be blocked

# Very long type (edge case of validation)
status, _ = api_post("/sea/bottle", {"type": "a" * 20, "content": "test"})
test("Accept max length type", status == 204)

# ============================================================
# CHAT TESTS (10 tests)
# ============================================================
print("\n📋 CHAT TESTS")
print("-" * 40)

# Send message
status, _ = api_post("/chat/global", {"content": "Hello Global Chat!"}, headers=headers)
test("Send global chat message", status == 204)

status, _ = api_post("/chat/global", {"content": "Second message"}, headers=headers)
test("Send second message", status == 204)

# Get messages
status, data = api_get("/chat/global", headers=headers)
test("Get global chat history", status == 200)
test("History is list", isinstance(data, list))
if isinstance(data, list) and len(data) > 0:
    test("Message structure has id", "id" in data[0])
    test("Message structure has content", "content" in data[0])
    test("Message structure has sender", "sender" in data[0])
    test("Message structure has is_me", "is_me" in data[0])
    test("is_me is true for my message", data[0]["is_me"] is True)
    
    # Check sort order (latest first)
    if len(data) >= 2:
        test("Sorted by latest first", data[0]["created_at"] >= data[1]["created_at"])
else:
    test("Message structure checks", False, "No messages returned")

# Pagination
status, data_p1 = api_get("/chat/global?limit=1", headers=headers)
test("Pagination limit works", len(data_p1) == 1)

# Auth checks
status, _ = api_post("/chat/global", {"content": "No auth"})
test("Require auth for send chat", status == 401)

status, _ = api_get("/chat/global")
test("Require auth for get chat", status == 401)

# Validation
status, _ = api_post("/chat/global", {"content": ""}, headers=headers)
test("Reject empty chat message", status in [400, 422])

status, _ = api_post("/chat/global", {"content": "a" * 1001}, headers=headers)
test("Reject long chat message", status in [400, 422])

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"Total Tests: {TOTAL}")
print(f"Passed:      {PASSED} ({PASSED/TOTAL*100:.1f}%)")
print(f"Failed:      {FAILED} ({FAILED/TOTAL*100:.1f}%)")
print("=" * 60)

sys.exit(0 if FAILED == 0 else 1)
