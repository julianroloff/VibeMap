#register user:

##request:
curl -X POST "http://35.204.6.188/auth/register" -H "Content-Type: application/json" -d '{
    "email": "ago@mail.com",
    "password": "pass"
}'
curl -X POST "https://vibemapbe.com/auth/auth/register" -H "Content-Type: application/json" -d '{
    "email": "ago@mail.com",
    "password": "pass"
}'

##response:
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ29AbWFpbC5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDE1MzExNzJ9.Cg7h0K0n1yDJ8KbvRxPMKoklhTV3OZS806kMrfsAQeI","token_type":"bearer"}



#login:
##request:
curl -X POST "https://vibemapbe.com/auth/auth/login" -H "Content-Type: application/json" -d '{
    "email": "ago@mail.com",
    "password": "pass"
}'

##response:
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ29AbWFpbC5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDE1MzE1MDN9.H2WMliHsnTt1t4GVTEhBK_VWdoQoofwWOgS7UKfQTLs","token_type":"bearer"}


#Checking which user email and id:

##request:
curl -X GET "https://vibemapbe.com/auth/auth/me" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ29AbWFpbC5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDE1MzE1MDN9.H2WMliHsnTt1t4GVTEhBK_VWdoQoofwWOgS7UKfQTLs"

##response:
{"email":"ago@mail.com","id":2}
