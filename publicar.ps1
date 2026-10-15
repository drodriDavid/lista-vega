# Regenera index.html desde datos.json + plantilla.html, lo valida y lo sube a GitHub.
# Uso:  .\publicar.ps1 "qué he cambiado"
param([string]$mensaje = "Actualizar la lista")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python build.py
if ($LASTEXITCODE -ne 0) { throw "Falló build.py" }
$html = Get-Content index.html -Raw -Encoding UTF8
$js = [regex]::Match($html, '(?s)<script>(.*)</script>').Groups[1].Value
$tmp = Join-Path $env:TEMP "lista-vega-check.js"
Set-Content $tmp $js -Encoding UTF8
node --check $tmp
if ($LASTEXITCODE -ne 0) { throw "El JavaScript tiene errores; no se publica" }
git add -A
git commit -m $mensaje
git push
Write-Host "Publicado. En 1-2 minutos estará en https://drodridavid.github.io/lista-vega/"
