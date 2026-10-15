"""Cifra datos.json con la contraseña y genera index.html a partir de plantilla.html.
El token de GitHub no va con la lista: va cifrado aparte con la clave de administrador."""
import base64, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

aqui = os.path.dirname(os.path.abspath(__file__))
clave = (sys.argv[1] if len(sys.argv) > 1 else "vega").strip().lower()
ruta_datos = os.path.join(aqui, "datos.json")
todo = json.load(open(ruta_datos, encoding="utf-8"))
token = todo.pop("token", "")
# La clave de administrador abre el token; si no existe se crea una y se guarda en datos.json
if not todo.get("clave_admin"):
    abc = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    todo["clave_admin"] = "-".join("".join(abc[x % len(abc)] for x in os.urandom(4)) for _ in range(4))
    json.dump(dict(todo, token=token), open(ruta_datos, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# Clave de privado.txt (lo que solo ve el admin). Se crea una vez y no puede cambiar
if not todo.get("clave_privada"):
    todo["clave_privada"] = base64.b64encode(os.urandom(32)).decode()
    json.dump(dict(todo, token=token), open(ruta_datos, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
clave_privada = todo.pop("clave_privada")
clave_admin = todo.pop("clave_admin").strip().lower()
datos = json.dumps(todo, ensure_ascii=False).encode()

# La sal es fija: si cambiara, la clave derivada cambiaría y la lista compartida (estado.txt) dejaría de leerse
ruta_sal = os.path.join(aqui, "sal.txt")
if not os.path.exists(ruta_sal):
    open(ruta_sal, "w").write(base64.b64encode(os.urandom(16)).decode())
sal, iv = base64.b64decode(open(ruta_sal).read().strip()), os.urandom(12)
k = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sal, iterations=200000).derive(clave.encode())
ct = AESGCM(k).encrypt(iv, datos, None)
blob = ".".join(base64.b64encode(x).decode() for x in (sal, iv, ct))

# Contraseña de admin: abre un bloque aparte con el token y la contraseña de familia (sal propia)
sal_a, iv_a = os.urandom(16), os.urandom(12)
k_a = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sal_a, iterations=200000).derive(clave_admin.encode())
admin = ".".join(base64.b64encode(x).decode() for x in (sal_a, iv_a, AESGCM(k_a).encrypt(iv_a, json.dumps({"token": token, "clave": clave, "kpriv": clave_privada}).encode(), None))) if token else ""

html = open(os.path.join(aqui, "plantilla.html"), encoding="utf-8").read()
assert html.count("__ADMIN__") == 1
assert html.count("__CIFRADO__") == 1
open(os.path.join(aqui, "index.html"), "w", encoding="utf-8", newline="\n").write(html.replace("__CIFRADO__", blob).replace("__ADMIN__", admin))
print("index.html generado")
