CREATE TABLE IF NOT EXISTS `Clientes`(
	`cod_cliente` INT PRIMARY KEY AUTO_INCREMENT,
	`dni` INT NOT NULL,
	`nombre` VARCHAR(255) NOT NULL,
	`apellido1` VARCHAR(255) NOT NULL,
	`apellido2` VARCHAR(255) NOT NULL,
	`direccion` VARCHAR(255) NULL,
	`email` VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS `Prestamos`(
	`id_prestamo` INT PRIMARY KEY AUTO_INCREMENT,
	`fecha_pretamo` TIME NOT NULL,
	`fecha_tope` TIME NOT NULL,
	`fecha_entrega` TIME NULL,
	`cod_cliente` INT NOT NULL,
	`n_copia` INT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Copias`(
	`n_copia` INT PRIMARY KEY AUTO_INCREMENT,
	`deteriorada` BOOLEAN NULL,
	`formato` VARCHAR(255) NOT NULL,
	`id_pelicula` INT NOT NULL,
	`precio_alquiler` INT NULL
);
CREATE TABLE IF NOT EXISTS `Peliculas`(
	`id_pelicula` INT PRIMARY KEY AUTO_INCREMENT,
	`titulo` VARCHAR(255) NOT NULL,
	`año` INT NULL,
	`critica` VARCHAR(255) NULL,
	`caratula` VARCHAR(255) NULL
);
ALTER TABLE `Prestamos`
	ADD CONSTRAINT `FK_Prestamos_Clientes`
 		FOREIGN KEY (`cod_cliente`) REFERENCES `Clientes` (`cod_cliente`) ON DELETE Restrict ON UPDATE Restrict
;
ALTER TABLE `Prestamos`
	ADD CONSTRAINT `FK_Prestamos_Copias`
 		FOREIGN KEY (`n_copia`) REFERENCES `Copias` (`n_copia`) ON DELETE Restrict ON UPDATE Restrict
;
ALTER TABLE `Copias`
	ADD CONSTRAINT `FK_Copias_Peliculas`
 		FOREIGN KEY (`id_pelicula`) REFERENCES `Peliculas` (`id_pelicula`) ON DELETE Restrict ON UPDATE Restrict
;
