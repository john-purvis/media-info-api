/admin/dashboard

Navigate to http://127.0.0.1:5000/admin/dashboard then with the page loaded run this in the console:
fetch('/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username: 'admin', password: 'g0dM0d3'})
})
.then(r => r.json())
.then(d => { localStorage.setItem('access_token', d.access_token); location.reload(); });



/register

$ curl -i -s -X POST "http://127.0.0.1:5000/register" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 17 Nov 2026 21:49:51 GMT
Content-Type: application/json
Content-Length: 43
Connection: close

{"error":"username and password required"}


$ curl -i -s -X POST "http://127.0.0.1:5000/register" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"mary\", \"password\": \"winston\", \"email\": \"mary@gmail.com\", \"phone\": \"5556664444\"}"
HTTP/1.1 409 CONFLICT
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 17 Nov 2026 21:38:19 GMT
Content-Type: application/json
Content-Length: 44
Connection: close

{"error":"username or email already taken"}


$ curl -i -s -X POST "http://127.0.0.1:5000/register" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"chad\", \"password\": \"winston\", \"email\": \"chad@gmail.com\", \"phone\": \"5556664444\"}"
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 17 Nov 2026 22:42:17 GMT
Content-Type: application/json
Content-Length: 133
Connection: close

{"id":5,"username":"chad","is_admin":0,"email":"chad@gmail.com","phone":"5556664444","date_created":"Tue, 17 Nov 2026 22:42:17 GMT"}




/login

$ curl -i -s -X POST "http://127.0.0.1:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"admin\", \"password\": \"g0dM0d3\"}"                         HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:02:47 GMT
Content-Type: application/json
Content-Length: 268
Connection: close

{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZDBhYjEzM2QtNWU0Yy00YTkwLWE1MzctMjYwYWM1MDc1MmQxIiwiaWF0IjoxNzk0OTgxNzY3LCJleHAiOjE3OTQ5ODUzNjcsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.JSEmKH6Oo4MDHhDzLE9ZWdMS7u7Ki4JyAAxIkiQfKtU"}




/logout

$ curl -i -s -X POST "http://127.0.0.1:5000/logout" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZDBhYjEzM2QtNWU0Yy00YTkwLWE1MzctMjYwYWM1MDc1MmQxIiwiaWF0IjoxNzk0OTgxNzY3LCJleHAiOjE3OTQ5ODUzNjcsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.JSEmKH6Oo4MDHhDzLE9ZWdMS7u7Ki4JyAAxIkiQfKtU" -d ""
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:04:13 GMT
Content-Type: application/json
Content-Length: 30
Connection: close

{"message":"user logged out"}


$ curl -i -s -X POST "http://127.0.0.1:5000/logout" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZDBhYjEzM2QtNWU0Yy00YTkwLWE1MzctMjYwYWM1MDc1MmQxIiwiaWF0IjoxNzk0OTgxNzY3LCJleHAiOjE3OTQ5ODUzNjcsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.JSEmKH6Oo4MDHhDzLE9ZWdMS7u7Ki4JyAAxIkiQfKtU" -d ""
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:04:33 GMT
Content-Type: application/json
Content-Length: 35
Connection: close

{"error":"token has been revoked"}



/users

$ curl -i -s -X GET "http://127.0.0.1:5000/users" -H "accept: application/json"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:06:16 GMT
Content-Type: application/json
Content-Length: 54
Connection: close

{"error":"missing or malformed authorization header"}


$ curl -i -s -X GET "http://127.0.0.1:5000/users" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZmI0ZWIyYTYtNTQzNC00Yjk3LTg0MWItZTM5MzBlYzhiMWNiIiwiaWF0IjoxNzk0OTgyMDEwLCJleHAiOjE3OTQ5ODU2MTAsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.d1PSDIAke9VB-ZTSIln5EIOQXHYBmdQmSAvQrHyyIOQ"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:07:31 GMT
Content-Type: application/json
Content-Length: 709
Connection: close

[{"id":1,"username":"admin","is_admin":"True","email":"admin@media_info.com","phone":"5555555555","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"},{"id":5,"username":"chad","is_admin":0,"email":"chad@gmail.com","phone":"5556664444","date_created":"Tue, 17 Nov 2026 22:42:17 GMT"},{"id":2,"username":"erica","is_admin":"False","email":"erica@media_info.com","phone":"5554444444","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"},{"id":3,"username":"jerry","is_admin":"False","email":"jerry@media_info.com","phone":"5553333333","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"},{"id":4,"username":"mary","is_admin":0,"email":"mary@mediainfo.com","phone":"5658992323","date_created":"Tue, 17 Nov 2026 18:43:07 GMT"}]



/users/5

$ curl -i -s -X GET "http://127.0.0.1:5000/users/5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZmI0ZWIyYTYtNTQzNC00Yjk3LTg0MWItZTM5MzBlYzhiMWNiIiwiaWF0IjoxNzk0OTgyMDEwLCJleHAiOjE3OTQ5ODU2MTAsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.d1PSDIAke9VB-ZTSIln5EIOQXHYBmdQmSAvQrHyyIOQ"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:08:12 GMT
Content-Type: application/json
Content-Length: 133
Connection: close

{"id":5,"username":"chad","is_admin":0,"email":"chad@gmail.com","phone":"5556664444","date_created":"Tue, 17 Nov 2026 22:42:17 GMT"}


$ curl -i -s -X GET "http://127.0.0.1:5000/users/999" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZmI0ZWIyYTYtNTQzNC00Yjk3LTg0MWItZTM5MzBlYzhiMWNiIiwiaWF0IjoxNzk0OTgyMDEwLCJleHAiOjE3OTQ5ODU2MTAsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.d1PSDIAke9VB-ZTSIln5EIOQXHYBmdQmSAvQrHyyIOQ"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:08:34 GMT
Content-Type: application/json
Content-Length: 17
Connection: close

"user not found"


$ curl -i -s -X GET "http://127.0.0.1:5000/users/999" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZmI0ZWIyYTYtNTQzNC00Yjk3LTg0MWItZTM5MzBlYzhiMWNiIiwiaWF0IjoxNzk0OTgyMDEwLCJleHAiOjE3OTQ5ODU2MTAsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.d1PSDIAke9VB-ZTSIln5EIOQXHYBmdQmSAvQrHyyI"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:08:52 GMT
Content-Type: application/json
Content-Length: 26
Connection: close

{"error":"invalid token"}


$ curl -i -s -X GET "http://127.0.0.1:5000/users/999" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZmI0ZWIyYTYtNTQzNC00Yjk3LTg0MWItZTM5MzBlYzhiMWNiIiwiaWF0IjoxNzk0OTgyMDEwLCJleHAiOjE3OTQ5ODU2MTAsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.d1PSDIAke9VB-ZTSIln5EIOQXHYBmdQmSAvQrHyyIOQ"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 18 Nov 2026 06:09:36 GMT
Content-Type: application/json
Content-Length: 35
Connection: close

{"error":"token has been revoked"}


==========================================================================================================


TOKEN EXPIRATION

$ curl -i -s -X POST "http://127.0.0.1:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"erica\", \"password\": \"Pa55w0rd\"}"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 16:47:21 GMT
Content-Type: application/json
Content-Length: 288
Connection: close

{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiODFlYWI5ZDUtYjczMi00NDQ2LTk4OTgtOTEzMDM0NTA0ZGU5IiwiaWF0IjoxNzk1MTA2ODQxLCJleHAiOjE3OTUxMDY5MDEsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.zsl-AOq5k5ASUnnk9IYSfoER1O99seKFxQX_QP6x9jY"}


$ curl -i -s -X GET "http://127.0.0.1:5000/users" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiODFlYWI5ZDUtYjczMi00NDQ2LTk4OTgtOTEzMDM0NTA0ZGU5IiwiaWF0IjoxNzk1MTA2ODQxLCJleHAiOjE3OTUxMDY5MDEsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.zsl-AOq5k5ASUnnk9IYSfoER1O99seKFxQX_QP6x9jY"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 16:49:16 GMT
Content-Type: application/json
Content-Length: 30
Connection: close

{"error":"token has expired"}

==========================================================================================================

USER GET OWN PROFILE

$ curl -i -s -X GET "http://127.0.0.1:5000/users/me" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjM3MGFkZjQtMDcxYS00ODY3LWIyMjctNjE0MGE1MTZjYzhmIiwiaWF0IjoxNzk1MTA5Mzg1LCJleHAiOjE3OTUxMTY1ODUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.cUnkodWgGsQFesfOw9jMlUN7UlJdzCsaiGCiPdtge_o"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 17:37:20 GMT
Content-Type: application/json
Content-Length: 114
Connection: close

{"username":"erica","email":"erican@help.me","phone":"5554444444","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"}


USER EDIT PROFILE

$ curl -i -s -X PATCH "http://127.0.0.1:5000/users/me" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjM3MGFkZjQtMDcxYS00ODY3LWIyMjctNjE0MGE1MTZjYzhmIiwiaWF0IjoxNzk1MTA5Mzg1LCJleHAiOjE3OTUxMTY1ODUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.cUnkodWgGsQFesfOw9jMlUN7UlJdzCsaiGCiPdtge_o" -H "Content-Type: application/json" -d "{ \"is_admin\": true, \"email\": \"erican@media-info.com\", \"attack\": \"this\"}"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 17:37:53 GMT
Content-Type: application/json
Content-Length: 121
Connection: close

{"username":"erica","email":"erican@media-info.com","phone":"5554444444","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"}


USER SHOW PROFILE CHANGED

$ curl -i -s -X GET "http://127.0.0.1:5000/users/me" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjM3MGFkZjQtMDcxYS00ODY3LWIyMjctNjE0MGE1MTZjYzhmIiwiaWF0IjoxNzk1MTA5Mzg1LCJleHAiOjE3OTUxMTY1ODUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.cUnkodWgGsQFesfOw9jMlUN7UlJdzCsaiGCiPdtge_o"                      HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 17:38:12 GMT
Content-Type: application/json
Content-Length: 121
Connection: close

{"username":"erica","email":"erican@media-info.com","phone":"5554444444","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"}


==========================================================================================================


$ curl -i -s -X GET "http://127.0.0.1:5000/users/me" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiYWZmMGViMDgtMWQ0NS00ZjA1LWI3Y2UtNWFhYjQ2YTg1ZjM3IiwiaWF0IjoxNzk1MTEwNTc5LCJleHAiOjE3OTUxMTc3NzksInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.TLAKafGLHx2EYflmk_5m2uMZ-qb7ARXu852PPxlntW0"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 17:54:50 GMT
Content-Type: application/json
Content-Length: 120
Connection: close

{"username":"jerry","email":"jerry@media_info.com","phone":"5553333333","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"}



$ curl -i -s -X PATCH "http://127.0.0.1:5000/users/me" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiYWZmMGViMDgtMWQ0NS00ZjA1LWI3Y2UtNWFhYjQ2YTg1ZjM3IiwiaWF0IjoxNzk1MTEwNTc5LCJleHAiOjE3OTUxMTc3NzksInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.TLAKafGLHx2EYflmk_5m2uMZ-qb7ARXu852PPxlntW0" -H "Content-Type: application/json" -d "{ \"phone\": \"2325688989\", \"email\": \"awesome_jerry@media-info.com\", \"some\": \"field\"}"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 17:55:20 GMT
Content-Type: application/json
Content-Length: 128
Connection: close

{"username":"jerry","email":"awesome_jerry@media-info.com","phone":"2325688989","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"}


$ curl -i -s -X GET "http://127.0.0.1:5000/users/me" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiYWZmMGViMDgtMWQ0NS00ZjA1LWI3Y2UtNWFhYjQ2YTg1ZjM3IiwiaWF0IjoxNzk1MTEwNTc5LCJleHAiOjE3OTUxMTc3NzksInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.TLAKafGLHx2EYflmk_5m2uMZ-qb7ARXu852PPxlntW0"                      HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 17:55:46 GMT
Content-Type: application/json
Content-Length: 128
Connection: close

{"username":"jerry","email":"awesome_jerry@media-info.com","phone":"2325688989","date_created":"Tue, 17 Nov 2026 06:14:02 GMT"}


==========================================================================================================

DELETE TEST AS NON ADMIN USER

$ curl -i -s -X DELETE "http://127.0.0.1:5000/users/5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiYzljNTU4MGQtODI4Yi00N2RhLWE5MzYtOTNmNjY2YWI3N2E4IiwiaWF0IjoxNzk1MTEyMjk1LCJleHAiOjE3OTUxMTk0OTUsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.IgA4z8m5blJVbEYawq0fabOBauEIMt8IcNZBQJ8-UuQ"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 18:20:07 GMT
Content-Type: application/json
Content-Length: 36
Connection: close

{"error":"authentication required"}


DELETE TEST AS ADMIN USER

$ curl -i -s -X DELETE "http://127.0.0.1:5000/users/5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiZWFiMjJlYTUtNmJmMi00YmU2LTk3OTEtODU2MTE1NDFlNDlmIiwiaWF0IjoxNzk1MTEyNDc2LCJleHAiOjE3OTUxMTk2NzYsInVzZXJuYW1lIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJpc19hZG1pbiI6dHJ1ZX0.mg_VUUiBx81Dd1TjYcm54aG0Umm8yW6eszPPlgE_7LM"
HTTP/1.1 204 NO CONTENT
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 18:24:51 GMT
Content-Type: text/html; charset=utf-8
Connection: close


NO AUTH HEADER AT ALL

$ curl -i -s -X DELETE "http://127.0.0.1:5000/users/5" -H "accept: application/json"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 18:31:37 GMT
Content-Type: application/json
Content-Length: 54
Connection: close

{"error":"missing or malformed authorization header"}

==========================================================================================================

$ curl -i -X PATCH http://localhost:5000/users/2 \
  -H "Content-Type: application/json" \
  -d '{"email": "new@example.com"}'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 19:35:06 GMT
Content-Type: application/json
Content-Length: 54
Connection: close

{"error":"missing or malformed authorization header"}

$ curl -i -X PATCH http://localhost:5000/users/2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer abc.def.ghi" \
  -d '{"email": "new@example.com"}'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 19:35:17 GMT
Content-Type: application/json
Content-Length: 26
Connection: close

{"error":"invalid token"}

$ curl -i -X PATCH http://localhost:5000/users/2   -H "Content-Type: application/json"   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiZWY5MDgxN2MtODk0MC00ZDgwLWE0YjItOGY2Y2ZiZjY3MDFiIiwiaWF0IjoxNzk1MTE3MDEyLCJleHAiOjE3OTUxMjQyMTIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.c0i1Xy3pcwgh6xIdT52pzFszv0rJq-vf32gHTBeHYZE" -d '{"email": "new@example.com"}'
HTTP/1.1 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 19 Nov 2026 19:39:36 GMT
Content-Type: application/json
Content-Length: 26
Connection: close

{"error":"access denied"}

$ curl -i -s -X GET "http://127.0.0.1:5000/users/3" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjRmYmYxYmYtNDA3YS00YzBkLWJkMGMtNjY2ZjQ3OTBkNWNmIiwiaWF0IjoxNzk1MTU2MjYwLCJleHAiOjE3OTUxNjM0NjAsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.7JXFW2s7ix-BR9KDl8G_mxl7jBmAaGvzd9Lg2313G98"
HTTP/1.1 403 FORBIDDEN
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Fri, 20 Nov 2026 06:32:19 GMT
Content-Type: application/json
Content-Length: 41
Connection: close

{"error":"elevated privileges required"}

TEST LOGIN WITH NO USERNAME
curl -i -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"password": "something"}'
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Fri, 20 Nov 2026 01:30:16 GMT
Content-Type: application/json
Content-Length: 32
Connection: close

{"error":"missing credentials"}

TEST LOGIN WITH GOOD ACCOUNT WRONG PASSWORD
curl -i -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "patty", "password": "TotallyWrong123!"}'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Fri, 20 Nov 2026 00:20:50 GMT
Content-Type: application/json
Content-Length: 25
Connection: close

{"error":"login failed"}

TEST LOGIN WITH GOOD ACCOUNT BLANK PASSWORD
$ curl -i -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "chad", "password": ""}'
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Fri, 20 Nov 2026 01:28:20 GMT
Content-Type: application/json
Content-Length: 25
Connection: close

{"error":"login failed"}

==========================================================================================================
VIEW ONLY OWNERS FILES BASED ON CURRENT USER ID

# USER ID = 3
curl -i -X POST http://127.0.0.1:5000/login   -H "Content-Type: application/json"   -d '{"username": "jerry", "password": "Pa55w0rd"}'
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiNjQ4ZGY0MDItODE4NC00N2U5LTg3ZDMtYzY4OWFkZmMzZjk0IiwiaWF0IjoxNzk1NTE3NjcxLCJleHAiOjE3OTU1MjQ4NzEsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.tJglB5IOxwdZP7OKXTHBmPIfeiIVPp6BXWephffcA0Q"
}

# USER ID = 2
curl -i -X POST http://127.0.0.1:5000/login   -H "Content-Type: application/json"   -d '{"username": "erica", "password": "Pa55w0rd"}'
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiMjNlODNhMDAtZDA1Mi00YmI4LWI5ODEtN2NiZWVhY2U4OTI2IiwiaWF0IjoxNzk1NTE5NDk5LCJleHAiOjE3OTU1MjY2OTksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.JC7UbNUyfKnWaa5FG2qyZYryR3CnDaURhzuAHeRf2-c"
}


# CREATE MEDIA AS USER 3
curl -i   -X POST http://localhost:5000/media   -H "Content-Type: application/json"   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiNjQ4ZGY0MDItODE4NC00N2U5LTg3ZDMtYzY4OWFkZmMzZjk0IiwiaWF0IjoxNzk1NTE3NjcxLCJleHAiOjE3OTU1MjQ4NzEsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.tJglB5IOxwdZP7OKXTHBmPIfeiIVPp6BXWephffcA0Q"   -d '{
    "title": "User A Movie",
    "type": "movie",
    "year": 2020
  }'
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 11:23:07 GMT
Content-Type: application/json
Content-Length: 202
Connection: close

{"id":5,"type":"movie","title":"User A Movie","year":2020,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":null,"user_id":3}


# CREATE MEDIA AS USER 2
curl -i \
  -X POST http://localhost:5000/media \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiMjNlODNhMDAtZDA1Mi00YmI4LWI5ODEtN2NiZWVhY2U4OTI2IiwiaWF0IjoxNzk1NTE5NDk5LCJleHAiOjE3OTU1MjY2OTksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.JC7UbNUyfKnWaa5FG2qyZYryR3CnDaURhzuAHeRf2-c" \
  -d '{
    "title": "User B Movie",
    "type": "movie",
    "year": 2021
  }'
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 11:26:26 GMT
Content-Type: application/json
Content-Length: 202
Connection: close

{"id":6,"type":"movie","title":"User B Movie","year":2021,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":null,"user_id":2}


# LIST MEDIA AS USER 3 (ONLY A's MEDIA SHOULD SHOW)
curl -i \
  -X GET http://localhost:5000/media \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiNjQ4ZGY0MDItODE4NC00N2U5LTg3ZDMtYzY4OWFkZmMzZjk0IiwiaWF0IjoxNzk1NTE3NjcxLCJleHAiOjE3OTU1MjQ4NzEsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.tJglB5IOxwdZP7OKXTHBmPIfeiIVPp6BXWephffcA0Q"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 11:28:22 GMT
Content-Type: application/json
Content-Length: 204
Connection: close

[{"id":5,"type":"movie","title":"User A Movie","year":2020,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":null,"user_id":3}]


===================================================================================

# GET MEDIA 5 WITH USER 2
curl -i -X GET "http://127.0.0.1:5000/media/5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiN2JjZTQ5NjUtMWZkOC00NjNkLWE4NWItMTA0OTJkODhkMjc5IiwiaWF0IjoxNzk1NTI4ODU3LCJleHAiOjE3OTU1MzYwNTcsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.wPiXqwXAXlS-nJRIr0FTzrAiMcE9bIS_tvlJc9XIFiI"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 14:02:18 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}

# GET MEDIA 5 WITH USER 2
curl -i -X GET "http://127.0.0.1:5000/media/6" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiN2JjZTQ5NjUtMWZkOC00NjNkLWE4NWItMTA0OTJkODhkMjc5IiwiaWF0IjoxNzk1NTI4ODU3LCJleHAiOjE3OTU1MzYwNTcsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.wPiXqwXAXlS-nJRIr0FTzrAiMcE9bIS_tvlJc9XIFiI"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 14:02:39 GMT
Content-Type: application/json
Content-Length: 202
Connection: close

{"id":6,"type":"movie","title":"User B Movie","year":2021,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":null,"user_id":2}

# GET MEDIA 5 WITH USER 3
curl -i -X GET "http://127.0.0.1:5000/media/5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiNWM3ODc5OTMtYWVhNi00MWU3LWFhMmQtZjQ3NjU0YzYxNjU4IiwiaWF0IjoxNzk1NTI4NjEzLCJleHAiOjE3OTU1MzU4MTMsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.9dQwqhJfvUjuIcVEwANqNTsXmO4b_QwOnOV89EFgwUM"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 13:59:50 GMT
Content-Type: application/json
Content-Length: 202
Connection: close

{"id":5,"type":"movie","title":"User A Movie","year":2020,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":null,"user_id":3}

# GET MEDIA 6 WITH USER 3
curl -i -X GET "http://127.0.0.1:5000/media/6" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiNWM3ODc5OTMtYWVhNi00MWU3LWFhMmQtZjQ3NjU0YzYxNjU4IiwiaWF0IjoxNzk1NTI4NjEzLCJleHAiOjE3OTU1MzU4MTMsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.9dQwqhJfvUjuIcVEwANqNTsXmO4b_QwOnOV89EFgwUM"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 14:00:13 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}


============================================================================
# TEST UPDATE AND DELETE MEDIA (TOKENS ARE DIFF BECAUSE UPDATE TESTED AFTER CREATE)
user 2 erica = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiOGM3OTNjMDYtOTIxYy00Njc0LWJiZmYtYjkwZDU1ZmZjMjFiIiwiaWF0IjoxNzk1NTYyMzk1LCJleHAiOjE3OTU1Njk1OTUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.kNXL--9PxPgpPTz5FxHkAmmWcEZFKwuK5u0suFvH8Co

curl -X POST "http://127.0.0.1:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"erica\", \"password\": \"Pa55w0rd\"}"
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiOGM3OTNjMDYtOTIxYy00Njc0LWJiZmYtYjkwZDU1ZmZjMjFiIiwiaWF0IjoxNzk1NTYyMzk1LCJleHAiOjE3OTU1Njk1OTUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.kNXL--9PxPgpPTz5FxHkAmmWcEZFKwuK5u0suFvH8Co"
}

user 3 jerry = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU

curl -X POST "http://127.0.0.1:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"jerry\", \"password\": \"Pa55w0rd\"}"
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"
}

# CREATE MEDIA AS USER 3
curl -i -X POST http://localhost:5000/media   \
-H "Content-Type: application/json"   \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"   \
-d '{
    "title": "User A Movie",
    "type": "movie",
    "year": 2020
  }'
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:28:23 GMT
Content-Type: application/json
Content-Length: 199
Connection: close

{"id":5,"type":"movie","title":"User A Movie","year":2020,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":5,"user_id":3}


# CREATE MEDIA AS USER 2
curl -i -X POST http://localhost:5000/media \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiOGM3OTNjMDYtOTIxYy00Njc0LWJiZmYtYjkwZDU1ZmZjMjFiIiwiaWF0IjoxNzk1NTYyMzk1LCJleHAiOjE3OTU1Njk1OTUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.kNXL--9PxPgpPTz5FxHkAmmWcEZFKwuK5u0suFvH8Co" \
  -d '{
    "title": "User B Movie",
    "type": "movie",
    "year": 2021
  }'
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:28:57 GMT
Content-Type: application/json
Content-Length: 199
Connection: close

{"id":6,"type":"movie","title":"User B Movie","year":2021,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":6,"user_id":2}



# READ MEDIA 5 USER 2
curl -i -X GET "http://127.0.0.1:5000/media/5" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:43:29 GMT
Content-Type: application/json
Content-Length: 199
Connection: close

{"id":5,"type":"movie","title":"User A Movie","year":2020,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":5,"user_id":3}



# READ MEDIA 6 USER 2
curl -i -X GET "http://127.0.0.1:5000/media/6" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:43:48 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}



# READ MEDIA 5 USER 3
curl -i -X GET "http://127.0.0.1:5000/media/5" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:44:07 GMT
Content-Type: application/json
Content-Length: 199
Connection: close

{"id":5,"type":"movie","title":"User A Movie","year":2020,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":5,"user_id":3}



# READ MEDIA 6 AS USER 3
curl -i -X GET "http://127.0.0.1:5000/media/6" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:44:25 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}





# UPDATE MEDIA 5 (OWNED BY 3) WITH USER 2 "erica"
curl -i -X PATCH "http://127.0.0.1:5000/media/5" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiOGM3OTNjMDYtOTIxYy00Njc0LWJiZmYtYjkwZDU1ZmZjMjFiIiwiaWF0IjoxNzk1NTYyMzk1LCJleHAiOjE3OTU1Njk1OTUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.kNXL--9PxPgpPTz5FxHkAmmWcEZFKwuK5u0suFvH8Co" \
-H "Content-Type: application/json" \
-d "{\"year\": 1972}"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:29:21 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}


# UPDATE MEDIA 6 (OWNED BY 2) WITH USER 2 "erica"
curl -i -X PATCH "http://127.0.0.1:5000/media/6" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiOGM3OTNjMDYtOTIxYy00Njc0LWJiZmYtYjkwZDU1ZmZjMjFiIiwiaWF0IjoxNzk1NTYyMzk1LCJleHAiOjE3OTU1Njk1OTUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.kNXL--9PxPgpPTz5FxHkAmmWcEZFKwuK5u0suFvH8Co" \
-H "Content-Type: application/json" \
-d "{\"year\": 1972}"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:29:50 GMT
Content-Type: application/json
Content-Length: 199
Connection: close

{"id":6,"type":"movie","title":"User B Movie","year":1972,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":6,"user_id":2}


# UPDATE MEDIA 6 (OWNED BY 2) WITH USER 3 "jerry"
curl -i -X PATCH "http://127.0.0.1:5000/media/6" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU" \
-H "Content-Type: application/json" \
-d "{\"year\": 1973}"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:30:20 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}


# UPDATE MEDIA 5 (OWNED BY 3) WITH USER 3 "jerry"
curl -i -X PATCH "http://127.0.0.1:5000/media/5" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU" \
-H "Content-Type: application/json" \
-d "{\"year\": 1973}"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:30:58 GMT
Content-Type: application/json
Content-Length: 199
Connection: close

{"id":5,"type":"movie","title":"User A Movie","year":1973,"duration":null,"certificate":null,"genres":null,"description":null,"imdb_id":null,"tmdb_id":null,"wiki_id":null,"catalog_id":5,"user_id":3}


# DELETE MEDIA 5 (OWNED BY 3) WITH USER 2 "erica"
curl -i -X DELETE "http://127.0.0.1:5000/media/5" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiOGM3OTNjMDYtOTIxYy00Njc0LWJiZmYtYjkwZDU1ZmZjMjFiIiwiaWF0IjoxNzk1NTYyMzk1LCJleHAiOjE3OTU1Njk1OTUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.kNXL--9PxPgpPTz5FxHkAmmWcEZFKwuK5u0suFvH8Co"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:31:17 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}


# DELETE MEDIA 6 (OWNED BY 2) WITH USER 3 "jerry"
curl -i -X DELETE "http://127.0.0.1:5000/media/6" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:31:38 GMT
Content-Type: application/json
Content-Length: 28
Connection: close

{"error":"media not found"}


# DELETE MEDIA 6 (OWNED BY 2) WITH USER 2 "erica"
curl -i -X DELETE "http://127.0.0.1:5000/media/6" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiOGM3OTNjMDYtOTIxYy00Njc0LWJiZmYtYjkwZDU1ZmZjMjFiIiwiaWF0IjoxNzk1NTYyMzk1LCJleHAiOjE3OTU1Njk1OTUsInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.kNXL--9PxPgpPTz5FxHkAmmWcEZFKwuK5u0suFvH8Co"
HTTP/1.1 204 NO CONTENT
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:32:00 GMT
Content-Type: text/html; charset=utf-8
Connection: close


# DELETE MEDIA 5 (OWNED BY 3) WITH USER 3 "jerry"
curl -i -X DELETE "http://127.0.0.1:5000/media/5" -H "accept: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1UKU"
HTTP/1.1 204 NO CONTENT
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:32:19 GMT
Content-Type: text/html; charset=utf-8
Connection: close


# MALFORMED TOKEN
curl -i -X GET "http://127.0.0.1:5000/media/6" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwianRpIjoiMzA0MzkzMDEtNzc4Mi00YWZlLThlMTAtOGZkZDc2NjJiOTVjIiwiaWF0IjoxNzk1NTYyNDcyLCJleHAiOjE3OTU1Njk2NzIsInVzZXJuYW1lIjoiamVycnkiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.N-0psr7p8BPH3thPHImgYfOmGN3bVo4kenPqGMB1U"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:45:45 GMT
Content-Type: application/json
Content-Length: 26
Connection: close

{"error":"invalid token"}

# AUTH HEADER NO TOKEN
curl -i -X GET "http://127.0.0.1:5000/media/6" -H "accept: application/json" -H "Authorization: Bearer "
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:46:32 GMT
Content-Type: application/json
Content-Length: 26
Connection: close

{"error":"invalid token"}

# NO AUTH HEADER
curl -i -X GET "http://127.0.0.1:5000/media/6" -H "accept: application/json"
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Tue, 24 Nov 2026 23:47:05 GMT
Content-Type: application/json
Content-Length: 54
Connection: close

{"error":"missing or malformed authorization header"}


================================================================================================


$ curl -X GET "http://127.0.0.1:5000/media?page=1&per_page=5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjVkY2UzMWMtMTNhMy00ZjNlLWE4NzktNDM2NGUxNGE5NDk1IiwiaWF0IjoxNzk1NzcwNzY5LCJleHAiOjE3OTU3Nzc5NjksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.XO_jw5-D2Dl9232DzSZOhQnr1iuPzYH22RyUGSmjYtI"

{"media":[{"id":2,"type":"movie","title":"Liger","year":2021,"duration":8400,"certificate":"PG-13","genres":"Action, Drama, Romance","description":"A story about martial arts, dreams and star crossed lovers. Liger is an MMA fighter who trains hard and rises up the ranks with one goal in mind, to fight like his idol, world renowned MMA fighter Mark Anderson and get noticed by him.","imdb_id":"tt4435072","tmdb_id":"787163","wiki_id":"Liger","catalog_id":2,"user_id":2},{"id":5,"type":"movie","title":"Interstellar","year":2014,"duration":10140,"certificate":"PG-13","genres":"Adventure, Drama, Sci-Fi","description":"A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.","imdb_id":"tt0816692","tmdb_id":"157336-interstellar","wiki_id":"Interstellar_(film)","catalog_id":5,"user_id":2},{"id":7,"type":"movie","title":"The Shawshank Redemption","year":1994,"duration":8520,"certificate":"R","genres":"Drama","description":"Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.","imdb_id":"tt0111161","tmdb_id":"278-the-shawshank-redemption","wiki_id":"The_Shawshank_Redemption","catalog_id":7,"user_id":2},{"id":12,"type":"movie","title":"Spirited Away","year":2001,"duration":7500,"certificate":"PG","genres":"Animation, Adventure, Family","description":"During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.","imdb_id":"tt0245429","tmdb_id":"129-spirited-away","wiki_id":"Spirited_Away","catalog_id":12,"user_id":2},{"id":14,"type":"movie","title":"Gladiator","year":2000,"duration":9300,"certificate":"R","genres":"Action, Adventure, Drama","description":"A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.","imdb_id":"tt0172495","tmdb_id":"98-gladiator","wiki_id":"Gladiator_(2000_film)","catalog_id":14,"user_id":2}],"page":1,"per_page":5,"total":18,"pages":4,"total_items":18,"total_pages":4,"has_prev":false,"prev_num":null,"has_next":true,"next_num":2,"prev_url":null,"next_url":"/media?page=2&per_page=5"}


$ curl -X GET "http://127.0.0.1:5000/media?page=4&per_page=5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjVkY2UzMWMtMTNhMy00ZjNlLWE4NzktNDM2NGUxNGE5NDk1IiwiaWF0IjoxNzk1NzcwNzY5LCJleHAiOjE3OTU3Nzc5NjksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.XO_jw5-D2Dl9232DzSZOhQnr1iuPzYH22RyUGSmjYtI"

{"media":[{"id":47,"type":"movie","title":"There Will Be Blood","year":2007,"duration":9480,"certificate":"R","genres":"Drama","description":"A story of family, religion, hatred, oil and madness, focusing on a turn-of-the-century prospector in the early days of the business.","imdb_id":"tt0469494","tmdb_id":"7345-there-will-be-blood","wiki_id":"There_Will_Be_Blood","catalog_id":47,"user_id":2},{"id":49,"type":"movie","title":"Memento","year":2000,"duration":6780,"certificate":"R","genres":"Mystery, Thriller","description":"A man with short-term memory loss attempts to track down his wife's murderer.","imdb_id":"tt0209144","tmdb_id":"77-memento","wiki_id":"Memento_(film)","catalog_id":49,"user_id":2},{"id":51,"type":"movie","title":"Good Will Hunting","year":1997,"duration":7560,"certificate":"R","genres":"Drama, Romance","description":"Will Hunting, a janitor at M.I.T., has a gift for mathematics, but needs help from a psychologist to find direction in his life.","imdb_id":"tt0119217","tmdb_id":"489-good-will-hunting","wiki_id":"Good_Will_Hunting","catalog_id":51,"user_id":2}],"page":4,"per_page":5,"total":18,"pages":4,"total_items":18,"total_pages":4,"has_prev":true,"prev_num":3,"has_next":false,"next_num":null,"prev_url":"/media?page=3&per_page=5","next_url":null}


$ curl -X GET "http://127.0.0.1:5000/media?page=5&per_page=5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjVkY2UzMWMtMTNhMy00ZjNlLWE4NzktNDM2NGUxNGE5NDk1IiwiaWF0IjoxNzk1NzcwNzY5LCJleHAiOjE3OTU3Nzc5NjksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.XO_jw5-D2Dl9232DzSZOhQnr1iuPzYH22RyUGSmjYtI"

{"media":[],"page":5,"per_page":5,"total":18,"pages":4,"total_items":18,"total_pages":4,"has_prev":true,"prev_num":4,"has_next":false,"next_num":null,"prev_url":"/media?page=4&per_page=5","next_url":null}


$ curl -X GET "http://127.0.0.1:5000/media?per_page=999" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjVkY2UzMWMtMTNhMy00ZjNlLWE4NzktNDM2NGUxNGE5NDk1IiwiaWF0IjoxNzk1NzcwNzY5LCJleHAiOjE3OTU3Nzc5NjksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.XO_jw5-D2Dl9232DzSZOhQnr1iuPzYH22RyUGSmjYtI"

{"error":"per_page must be a number between 1 and 400"}


$ curl -X GET "http://127.0.0.1:5000/media?page=<last_page>&per_page=5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjVkY2UzMWMtMTNhMy00ZjNlLWE4NzktNDM2NGUxNGE5NDk1IiwiaWF0IjoxNzk1NzcwNzY5LCJleHAiOjE3OTU3Nzc5NjksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.XO_jw5-D2Dl9232DzSZOhQnr1iuPzYH22RyUGSmjYtI"

{"media":[{"id":2,"type":"movie","title":"Liger","year":2021,"duration":8400,"certificate":"PG-13","genres":"Action, Drama, Romance","description":"A story about martial arts, dreams and star crossed lovers. Liger is an MMA fighter who trains hard and rises up the ranks with one goal in mind, to fight like his idol, world renowned MMA fighter Mark Anderson and get noticed by him.","imdb_id":"tt4435072","tmdb_id":"787163","wiki_id":"Liger","catalog_id":2,"user_id":2},{"id":5,"type":"movie","title":"Interstellar","year":2014,"duration":10140,"certificate":"PG-13","genres":"Adventure, Drama, Sci-Fi","description":"A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.","imdb_id":"tt0816692","tmdb_id":"157336-interstellar","wiki_id":"Interstellar_(film)","catalog_id":5,"user_id":2},{"id":7,"type":"movie","title":"The Shawshank Redemption","year":1994,"duration":8520,"certificate":"R","genres":"Drama","description":"Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.","imdb_id":"tt0111161","tmdb_id":"278-the-shawshank-redemption","wiki_id":"The_Shawshank_Redemption","catalog_id":7,"user_id":2},{"id":12,"type":"movie","title":"Spirited Away","year":2001,"duration":7500,"certificate":"PG","genres":"Animation, Adventure, Family","description":"During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.","imdb_id":"tt0245429","tmdb_id":"129-spirited-away","wiki_id":"Spirited_Away","catalog_id":12,"user_id":2},{"id":14,"type":"movie","title":"Gladiator","year":2000,"duration":9300,"certificate":"R","genres":"Action, Adventure, Drama","description":"A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.","imdb_id":"tt0172495","tmdb_id":"98-gladiator","wiki_id":"Gladiator_(2000_film)","catalog_id":14,"user_id":2}],"page":1,"per_page":5,"total":18,"pages":4,"total_items":18,"total_pages":4,"has_prev":false,"prev_num":null,"has_next":true,"next_num":2,"prev_url":null,"next_url":"/media?page=2&per_page=5"}



$ curl -X GET "http://127.0.0.1:5000/media?page=<last_page+1>&per_page=5" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiNjVkY2UzMWMtMTNhMy00ZjNlLWE4NzktNDM2NGUxNGE5NDk1IiwiaWF0IjoxNzk1NzcwNzY5LCJleHAiOjE3OTU3Nzc5NjksInVzZXJuYW1lIjoiZXJpY2EiLCJyb2xlIjoidXNlciIsImlzX2FkbWluIjpmYWxzZX0.XO_jw5-D2Dl9232DzSZOhQnr1iuPzYH22RyUGSmjYtI"

{"media":[{"id":2,"type":"movie","title":"Liger","year":2021,"duration":8400,"certificate":"PG-13","genres":"Action, Drama, Romance","description":"A story about martial arts, dreams and star crossed lovers. Liger is an MMA fighter who trains hard and rises up the ranks with one goal in mind, to fight like his idol, world renowned MMA fighter Mark Anderson and get noticed by him.","imdb_id":"tt4435072","tmdb_id":"787163","wiki_id":"Liger","catalog_id":2,"user_id":2},{"id":5,"type":"movie","title":"Interstellar","year":2014,"duration":10140,"certificate":"PG-13","genres":"Adventure, Drama, Sci-Fi","description":"A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.","imdb_id":"tt0816692","tmdb_id":"157336-interstellar","wiki_id":"Interstellar_(film)","catalog_id":5,"user_id":2},{"id":7,"type":"movie","title":"The Shawshank Redemption","year":1994,"duration":8520,"certificate":"R","genres":"Drama","description":"Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.","imdb_id":"tt0111161","tmdb_id":"278-the-shawshank-redemption","wiki_id":"The_Shawshank_Redemption","catalog_id":7,"user_id":2},{"id":12,"type":"movie","title":"Spirited Away","year":2001,"duration":7500,"certificate":"PG","genres":"Animation, Adventure, Family","description":"During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.","imdb_id":"tt0245429","tmdb_id":"129-spirited-away","wiki_id":"Spirited_Away","catalog_id":12,"user_id":2},{"id":14,"type":"movie","title":"Gladiator","year":2000,"duration":9300,"certificate":"R","genres":"Action, Adventure, Drama","description":"A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.","imdb_id":"tt0172495","tmdb_id":"98-gladiator","wiki_id":"Gladiator_(2000_film)","catalog_id":14,"user_id":2}],"page":1,"per_page":5,"total":18,"pages":4,"total_items":18,"total_pages":4,"has_prev":false,"prev_num":null,"has_next":true,"next_num":2,"prev_url":null,"next_url":"/media?page=2&per_page=5"}


================================================================================================
