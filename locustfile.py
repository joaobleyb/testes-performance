from locust import HttpUser, task, between
import random

class UsuarioAPI(HttpUser):
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 3)

    @task(4)
    def listar_posts(self):
        self.client.get("/posts")

    @task(3)
    def buscar_post(self):
        post_id = random.randint(1, 100)
        self.client.get(f"/posts/{post_id}")

    @task(2)
    def listar_comentarios(self):
        self.client.get("/comments")

    @task(2)
    def criar_post(self):
        self.client.post("/posts", json={
            "title": "Teste",
            "body": "Teste Locust",
            "userId": 1
        })

    @task(1)
    def criar_comentario(self):
        self.client.post("/comments", json={
            "name": "Teste",
            "email": "teste@email.com",
            "body": "Comentário teste",
            "postId": 1
        })