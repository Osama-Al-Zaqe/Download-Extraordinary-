"""
MediaFlow — Desktop Media Downloader & Manager
Application Entry Point.

Starts the local FastAPI backend engine and launches the desktop WebView
or default browser interface.
"""

import sys
import os
import time
import socket
import argparse
import threading
import webbrowser
import logging
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MediaFlow.Main")

def find_available_port(start_port: int = 52180, max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            res = sock.connect_ex(("127.0.0.1", port))
            if res != 0:
                return port
    return start_port

def run_server(host: str, port: int):
    """Run uvicorn server."""
    from app.server import create_app
    app = create_app()
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="warning",
        access_log=False
    )
    server = uvicorn.Server(config)
    server.run()

def wait_for_server(host: str, port: int, timeout: float = 10.0) -> bool:
    """Wait until the HTTP server is responsive."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((host, port)) == 0:
                    return True
        except Exception:
            pass
        time.sleep(0.1)
    return False

def main():
    parser = argparse.ArgumentParser(description="MediaFlow - Media Downloader & Manager")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=0, help="Port to bind (default: auto)")
    parser.add_argument("--browser", action="store_true", help="Force opening in default web browser instead of desktop window")
    parser.add_argument("--headless", action="store_true", help="Run server only without launching any GUI or browser")
    args = parser.parse_args()

    port = args.port if args.port > 0 else find_available_port(52180)
    host = args.host
    url = f"http://{host}:{port}"

    logger.info(f"Starting MediaFlow backend at {url}...")

    # Start FastAPI server in background thread
    server_thread = threading.Thread(target=run_server, args=(host, port), daemon=True)
    server_thread.start()

    if not wait_for_server(host, port, timeout=12.0):
        logger.error("Failed to start MediaFlow backend server in time.")
        sys.exit(1)

    logger.info(f"MediaFlow engine is running successfully at {url}")

    if args.headless:
        logger.info("Running in headless mode. Press Ctrl+C to terminate.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Exiting...")
            sys.exit(0)

    # Launch UI
    use_webview = False
    if not args.browser:
        try:
            import webview
            use_webview = True
        except ImportError:
            use_webview = False

    if use_webview:
        try:
            import webview
            logger.info("Launching desktop window...")
            window = webview.create_window(
                title="MediaFlow",
                url=url,
                width=1200,
                height=800,
                min_size=(900, 600),
                text_select=True,
                confirm_close=False
            )
            webview.start()
            logger.info("Desktop window closed. Exiting MediaFlow.")
            sys.exit(0)
        except Exception as e:
            logger.warning(f"Could not open native WebView window ({e}), falling back to browser.")
            use_webview = False

    if not use_webview:
        logger.info("Opening default web browser...")
        webbrowser.open(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Exiting MediaFlow.")
            sys.exit(0)

if __name__ == "__main__":
    main()
