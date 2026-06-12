import http.server
import os
import cgi

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Upload Image</title>
<style>body{font-family:sans-serif;padding:2rem;max-width:500px;margin:auto}
h1{color:#0D9488}input{margin:1rem 0}
.btn{background:#0D9488;color:#fff;padding:0.6rem 1.5rem;border:0;border-radius:8px;cursor:pointer}
</style></head><body>
<h1>Enviar imagem</h1>
<form method="post" enctype="multipart/form-data">
<input type="file" name="file" accept="image/*" required><br>
<button class="btn" type="submit">Upload</button>
</form>
<p style="color:#64748B;font-size:0.85rem">Formatos: PNG, JPG, WebP</p>
</body></html>'''
            self.wfile.write(html.encode())
        else:
            super().do_GET()

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
        if 'file' in form:
            item = form['file']
            if item.filename:
                safe = ''.join(c for c in item.filename if c.isalnum() or c in '._-')
                path = os.path.join(UPLOAD_DIR, safe)
                with open(path, 'wb') as f:
                    f.write(item.file.read())
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                msg = f'✅ <b>{safe}</b> enviado!<br><br>URL: <code>/images/{safe}</code><br><br><a href="/">Voltar</a>'
                self.wfile.write(msg.encode())
                return
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'Erro: selecione um arquivo.')

http.server.HTTPServer(('', 8083), UploadHandler).serve_forever()
