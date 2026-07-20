# Docker — Revision Notes

## 1. Container Lifecycle — Basic Commands

Think of an **image** as a *recipe/blueprint*, and a **container** as the *actual running dish* made from that recipe.

| Command | Meaning |
|---|---|
| `docker run <image>` | Create + start a new container from an image. |
| `docker run -d nginx` | Run container in **background** (detached mode) — you get your terminal back immediately. |
| `docker ps` | List **currently running** containers. |
| `docker ps -a` | List **all** containers — running *and* stopped. |
| `docker stop <name/id>` | Stop a running container (gracefully). |
| `docker rm <name/id>` | Remove a stopped container permanently. |
| `docker images` | List all **downloaded/local images**. |
| `docker rmi <name>` | Delete a downloaded image — the image must **not** be running or even stopped as a container first. |
| `docker pull <name>` | Download an image from a registry (like Docker Hub) without running it. |
| `docker exec <id> <command>` | Run a command **inside** an already-running container. |
| `docker system prune` | Clean up unused containers, images, networks in one shot — frees up disk space. |

> Example: `docker exec 538d cat /etc/hosts` → runs `cat /etc/hosts` inside the already-running container with ID starting `538d`, without needing to log into it.

---

## 2. Image Versions (Tags)

Docker images can have different **versions**, called **tags**.
```
docker pull nginx:1.25
```
If you don't specify a tag, Docker defaults to `latest`. Tags let you pin a specific version instead of always getting the newest one.

---

## 3. Running Containers — Common Options

**Interactive Mode**
Lets you actually type commands *into* the container (like opening a terminal inside it).
- `-i` → keeps input open (interactive).
- `-t` → gives you a proper terminal-like display (pseudo-TTY).
- Together: `docker run -it ubuntu bash` → opens an interactive shell inside an Ubuntu container.

**Port Mapping**
Containers run in their own isolated network — port mapping connects a port on your machine to a port inside the container.
```
docker run -p 80:5000 myapp
```
Means: *"traffic hitting port 80 on my computer → forward it to port 5000 inside the container."*
> This also lets you run multiple copies of the same app on different host ports, e.g., `-p 81:5000`, `-p 82:5000`, without them clashing.

**Data Persistence (Volumes)**
Containers are **temporary** by default — delete the container, lose the data inside it. Volumes solve this by linking a folder on your real machine to a folder inside the container.
```
docker run -v /opt/datadir:/var/lib/mysql mysql
```
or the newer, more explicit syntax:
```
docker run --mount type=bind,source=/opt/datadir,target=/var/lib/mysql mysql
```
Both do the same thing: keep your database's data safe on your host machine even if the container is removed.

---

## 4. Inspecting Containers

- `docker logs <name/id>` → view the console/output logs of a container (great for debugging).
- `docker inspect <name/id>` → get **detailed JSON info** about a container (its IP address, mounted volumes, config, etc.).

---

## 5. Building Your Own Docker Image

To create a **custom image**, you typically need to define:
1. Base **operating system**
2. **Update** package repositories
3. **Install** required software (e.g., Flask)
4. **Copy** your source code in
5. Set **environment variables**
6. Command to **run the app/web server**

All of this is written in a file called a **Dockerfile**.

```dockerfile
FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3-flask
COPY app.py /opt/app.py
ENV FLASK_APP=/opt/app.py
ENTRYPOINT flask run --host=0.0.0.0
```

**Build & Push commands:**
- `docker build -t myapp .` → build an image from the Dockerfile in the current folder, tag it `myapp`.
- `docker push myapp` → upload your image to a registry (like Docker Hub) so others (or servers) can pull it.

**Layered Architecture**
Each line in a Dockerfile creates a **layer**. Docker caches these layers — if a layer hasn't changed, it reuses it instead of redoing the work, which makes rebuilds **faster**.
- `docker history <image>` → shows all the layers that make up an image and their sizes.

---

## 6. Problems With the Traditional Build Approach

- **Repeated downloads** — packages get re-downloaded on every build even if nothing changed.
- **Secret leaks** — sensitive data (like API keys) used during build can accidentally get baked into the image layers.
- **Architecture lock-in** — an image built for one CPU architecture (e.g., Intel) won't easily run on another (e.g., ARM/Mac M1).
- **Sequential builds** — build steps run one after another even when some of them could run at the same time, wasting time.

---

## 7. The Solution — BuildKit

**BuildKit** is Docker's smarter, modern build engine that fixes the problems above.

- **Smarter Caching** — reuses layers more intelligently, skipping unnecessary rework.
- **buildx plugin** — the tool/plugin that gives access to BuildKit's extra features.
- **Cache Mounts** — lets a build step (like package downloads) reuse a *persistent* cache across builds, so the packages aren't re-downloaded every single time.
  ```dockerfile
  # syntax=docker/dockerfile:1
  RUN --mount=type=cache,target=/var/cache/apt apt-get update
  ```
  First build downloads packages normally; later builds pull from the **local cache** instead.
- **Secret Mounts** — mounts a secret file (like a password) temporarily, only for the one command that needs it, then **unmounts it** — so it never gets saved into the image layers.
- **Multi-platform Builds** — build one image that works on **both Intel and ARM** chips in a single command.
- **Parallel Stage Execution** — independent build stages can now run **at the same time** instead of waiting on each other, saving build time.

---

## 8. Scaffolding a New Project

**`docker init`** — a command that auto-generates the standard files you need to Dockerize a project:
- `Dockerfile`
- `.dockerignore` (files to exclude from the build, like `node_modules`)
- `compose.yaml`
- A `README`/`DOCKER.md` with usage instructions

Great starting point instead of writing all these files by hand.

---

## 9. CMD vs ENTRYPOINT

Both define what runs when the container starts, but with a subtle difference:

- **ENTRYPOINT** — the *fixed* main command that always runs when the container starts (like the "main job" of the container).
- **CMD** — provides *default arguments*, which can be easily overridden when you run the container.

> Simple way to remember: ENTRYPOINT = "what to run", CMD = "default extra options/arguments for it."
Environment variables (`ENV`) are also commonly used here to configure behavior without hardcoding values into the command.

---

## 10. Docker Compose

When your app needs **multiple containers** working together (e.g., a web app + a database), manually running `docker run` for each gets messy. **Docker Compose** solves this by describing your whole multi-container setup in **one file**.

- **`compose.yaml`** — the file where you define all your services (containers), their images, ports, volumes, and networks.
- **`docker compose ...`** — the current command to manage this (older versions used `docker-compose` as a separate tool; now it's built into the `docker` CLI).
- **User-defined Networks** — Compose automatically creates a private network so your containers can talk to each other by name — you don't have to set this up manually.
- **Compose Specification** — the official standard/format that defines what's allowed inside a `compose.yaml` file.
- **Networks (e.g., frontend, backend)** — you can define **multiple separate networks** in Compose, so e.g. your database is only reachable by your backend service, not directly exposed to the frontend — better isolation and security.

---

### Quick Recap Table

| Term | One-liner |
|---|---|
| `docker run` | Create & start a container from an image |
| `docker ps -a` | Show all containers, running or stopped |
| `docker rmi` | Delete a downloaded image (must not be in use) |
| `-p host:container` | Map a host port to a container port |
| `-v` / `--mount` | Persist data outside the container |
| Dockerfile | Recipe to build a custom image |
| Layered Architecture | Each Dockerfile step = a cached layer |
| BuildKit | Modern, faster, smarter Docker build engine |
| Cache/Secret Mounts | Reuse cache & safely use secrets during build |
| `docker init` | Auto-generate starter Docker project files |
| ENTRYPOINT vs CMD | Fixed main command vs overridable default args |
| Docker Compose | Manage multi-container apps with one YAML file |

