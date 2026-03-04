import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
import socket

class AccessManagerRequestHandler(BaseHTTPRequestHandler):
    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                return
            mname = 'access_manager'
            if not hasattr(self, mname):
                self.send_error(501, "Method not implemented: (%r)" % mname)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush()
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return
    
    def access_manager(self):
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        method()

white_mime = {
    ".html": "text/html",
    ".htm": "text/html",
    ".css": "text/css",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".txt": "text/plain",
    ".pdf": "application/pdf",
    ".zip": "application/zip",  
    ".rar": "application/x-rar-compressed",
    ".mp3": "audio/mpeg",
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".mpeg": "video/mpeg",
    ".webm": "video/webm",
    ".ogg": "audio/ogg",
    ".wav": "audio/wav",
    ".flac": "audio/flac",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
}

class MainHandler(AccessManagerRequestHandler):
    def access_manager(self):
        # Логіка віддачі статичних файлів (виправлена)
        if not self.path.endswith("/") and not "../" in self.path:
            try:            
                dot_index = self.path.rindex(".")
                ext = self.path[dot_index:].lower()
                mime_type = white_mime.get(ext) # Виправлено: .get() та інше ім'я змінної
                if mime_type:
                    fname = "./http/assets" + self.path
                    if os.path.exists(fname):
                        with open(fname, "rb") as file:
                            self.send_response(200, "OK")
                            self.send_header("Content-Type", mime_type)
                            self.end_headers()
                            self.wfile.write(file.read()) 
                        return     
            except:
                pass
        return super().access_manager()


    def do_GET(self):
        # Твій блок парсингу параметрів (збережено без змін)
        parts = self.path.split("?", 1)
        path = parts[0]
        query_string = parts[1] if len(parts) > 1 else None

        parts = path.split("/", 3)
        controller = parts[1].lower() if len(parts) > 1 and len(parts[1]) > 0 else "home"
        action = parts[2].lower() if len(parts) > 2 and len(parts[2]) > 0 else "index"
        id = parts[3] if len(parts) > 3 and len(parts[3]) > 0 else None

        parts = path.split("/", 2)
        service = parts[1].lower() if len(parts) > 1 and len(parts[1]) > 0 else "home"
        service_param = parts[2] if len(parts) > 2 and len(parts[2]) > 0 else None

        query_params = {}
        if query_string != None:
            for key, value in (
                map(
                    lambda x: None if x is None else unquote_plus(x),
                    item.split("=", 1) if "=" in item else [item, None],
                )
                for item in query_string.split("&")
                if len(item) > 0
            ):
                query_params[key] = (
                    value if not key in query_params
                    else [*(query_params[key] if isinstance(query_params[key], (list, tuple)) else [query_params[key]]), value]
                )

        # --- НОВА ЛОГІКА ДЛЯ ДЗ: Таблиця файлів ---
        assets_dir = "./http/assets"
        assets_rows = ""
        if os.path.exists(assets_dir):
            for file in os.listdir(assets_dir):
                ext = os.path.splitext(file)[1].lower()
                if ext in white_mime:
                    example = ""
                    # Приклад для картинок
                    if "image" in white_mime[ext]:
                        example = f'<img src="/{file}" height="40" style="border: 1px solid #ccc">'
                    # Приклад для JSON
                    elif ext == ".json":
                        try:
                            with open(os.path.join(assets_dir, file), "r") as f:
                                content = f.read(400) # Беремо перші 40 символів
                                example = f'<code style="background:#eee; padding:2px;">{content}...</code>'
                        except: example = "[json data]"
                    else:
                        example = f"File: {file}"
                    
                    assets_rows += f"<tr><td>{ext}</td><td>{example}</td></tr>"

        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # HTML контент з твоєю стилістикою та двома таблицями
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; padding: 20px; }}
                table {{ border-collapse: collapse; width: 60%; margin-top: 20px; }}
                th, td {{ border: 1px solid #dddddd; text-align: left; padding: 12px; }}
                th {{ background-color: #f2f2f2; }} 

                # tr, td {{ background-color: lightgreen; }} 
                # tr, td {{ background-color: violet; }} 


                h1, h2 {{ color: #333; }}
                .nav-links {{ margin-bottom: 20px; }}
                .nav-links a {{ 
                    margin-right: 15px; text-decoration: none; color: black; 
                    padding: 5px 10px; border: 1px solid #007bff; border-radius: 4px; 
                }}
                .nav-links a:hover {{ background-color: #007bff; color: white; }}
                .hw-table th {{ background-color: #e3f2fd; }} /* Стиль для таблиці ДЗ */
            </style>
            <link rel="icon" href="Python.png">
        </head>
        <body>
            <h1>Request Details</h1>
            <div class="nav-links">
                <a href="/?">Без параметрів</a>
                <a href="/?x=10&x=20">Масив параметрів (x=10, x=20)</a>
                <a href="/?q=it+step">URL-кодовані параметри</a>
            </div>

            <table>
                <tr><th>Parameter</th><th>Value</th></tr>
                <tr><td><b>Full Path</b></td><td>{self.path}</td></tr>
                <tr><td><b>Base Path</b></td><td>{path}</td></tr>
                <tr><td><b>Controller</b></td><td>{controller}</td></tr>
                <tr><td><b>Action</b></td><td>{action}</td></tr>
                <tr><td><b>ID</b></td><td>{id}</td></tr>
                <tr><td><b>Query String</b></td><td>{query_string}</td></tr>
                <tr><td><b>Query Params</b></td><td>{query_params}</td></tr>
                <tr><td><b>Service</b></td><td>{service}</td></tr>
                <tr><td><b>Service Param</b></td><td>{service_param}</td></tr>
            </table>

            <h2>Відображення дозволених типів (./http/assets)</h2>
            <table class="hw-table">
                <tr><th>Тип</th><th>Приклад</th></tr>
                {assets_rows if assets_rows else "<tr><td colspan='2'>Папка assets порожня або не знайдена</td></tr>"}
            </table>

            <h2>LINK Request</h2>
            <button onclick="sendLink()">Send LINK Request</button>
            <p id="out"></p>

            <script>
                function sendLink() {{
                    fetch('/', {{
                        method: "LINK",
                    }}).then(r => r.text()).then(t => document.getElementById('out').innerText = t);
                }}
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode("utf-8"))

    def do_LINK(self):
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"LINK request received")

def main():
    port = 88
    http_server = HTTPServer(("127.0.0.1", port), MainHandler)
    try:
        print(f"Starting server on port {port}...")
        print(f"http://localhost:{port}")
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()