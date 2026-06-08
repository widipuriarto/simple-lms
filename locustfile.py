from locust import HttpUser, task, between

class SimpleLMSUser(HttpUser):
    # Waktu tunggu simulasi user (jeda 1 sampai 3 detik per request)
    wait_time = between(1, 3)

    @task(3) # Bobot 3: Paling sering diakses
    def view_all_courses(self):
        self.client.get("/api/v1/protected/courses", name="/api/v1/protected/courses")

    @task(2) # Bobot 2: Cukup sering diakses
    def search_courses(self):
        self.client.get("/api/v1/protected/courses?title=python", name="/api/v1/protected/courses (Search)")

    @task(1) # Bobot 1: Paling jarang diakses (mensimulasikan user gagal login berulang)
    def attempt_login(self):
        self.client.post("/api/v1/auth/sign-in", json={"username": "hacker", "password": "salah"}, name="/api/v1/auth/sign-in")
