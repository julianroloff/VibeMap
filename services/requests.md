#register user:

##request:
curl -X POST "https://vibemapbe.com/auth/auth/register" -H "Content-Type: application/json" -d '{
  "email": "test2@mail.com",
  "password": "pass",
  "profilePicture": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAQABADASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AJUA/9k=",
  "username": "test"
}'

##response:
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ29AbWFpbC5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDE1MzExNzJ9.Cg7h0K0n1yDJ8KbvRxPMKoklhTV3OZS806kMrfsAQeI","token_type":"bearer"}



#login:
##request:
curl -X POST "https://vibemapbe.com/auth/auth/login" -H "Content-Type: application/json" -d '{
    "email": "test@mail.com",
    "password": "test"
}'

##response:
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ29AbWFpbC5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDE1MzE1MDN9.H2WMliHsnTt1t4GVTEhBK_VWdoQoofwWOgS7UKfQTLs","token_type":"bearer"}


#Checking which user email and id:

##request:
curl -X GET "https://vibemapbe.com/auth/auth/me" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QG1haWwuY29tIiwidXNlcl9pZCI6NCwiZXhwIjoxNzQxODE1OTUyfQ.KncMkUUUF93V3dSt5TjAhic7iQdQv5jE2BzOEyj5y6w"

##response:
{"username":"test","email":"test@mail.com","id":4,"profilePicture":null}

##Creating a location with user token:

curl -X POST "https://vibemapbe.com/location/location/locations/" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ28yQG1haWwuY29tIiwidXNlcl9pZCI6MSwiZXhwIjoxNzQxODA1OTI2fQ.GgcCONAs-nvYtveA5mW9NhxuuKTG_R54m87GLp7qTLA" \
-H "Content-Type: application/json" \
-d '{
  "latitude": 52.3748725,
  "longitude": 4.9448453,
  "comment": "Good soup",
  "stress_level": 3.5
}'


##Response
{"latitude":52.3748725,"longitude":4.9448453,"stress_level":3.5,"comment":"Good soup","id":5,"user_Id":1}


##Requesting locations created by user

curl -X GET "https://vibemapbe.com/location/location/locations/user/{user_id}"

