"""
Usage:
- Run app: python main.py
"""
import uvicorn
import socket
from app.logger import logger

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    local_ip = get_local_ip()

    logger.info(f"Server starting. Access the API at:")
    logger.info(f"Local:   \033[94mhttp://localhost:{port}\033[0m")
    logger.info(f"Network: \033[94mhttp://{local_ip}:{port}\033[0m")
    logger.info("Click on the links above to open in your browser.")
    logger.info("Press CTRL+C to stop the server.")

    uvicorn.run("app.asgi:app", port=port, host=host, reload=True)
