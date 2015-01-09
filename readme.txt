http://localhost:65010/oauth/authorize?client_id=12345&redirect_uri=ololo.ru

 curl —data "code=***&client_id=12345&client_secret=123456789&redirect_uri=ololo.ru" http://localhost:65010/oauth/token

curl -h "Authorization: Bearer **TOKEN**" **Adress**