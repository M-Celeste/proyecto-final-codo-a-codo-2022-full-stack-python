# Verificación

Comprobaciones realizadas el 8 de noviembre de 2026:

- MySQL 8.0.43 en una instancia temporal aislada, puerto 13316. No se modificó
  el servicio MySQL80 existente ni las bases del usuario.
- Ejecución real de 01_schema.sql y 02_seed.sql. Segunda importación de los datos
  sin duplicados: 4 categorías y 6 plantas.
- Ocho rutas HTML y página 404 verificadas con el cliente de pruebas de Flask.
- Recursos estáticos servidos correctamente. Bootstrap cargado solo en contacto.
- CRUD real de plantas y categorías: altas, consultas, cambios y bajas.
- Búsqueda, filtros por categoría, disponibles y destacadas.
- Rechazo de precios negativos/no finitos/con más de dos decimales; stock negativo
  o fraccionario; categoría inválida; nombre vacío; URL de imagen no permitida y
  valor de destacada no booleano.
- Categorías duplicadas y eliminación de categorías con plantas: respuesta 409.
- Consultas parametrizadas comprobadas con una búsqueda que contiene texto SQL.
- Restricciones CHECK de precio y stock comprobadas directamente en MySQL.
- Sintaxis de los cuatro archivos JavaScript comprobada con node --check.

La instancia temporal se apagó después de las pruebas.

## Puesta en marcha local

El 8 de noviembre de 2026 se creó la base en el servicio MySQL80 del usuario,
utilizando la conexión guardada de Workbench. Se configuró un usuario exclusivo
para la aplicación y se comprobó la lectura de 6 plantas y 4 categorías.
Flask quedó disponible en http://127.0.0.1:5000. En el navegador se comprobó que
Vue carga el catálogo y que buscar Monstera deja únicamente esa planta.

Pendiente: revisión visual exhaustiva en distintos tamaños, interacción del
formulario de contacto y preparación del despliegue público.

## Recorrido manual con MySQL

1. Importar el esquema y los datos. Confirmar 4 categorías y 6 plantas.
2. Abrir inicio, catálogo, detalle y contacto.
3. Buscar Monstera; filtrar Aromáticas y activar Solo disponibles.
4. Crear una categoría y una planta de prueba. Comprobar su detalle público.
5. Editar nombre, stock, precio y destacada. Ver los cambios en inicio y catálogo.
6. Intentar borrar una categoría con plantas: debe responder 409 y conservarla.
7. Borrar la planta de prueba y luego su categoría.
8. Comprobar rechazo de precio negativo, stock fraccionario y categoría inexistente.
9. Probar contacto con campos vacíos y luego válidos: no debe enviar correos.
10. Revisar teclado y pantallas de 375, 576, 768, 1024 y 1440 px.

## Renovación visual y fotos

- Siete fotografías locales con autores y licencias registrados (seis plantas e invernadero).
- Comprobadas las seis rutas de imagen y la nueva página de créditos.
- Búsqueda de Monstera: una tarjeta; limpiar filtros: seis tarjetas.
- Acceso Interior desde la portada: Monstera y Potus.
- Ficha de Monstera con fotografía real.
- Sin desbordamiento horizontal en las vistas revisadas de 375, 768 y 1280 px.
- Revisadas portada móvil y escritorio, catálogo y ficha en tablet.
- Bootstrap continúa cargándose únicamente en contacto.

## Revisión de tarjetas del catálogo

- Revisadas las seis tarjetas a 1280 y 375 px, sin desbordamiento horizontal.
- Se reemplazó la foto oscura de Monstera por una referencia más clara de Raul654 (CC BY-SA 3.0), con créditos actualizados.
- Disponibilidad separada del enlace de imagen para que el texto también sea accesible.
- Etiquetas de stock y cuidados con mayor legibilidad; mejor encuadre de Echeveria.
- Las seis fotos cargan y los tres enlaces de cada tarjeta apuntan a su misma ficha.
- Solo disponibles muestra cinco plantas y excluye Albahaca; limpiar devuelve seis.
- Las seis fichas y fotos responden HTTP 200.
