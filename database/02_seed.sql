-- Datos ficticios para desarrollar la entrega. Precios de demostración.
-- Se puede volver a ejecutar: agrega nombres ausentes y conserva los existentes.
USE raiz_celeste;
START TRANSACTION;

INSERT INTO categorias (nombre, descripcion)
SELECT 'Interior', 'Verde para acompañar los espacios de tu casa.'
WHERE NOT EXISTS (SELECT 1 FROM categorias WHERE nombre = 'Interior');
INSERT INTO categorias (nombre, descripcion)
SELECT 'Exterior', 'Plantas para patios, balcones y jardines.'
WHERE NOT EXISTS (SELECT 1 FROM categorias WHERE nombre = 'Exterior');
INSERT INTO categorias (nombre, descripcion)
SELECT 'Suculentas', 'Una colección de formas y texturas.'
WHERE NOT EXISTS (SELECT 1 FROM categorias WHERE nombre = 'Suculentas');
INSERT INTO categorias (nombre, descripcion)
SELECT 'Aromáticas', 'Aromas y sabores para tu huerta.'
WHERE NOT EXISTS (SELECT 1 FROM categorias WHERE nombre = 'Aromáticas');

INSERT INTO plantas (categoria_id, nombre, nombre_cientifico, descripcion, precio, stock, imagen, luz, riego, destacada)
SELECT c.id, 'Monstera', 'Monstera deliciosa', 'Hojas amplias para un rincón lleno de verde.', 18500, 8, '/static/img/plantas/monstera.jpg', 'Luz indirecta', 'Cuando se seque la capa superior del sustrato', TRUE
FROM categorias c WHERE c.nombre = 'Interior'
AND NOT EXISTS (SELECT 1 FROM plantas WHERE nombre = 'Monstera');
INSERT INTO plantas (categoria_id, nombre, nombre_cientifico, descripcion, precio, stock, imagen, luz, riego, destacada)
SELECT c.id, 'Potus', 'Epipremnum aureum', 'Una planta trepadora para estantes y macetas colgantes.', 6500, 12, '/static/img/plantas/potus.jpg', 'Luz indirecta', 'Moderado, evitando el encharcamiento', TRUE
FROM categorias c WHERE c.nombre = 'Interior'
AND NOT EXISTS (SELECT 1 FROM plantas WHERE nombre = 'Potus');
INSERT INTO plantas (categoria_id, nombre, nombre_cientifico, descripcion, precio, stock, imagen, luz, riego, destacada)
SELECT c.id, 'Lavanda', 'Lavandula angustifolia', 'Flores perfumadas para sumar color al jardín.', 7200, 6, '/static/img/plantas/lavanda.jpg', 'Sol directo', 'Moderado, con buen drenaje', TRUE
FROM categorias c WHERE c.nombre = 'Exterior'
AND NOT EXISTS (SELECT 1 FROM plantas WHERE nombre = 'Lavanda');
INSERT INTO plantas (categoria_id, nombre, nombre_cientifico, descripcion, precio, stock, imagen, luz, riego, destacada)
SELECT c.id, 'Echeveria', 'Echeveria elegans', 'Una suculenta de hojas agrupadas en roseta.', 4200, 15, '/static/img/plantas/echeveria.png', 'Mucha luz', 'Espaciado, con sustrato seco', FALSE
FROM categorias c WHERE c.nombre = 'Suculentas'
AND NOT EXISTS (SELECT 1 FROM plantas WHERE nombre = 'Echeveria');
INSERT INTO plantas (categoria_id, nombre, nombre_cientifico, descripcion, precio, stock, imagen, luz, riego, destacada)
SELECT c.id, 'Romero', 'Salvia rosmarinus', 'Una aromática para empezar tu huerta.', 3500, 9, '/static/img/plantas/romero.jpg', 'Sol directo', 'Moderado', FALSE
FROM categorias c WHERE c.nombre = 'Aromáticas'
AND NOT EXISTS (SELECT 1 FROM plantas WHERE nombre = 'Romero');
INSERT INTO plantas (categoria_id, nombre, nombre_cientifico, descripcion, precio, stock, imagen, luz, riego, destacada)
SELECT c.id, 'Albahaca', 'Ocimum basilicum', 'Hojas frescas y aromáticas para cultivar en maceta.', 2800, 0, '/static/img/plantas/albahaca.jpg', 'Buena iluminación', 'Regular, sin encharcar', FALSE
FROM categorias c WHERE c.nombre = 'Aromáticas'
AND NOT EXISTS (SELECT 1 FROM plantas WHERE nombre = 'Albahaca');

COMMIT;
