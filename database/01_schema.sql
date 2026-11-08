-- Raíz Celeste · Esquema para MySQL 8.0.16 o superior.
-- No elimina bases ni tablas existentes. Ejecutar antes de 02_seed.sql.
CREATE DATABASE IF NOT EXISTS raiz_celeste
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE raiz_celeste;

CREATE TABLE IF NOT EXISTS categorias (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(80) NOT NULL,
  descripcion VARCHAR(255) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  CONSTRAINT uq_categorias_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS plantas (
  id INT NOT NULL AUTO_INCREMENT,
  categoria_id INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  nombre_cientifico VARCHAR(150) NOT NULL DEFAULT '',
  descripcion TEXT NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  imagen VARCHAR(255) NOT NULL DEFAULT '/static/img/planta.svg',
  luz VARCHAR(100) NOT NULL DEFAULT '',
  riego VARCHAR(150) NOT NULL DEFAULT '',
  destacada BOOLEAN NOT NULL DEFAULT FALSE,
  creada_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX idx_plantas_categoria (categoria_id),
  INDEX idx_plantas_nombre (nombre),
  CONSTRAINT fk_plantas_categoria FOREIGN KEY (categoria_id)
    REFERENCES categorias(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT ck_plantas_precio CHECK (precio > 0),
  CONSTRAINT ck_plantas_stock CHECK (stock >= 0)
) ENGINE=InnoDB;
