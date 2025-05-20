# Simple Facturacion Electronica (Chile)

Este proyecto incluye un conjunto de scripts muy simples para generar DTE, 
construir envíos al SII y emitir respuestas de aceptación o rechazo. **No** 
es un sistema completo ni cumple con todas las especificaciones oficiales, 
solo sirve como ejemplo educativo.

## Estructura de carpetas

```
sf/
  bin/            Scripts de utilidad
  caf/            Archivos CAF (no incluidos)
  templates/      Plantillas de DTE
  dte_recibidos/  DTE obtenidos de intercambio
  dte_emitidos/   DTE generados
  cert/           Certificados (cert.pem y key.pem)
  logs/           Archivos de log
```

## Scripts

- `sf/bin/create_dte.py <archivo.json>`: crea un DTE a partir de un archivo JSON.
- `sf/bin/create_envio.py <dtes...>`: construye un EnvioDTE a partir de uno o más
  DTE generados previamente.
- `sf/bin/respuesta_dte.py <folio> <ACEPTADO|RECHAZADO>`: genera una respuesta
  para un DTE recibido.

Todos los scripts dejan registro de su ejecución en `sf/logs/`.

### Ejemplo de uso

```
./sf/bin/create_dte.py factura.json
./sf/bin/create_envio.py sf/dte_emitidos/dte_33_1844.xml --output envio_1844.xml
./sf/bin/respuesta_dte.py 1844 ACEPTADO --output resp_1844.xml
```

Los archivos `cert.pem` y `key.pem` deben contener el certificado y la clave
privada sin contraseña para poder firmar los documentos.
