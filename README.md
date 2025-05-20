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

### Ejemplo de JSON para `create_dte.py`

```json
{
    "IdDoc": {
        "TipoDTE": "33",
        "Folio": 1844,
        "FchEmis": "2025-05-16"
    },
    "Receptor": {
        "RUTRecep": "61607100-9",
        "RznSocRecep": "SERVICIO DE SALUD CONCEPCION",
        "GiroRecep": "ACTIVIDADES DE LA ADMINISTRACION PUBLICA",
        "Contacto": "Felipe Vargas",
        "CorreoRecep": "fvargas@ssconcepcion.cl",
        "DirRecep": "O HIGGINS 297 CONCEPCION",
        "CmnaRecep": "Concepcion"
    },
    "Totales": {
        "MntNeto": 22765000,
        "MntExe": 0,
        "TasaIVA": 19,
        "IVA": 4325350,
        "MntTotal": 27090350
    },
    "Detalle": [
        {
            "NumLinea": 1,
            "CodItem": "HITO-1282",
            "NombreItem": "CONSULTORIA",
            "DescripcionItem": "Consultoria Adopcion usuaria, Cuota 7. Periodo 16-febrero-2025 a 15-marzo-2025",
            "Cantidad": "1",
            "PrecioU": "14687000",
            "SubTotal": "14687000"
        },
        {
            "NumLinea": 2,
            "CodItem": "HITO-1270",
            "NombreItem": "CONSULTORIA",
            "DescripcionItem": "Servicio de Mesa de Ayuda, Cuota 7. Periodo 16-febrero-2025 a 15-marzo-2025",
            "Cantidad": "1",
            "PrecioU": "8078000",
            "SubTotal": "8078000"
        }
    ],
    "Referencias": [
        {
            "NumLinea": "2",
            "TipoDocRef": "801",
            "FolioRef": "1057432-433-SE24",
            "FchRef": "2025-03-20",
            "RazonRef": "OC"
        }
    ]
}
```


### Ejemplo de uso

```
./sf/bin/create_dte.py factura.json
./sf/bin/create_envio.py sf/dte_emitidos/dte_33_1844.xml --output envio_1844.xml
./sf/bin/respuesta_dte.py 1844 ACEPTADO --output resp_1844.xml
```

Los archivos `cert.pem` y `key.pem` deben contener el certificado y la clave
privada sin contraseña para poder firmar los documentos.
