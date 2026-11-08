-- Reemplaza solo las imágenes provisionales; conserva fotos cargadas manualmente.
USE raiz_celeste;
START TRANSACTION;
UPDATE plantas SET imagen = '/static/img/plantas/monstera.jpg' WHERE nombre = 'Monstera' AND (imagen = '/static/img/planta.svg' OR imagen = '');
UPDATE plantas SET imagen = '/static/img/plantas/potus.jpg' WHERE nombre = 'Potus' AND (imagen = '/static/img/planta.svg' OR imagen = '');
UPDATE plantas SET imagen = '/static/img/plantas/lavanda.jpg' WHERE nombre = 'Lavanda' AND (imagen = '/static/img/planta.svg' OR imagen = '');
UPDATE plantas SET imagen = '/static/img/plantas/echeveria.png' WHERE nombre = 'Echeveria' AND (imagen = '/static/img/planta.svg' OR imagen = '');
UPDATE plantas SET imagen = '/static/img/plantas/romero.jpg' WHERE nombre = 'Romero' AND (imagen = '/static/img/planta.svg' OR imagen = '');
UPDATE plantas SET imagen = '/static/img/plantas/albahaca.jpg' WHERE nombre = 'Albahaca' AND (imagen = '/static/img/planta.svg' OR imagen = '');
COMMIT;
