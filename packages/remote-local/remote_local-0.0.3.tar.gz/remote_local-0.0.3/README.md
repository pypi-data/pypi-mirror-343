# remote-local

Expose your local FastAPI, NiceGUI, or development servers remotely — easily, reliably, and for free.

**remote-local** is a simple and robust middleware that automatically creates a public tunnel for your local server using ngrok (and more in the future).  
It handles session cleanup, hot reloads, and retries automatically — no manual setup required.

---

## Features

- 🌍 Expose your local server remotely with **one line of code**.
- ⚡ Fully compatible with **FastAPI**, **NiceGUI**, or any **ASGI app**.
- 🔄 **Handles hot reloads** and session recovery automatically.
- 🔒 **No external configuration** required — works with free ngrok accounts.
- 🛠️ Designed for **development, testing, and remote integrations**.

---

## Installation

```bash
pip install remote-local
```

---

## Quick Usage

```python
from nicegui import app, ui
from remote_local import NgrokMiddleware

NgrokMiddleware(app, port=8080)

@ui.page('/')
async def main_page():
    ui.label('Hello World')

ui.run(port=8080, reload=True)
```

✅ That's it! Your local server is now publicly accessible through a secure URL.

By default, a `/server-info` endpoint is also created, showing the current public URL and server status.

---

## Environment Variable: PUBLIC_URL

If your server is already running with a public URL (for example, in a production deployment), you can set the `PUBLIC_URL` environment variable. When `PUBLIC_URL` is set, the middleware will **skip starting ngrok** and use the provided URL as the public-facing address for your app.

- If `PUBLIC_URL` is set, ngrok will **not** be started and the middleware will simply use this value.
- If `PUBLIC_URL` is not set, the middleware will start ngrok and set the public URL automatically.

Example:

```bash
export PUBLIC_URL=https://your-production-url.example.com
```

---

## Configuration Options

You can customize the middleware:

```python
NgrokMiddleware(
    app,
    port=8080,
    max_wait_seconds=60,    # how long to retry if ngrok fails initially
    fallback_to_localhost=False,  # fallback to localhost if ngrok fails
    expose_server_info=True,      # create a /server-info endpoint
)
```

## Temporary Usage: `temporal_url`

If you need a **temporary public URL** during the execution of a specific task (instead of during the whole app lifecycle), you can use `temporal_url` as a simple context manager.

It will automatically **reuse** the same public URL if called multiple times in parallel, and will **close the tunnel** once all usages are finished.

Example:

```python
from remote_local import temporal_url

@router.post("/external-access")
async def external_access():
    with temporal_url(port=8080) as public_url:
        print(f"My API is now accessible at {public_url}")
        # Perform actions that need external access
    # Tunnel is closed automatically after the block
```

**Notes:**

- `temporal_url` requires specifying the `port` explicitly.
- It automatically kills existing ngrok sessions if needed.
- It's safe to nest multiple `with temporal_url(...)` usages — they will share the same tunnel.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Future Plans

- Support for other tunnels (Cloudflared, Localhost.run, etc.)
- More flexible server info APIs
- Auto-detection of multiple servers

---

## Author

Made with ❤️ by Pablo Schaffner
