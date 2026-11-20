$ curl -i -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "patty", "password": "TotallyWrong123!"}'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Fri, 20 Nov 2026 00:20:50 GMT
Content-Type: application/json
Content-Length: 25
Connection: close

{"error":"login failed"}

sqlite> SELECT * FROM users WHERE id = 6;
6|jack|scrypt:32768:8:1$ksRRnsTMLJ7b2n0H$5eafccab6b8ca0a69e12f1fadf675074791845b2379844f307417f93b8bd217c645a83e1bdef8cc5d2765479ce8c45a1d20d1fc5c922b3abdede3fa9d08d3524|true|jack@gmail.com|5556623232|2026-11-19 14:07:00|user

sqlite> PRAGMA table_info(users);
0|id|INTEGER|1||1
1|username|TEXT|1||0
2|password_hash|TEXT|1|''|0
3|is_admin|INTEGER|1|'0'|0
4|email|TEXT|1||0
5|phone|TEXT|0||0
6|date_created|DATETIME|1|CURRENT_TIMESTAMP|0
7|role|TEXT|1|'user'|0

$ curl -i -X POST http://127.0.0.1:5000/login   -H "Content-Type: application/json"   -d '{"password": "something"}'
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Fri, 20 Nov 2026 01:30:16 GMT
Content-Type: application/json
Content-Length: 32
Connection: close

{"error":"missing credentials"}

$ curl -i -X POST http://127.0.0.1:5000/login   -H "Content-Type: application/json"   -d '{"username": "hippy", "password": ""}'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Fri, 20 Nov 2026 01:30:03 GMT
Content-Type: application/json
Content-Length: 25
Connection: close

{"error":"login failed"}
