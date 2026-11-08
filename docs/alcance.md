# Alcance inicial y consignas

## Modelo de datos

`categorias (1) ─── (N) plantas`

Cada planta pertenece a una categoría. La clave foránea impide categorías
inexistentes y protege a las que tienen plantas. El stock cero representa falta
de disponibilidad; los precios de ejemplo están expresados en pesos argentinos.

## Correspondencia

| Requisito | Ubicación |
|---|---|
| Tres páginas HTML | Inicio, catálogo y contacto, además de detalle y gestión |
| Etiquetas semánticas | Base y plantillas: header, nav, main, section, article, footer |
| Validación JS de contacto | static/js/contacto.js |
| Iframe | Mapa ilustrativo de contacto |
| Íconos | FontAwesome en base e inicio |
| Fuentes | Google Fonts en base |
| Tres puntos de corte | estilos.css: 576, 768 y 1024 px |
| Flexbox/Grid | Navegación, catálogo, detalle y formularios |
| Transición | .plant-card: elevación y sombra al pasar el puntero |
| Bootstrap restringido | Solo contacto.html carga su hoja de estilos |
| Vue | Catálogo, detalle y panel de gestión |
| Python/Flask/MySQL | Paquete raiz_celeste y scripts database |
| CRUD | Plantas y categorías, API y formularios |
| Publicación navegable | Pendiente |

Este mapa usa el TPO de Front-End disponible y la actividad integradora de Back-End
como base de trabajo. No afirma haber recuperado una rúbrica oficial adicional del
final. La evaluación del diseño requiere revisión visual; la publicación se hará
cuando esté listo el proyecto.

## Fuera del alcance inicial

Carrito, pagos, envíos, reservas, carga de archivos, envío real de correos y cuentas
de clientes. La autenticación del administrador se incorporará antes de publicar
el panel. Los recursos externos están enlazados por CDN y no se incluyen descargados.
