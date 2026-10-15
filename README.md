# La lista de Vega

Lista de compras compartida de la familia para la llegada de Vega (abril de 2027).
Web: https://drodridavid.github.io/lista-vega/ (con contraseña).

## Cómo funciona

- `index.html` es la web publicada. Lleva la lista **cifrada**: sin contraseña no se lee.
- Lo que marca la familia (lo que ya está, quién regala qué, los enlaces, las notas y las cosas
  añadidas) se guarda **cifrado** en `estado.txt` de la rama `datos`. Cada móvil lo lee y lo
  escribe directamente en GitHub y comprueba si hay cambios cada 15 segundos.
- La familia solo consulta: lee `estado.txt` sin token (el repositorio es público).
- El administrador entra en ⋯ → Modo admin con la clave de administrador. Esa clave descifra
  el token de grano fino (solo este repositorio, Contents: lectura y escritura), que se guarda
  en su navegador hasta que sale del modo admin. El token y la clave están en `datos.json`,
  que no se sube.

## Hacer cambios en la lista base

1. Editar `datos.json` (no está en git) o `plantilla.html` (el diseño y la lógica).
2. Ejecutar `.\publicar.ps1 "qué he cambiado"`.

`sal.txt` no se puede cambiar ni borrar: si cambia, la lista compartida deja de poder leerse.
Lo mismo pasa si cambia la contraseña.

## Enlaces

- En modo admin: botón **🔗 Añadir enlace**, el ✎ de cada cosa (con 📋 para pegar y precio),
  o pegar el enlace directamente en «Añadir algo más…». El nombre y la foto del producto se
  intentan rellenar solos con microlink.io; algunas tiendas no lo permiten.
- **Compartir desde el móvil (Android):** instala la web como app (menú de Chrome → «Instalar
  app» o «Añadir a pantalla de inicio») y luego, en Amazon, IKEA, etc., Compartir → Vega.
- **Enlaces útiles:** sección para la lista de nacimiento, tiendas o guías.
- La familia ve los enlaces como botones o tarjetas con foto, y «🔍 Buscar» en lo que no tiene enlace.
