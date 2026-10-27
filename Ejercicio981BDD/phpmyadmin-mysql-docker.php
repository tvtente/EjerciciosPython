<?php
/* Configuración local de phpMyAdmin para MySQL Docker.
 * Copiar en /etc/phpmyadmin/conf.d/99-mysql-docker.php.
 * La contraseña se introduce en el formulario de acceso; no se guarda aquí.
 * No usa el controluser de la instalación local, cuyas credenciales fallan.
 * Las funciones de almacenamiento avanzado se podrán configurar por separado.
 */
$cfg['Servers'][1] = [
    'verbose' => 'MySQL Docker - gestion_de_pedidos (3307)',
    'host' => '127.0.0.1',
    'port' => '3307',
    'auth_type' => 'cookie',
    'AllowNoPassword' => false,
];
$cfg['ServerDefault'] = 1;
