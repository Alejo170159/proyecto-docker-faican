from flask import Flask, request, redirect, render_template_string
import pymysql

app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(
        host='base_datos',
        user='usuario',
        password='password123',
        database='mi_base'
    )

def inicializar_tabla():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS registros (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conexion.commit()
    conexion.close()

HTML_PAGINA = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>App Faican</title>
<style>
body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;padding-top:50px}
.caja{background:#fff;padding:30px;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,.1);width:420px}
h2{color:#1a73e8;margin-top:0}form{display:flex;gap:10px;margin-bottom:20px}
input{flex:1;padding:10px;border:1px solid #ccc;border-radius:5px}
button{padding:10px 15px;background:#1a73e8;color:#fff;border:none;border-radius:5px;cursor:pointer;font-weight:bold}
table{width:100%;border-collapse:collapse}th,td{padding:10px;border-bottom:1px solid #eee;text-align:left}
</style></head><body><div class="caja"><h2>Registro en MariaDB</h2>
<form method="POST" action="/guardar"><input type="text" name="nombre" placeholder="Escribe un dato..." required><button type="submit">Guardar</button></form>
<table><tr><th>ID</th><th>Dato</th><th>Fecha</th></tr>
{% for f in datos %}<tr><td>{{f[0]}}</td><td>{{f[1]}}</td><td>{{f[2]}}</td></tr>{% endfor %}
</table></div></body></html>"""

@app.route('/')
def inicio():
    inicializar_tabla()
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, fecha FROM registros ORDER BY id DESC")
        datos = cursor.fetchall()
    conexion.close()
    return render_template_string(HTML_PAGINA, datos=datos)

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form.get('nombre')
    if nombre:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO registros (nombre) VALUES (%s)", (nombre,))
        conexion.commit()
        conexion.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

