# Publicación gratuita en Vercel

La aplicación Flask se importa desde `app.py`. El proceso de compilación copia
`static/` a `public/static/` para servir CSS, JavaScript y fotografías desde la CDN.
`public/` se genera y no se guarda en Git. No hace falta cambiar las URLs locales.

## Base de datos

Vercel no ejecuta el MySQL de la computadora. Hace falta una base remota.
Una opción es TiDB Cloud Starter gratuito en modo compatible con MySQL; **su motor
es TiDB, no MySQL**. La instalación local mantiene MySQL y los scripts originales.
El plan tiene cuotas y condiciones que se deben revisar al crear la instancia;
no activar facturación ni ampliar a un plan pago para esta demostración.

Crear una base vacía `raiz_celeste` y configurar en Vercel:

| Variable | Valor |
| --- | --- |
| `MYSQL_HOST` | Host del proveedor |
| `MYSQL_PORT` | Puerto del proveedor |
| `MYSQL_USER` | Usuario de la base |
| `MYSQL_PASSWORD` | Contraseña; marcar como sensible |
| `MYSQL_DATABASE` | `raiz_celeste` |
| `MYSQL_SSL` | `true` |
| `PUBLIC_DEMO` | `true` |

El certificado y el nombre del servidor se verifican con las autoridades de
confianza de `certifi`. Si el proveedor necesita una CA propia, indicar la ruta
de su certificado en `MYSQL_SSL_CA`. Nunca desactivar la verificación para
resolver un error de conexión.

Para inicializar **una base remota vacía**, usar una terminal separada con las
variables de esa base y ejecutar desde la raíz del proyecto:

```sh
python -m scripts.init_database
```

El importador omite `CREATE DATABASE` y `USE` y trabaja sobre `MYSQL_DATABASE`.
Crea las tablas y agrega los datos de demostración ausentes. No borra tablas;
los cambios de estructura no son transaccionales en MySQL. Ejecutarlo con un
usuario autorizado para crear el esquema. Para la web es preferible un usuario
limitado a `SELECT` sobre esa base. No importar datos reales de clientes.

## Proyecto en Vercel

1. Usar el plan personal Hobby gratuito.
2. Importar el repositorio de GitHub y elegir la raíz del proyecto (`./`).
3. Verificar el framework Flask; `vercel.json` define el comando de compilación.
4. Cargar las variables de conexión antes del despliegue. No subir `.env`.
5. Publicar y comprobar inicio, catálogo, filtros, detalle y fotografías.
6. Comprobar que `/admin/plantas` devuelve 404 y los cambios de la API, 403.
7. Agregar al README únicamente la URL pública comprobada.

En Vercel el modo de consulta se activa automáticamente. Oculta Gestión y bloquea
las operaciones de escritura de la API antes de acceder a la base, también en
despliegues de vista previa. El CRUD local sigue disponible mientras
`PUBLIC_DEMO=false`. Para habilitar administración remota se requiere incorporar
autenticación y autorización; no basta con ocultar enlaces.

## Estado

Instancia TiDB Cloud Starter creada con compatibilidad MySQL y límite de gasto
de USD 0 al mes, sin tarjeta. Base `raiz_celeste` inicializada y verificada con
4 categorías y 6 plantas de demostración.

La publicación en Vercel y la prueba de conexión desde Flask siguen pendientes
de configurar las credenciales. Todavía no hay una URL pública confirmada.

## Documentación oficial

- [Flask en Vercel](https://vercel.com/docs/frameworks/backend/flask)
- [Plan Hobby](https://vercel.com/docs/plans/hobby)
- [TiDB Cloud Starter y cuotas gratuitas](https://docs.pingcap.com/tidbcloud/select-cluster-tier/)
- [MySQL Connector/Python con TiDB](https://docs.pingcap.com/developer/dev-guide-sample-application-python-mysql-connector/)
