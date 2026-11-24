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
