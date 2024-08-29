# <p align="center">FastApi - Celery - Redis</p>
  ## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/) 
- [Firebase](https://firebase.google.com/)
- [Celery](https://derlin.github.io/introduction-to-fastapi-and-celery/)
- [Redis](https://redis.io/fr/) 
- [Nginx](https://nginx.org/en/docs/)
- [Mkcert](https://github.com/FiloSottile/mkcert)
<hr>

Retrieve your .json file from firebase and put it in the auth folder, the path to the json in docker-compose.yml and in db/firebase.py <br>
For SSL => in folder SSL<br>
```bash
mkcert localhost
```
Then start the project
```bash
docker-compose up --build
```
You can test it: <br>
https://localhost/docs <br>
For authentication you can use:
https://www.firebasejwt.com/
        

## Arnaud Fischer
