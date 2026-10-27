USE gestion_de_pedidos;

START TRANSACTION;

UPDATE clientes SET nif='10037129K', nombre='Lucía', apellidos='García López', direccion='C/ del Olivo, 14, 2.º B, 28012 Madrid', telefono='610073129', email='lucia.garcia@example.com' WHERE id=1;

UPDATE clientes SET nif='10074258M', nombre='José Luis', apellidos='Martínez Ruiz', direccion='Av. de los Naranjos, 32, bajo, 46022 Valencia', telefono='+34 610 146 258', email='jose-luis.martinez@example.com' WHERE id=2;

UPDATE clientes SET nif='10111387N', nombre='María del Mar', apellidos='Sánchez Pérez', direccion='Plaza del Mercado, 5, 1.º A, 41003 Sevilla', telefono='610-219-387', email='maria.delmar@example.com' WHERE id=3;

UPDATE clientes SET nif='10148516L', nombre='Óscar', apellidos='Fernández Díaz', direccion='Calle Mayor, 108, 3.º C, 50001 Zaragoza', telefono='0034 610292516', email='oscar_fernandez@example.com' WHERE id=4;

UPDATE clientes SET nif='10185645A', nombre='Ana Belén', apellidos='López Romero', direccion='P.º de la Alameda, 7, 29016 Málaga', telefono='(610) 365 645', email='ana.belen+5@example.com' WHERE id=5;

UPDATE clientes SET nif='X1007404G', nombre='Iñaki', apellidos='Etxeberria Martín', direccion='C/ de la Estación, 21, 48008 Bilbao', telefono='610438774', email='inaki.etxeberria@example.com' WHERE id=6;

UPDATE clientes SET nif='10259903V', nombre='Núria', apellidos='Puig Soler', direccion='Rambla de les Flors, 18, 08002 Barcelona', telefono='+34 610 511 903', email='nuria.puig@example.com' WHERE id=7;

UPDATE clientes SET nif='10297032R', nombre='Álvaro', apellidos='Muñoz Jiménez', direccion='Avda. de Castilla, 45, 47008 Valladolid', telefono='610-585-032', email='alvaro.munoz@example.com' WHERE id=8;

UPDATE clientes SET nif='10334161P', nombre='Carmen', apellidos='De la Fuente Gil', direccion='Calle Río Ebro, 9, 4.º D, 26004 Logroño', telefono='0034 610658161', email='carmen.delafuente@example.com' WHERE id=9;

UPDATE clientes SET nif='10371290S', nombre='Miguel Ángel', apellidos='Torres Navarro', direccion='Plaza de España, 3, 03001 Alicante', telefono='(610) 731 290', email='miguel.angel+10@example.com' WHERE id=10;

UPDATE clientes SET nif='10408419E', nombre='Rocío', apellidos='Ortega Molina', direccion='C/ del Almendro, 27, 14006 Córdoba', telefono='610804419', email='rocio.ortega@example.com' WHERE id=11;

UPDATE clientes SET nif='10445548Y', nombre='Héctor', apellidos='Castro Iglesias', direccion='Paseo del Parque, 6, 33203 Gijón', telefono='+34 610 877 548', email='hector.castro@example.com' WHERE id=12;

UPDATE clientes SET nif='X1016042V', nombre='Ainhoa', apellidos='Vázquez Alonso', direccion='Calle San Pedro, 11, 31001 Pamplona', telefono='610-950-677', email='ainhoa.vazquez@example.com' WHERE id=13;

UPDATE clientes SET nif='10519806C', nombre='Pablo', apellidos='Del Río Santos', direccion='Av. de Galicia, 64, 15004 A Coruña', telefono='0034 611023806', email='pablo.delrio@example.com' WHERE id=14;

UPDATE clientes SET nif='10556935G', nombre='Inés', apellidos='Herrera Marín', direccion='C/ de la Huerta, 8, 30002 Murcia', telefono='(611) 096 935', email='ines.herrera+15@example.com' WHERE id=15;

UPDATE clientes SET nif='10594064B', nombre='Adrián', apellidos='Moreno Serrano', direccion='Calle del Mar, 16, 07012 Palma', telefono='611170064', email='adrian.moreno@example.com' WHERE id=16;

UPDATE clientes SET nif='10631193H', nombre='Mónica', apellidos='Pascual Ferrer', direccion='Avda. del Puerto, 92, 12003 Castellón', telefono='+34 611 243 193', email='monica.pascual@example.com' WHERE id=17;

UPDATE clientes SET nif='10668322W', nombre='Raúl', apellidos='Núñez Vega', direccion='C/ de la Acequia, 4, 18010 Granada', telefono='611-316-322', email='raul.nunez@example.com' WHERE id=18;

UPDATE clientes SET nif='X1023446S', nombre='Elena', apellidos='Ramos Cabrera', direccion='Plaza del Carmen, 12, 39003 Santander', telefono='0034 611389451', email='elena.ramos@example.com' WHERE id=19;

UPDATE clientes SET nif='10742580Q', nombre='Víctor', apellidos='Peña Domínguez', direccion='Calle de los Pinos, 30, 20009 Donostia', telefono='(611) 462 580', email='victor.pena+20@example.com' WHERE id=20;

UPDATE categorias SET nombre='Fruta fresca', descripcion='Frutas de temporada y variedades de proximidad' WHERE id=1;

UPDATE categorias SET nombre='Verduras y hortalizas', descripcion='Hortalizas para ensalada, guisos y cocina diaria' WHERE id=2;

UPDATE categorias SET nombre='Cítricos', descripcion='Naranjas, mandarinas, limones y pomelos' WHERE id=3;

UPDATE categorias SET nombre='Frutos secos', descripcion='Frutos secos naturales y tostados' WHERE id=4;

UPDATE categorias SET nombre='Hierbas aromáticas', descripcion='Hierbas frescas para cocinar' WHERE id=5;

UPDATE productos SET nombre='Manzana Golden', descripcion='Pieza de calibre mediano; origen: Lleida', precio='1.20', categoriaId='1' WHERE id=1;

UPDATE productos SET nombre='Pera conferencia', descripcion='Pieza madura para consumo; origen: La Rioja', precio='0.95', categoriaId='1' WHERE id=2;

UPDATE productos SET nombre='Plátano de Canarias', descripcion='Venta por pieza; categoría extra', precio='0.45', categoriaId='1' WHERE id=3;

UPDATE productos SET nombre='Fresa de Huelva', descripcion='Bandeja de 500 g', precio='3.25', categoriaId='1' WHERE id=4;

UPDATE productos SET nombre='Uva blanca sin pepitas', descripcion='Bandeja de 500 g', precio='2.80', categoriaId='1' WHERE id=5;

UPDATE productos SET nombre='Melocotón amarillo', descripcion='Pieza de temporada', precio='1.10', categoriaId='1' WHERE id=6;

UPDATE productos SET nombre='Ciruela roja', descripcion='Bandeja de 500 g', precio='2.35', categoriaId='1' WHERE id=7;

UPDATE productos SET nombre='Kiwi verde', descripcion='Pieza de calibre 27', precio='0.75', categoriaId='1' WHERE id=8;

UPDATE productos SET nombre='Melón piel de sapo', descripcion='Pieza de aproximadamente 2 kg', precio='4.90', categoriaId='1' WHERE id=9;

UPDATE productos SET nombre='Sandía sin semillas', descripcion='Media pieza envasada', precio='3.95', categoriaId='1' WHERE id=10;

UPDATE productos SET nombre='Tomate de ensalada', descripcion='Bandeja de 1 kg', precio='2.40', categoriaId='2' WHERE id=11;

UPDATE productos SET nombre='Lechuga romana', descripcion='Unidad fresca', precio='1.15', categoriaId='2' WHERE id=12;

UPDATE productos SET nombre='Zanahoria lavada', descripcion='Bolsa de 1 kg', precio='1.30', categoriaId='2' WHERE id=13;

UPDATE productos SET nombre='Calabacín verde', descripcion='Bandeja de 1 kg', precio='1.95', categoriaId='2' WHERE id=14;

UPDATE productos SET nombre='Pepino holandés', descripcion='Unidad de aproximadamente 400 g', precio='0.85', categoriaId='2' WHERE id=15;

UPDATE productos SET nombre='Pimiento rojo', descripcion='Bandeja de 500 g', precio='2.25', categoriaId='2' WHERE id=16;

UPDATE productos SET nombre='Naranja de zumo', descripcion='Malla de 2 kg', precio='3.60', categoriaId='3' WHERE id=17;

UPDATE productos SET nombre='Mandarina clementina', descripcion='Malla de 1 kg', precio='2.10', categoriaId='3' WHERE id=18;

UPDATE productos SET nombre='Limón de Murcia', descripcion='Malla de 500 g', precio='1.25', categoriaId='3' WHERE id=19;

UPDATE productos SET nombre='Pomelo rosa', descripcion='Unidad de aproximadamente 350 g', precio='1.05', categoriaId='3' WHERE id=20;

UPDATE productos SET nombre='Almendra cruda', descripcion='Bolsa de 250 g; sin sal', precio='3.75', categoriaId='4' WHERE id=21;

UPDATE productos SET nombre='Nuez con cáscara', descripcion='Bolsa de 500 g', precio='4.20', categoriaId='4' WHERE id=22;

UPDATE productos SET nombre='Avellana tostada', descripcion='Bolsa de 200 g; sin sal', precio='2.95', categoriaId='4' WHERE id=23;

UPDATE productos SET nombre='Perejil fresco', descripcion='Manojo de aproximadamente 50 g', precio='0.80', categoriaId='5' WHERE id=24;

UPDATE productos SET nombre='Albahaca fresca', descripcion='Bandeja de 30 g', precio='1.45', categoriaId='5' WHERE id=25;

UPDATE proveedores SET nombre='Huertas del Turia, S. L.', nif='B1000001', telefono='+34 960 123 401', email='pedidos@proveedor1.example.com', direccion='Av. de los Naranjos, 32, bajo, 46022 Valencia' WHERE id=1;

UPDATE proveedores SET nombre='Cítricos Azahar, S. Coop.', nif='B1000002', telefono='955-240-802', email='comercial@proveedor2.example.com', direccion='Calle Mayor, 108, 3.º C, 50001 Zaragoza' WHERE id=2;

UPDATE proveedores SET nombre='Frutas del Ebro, S. L.', nif='B1000003', telefono='976 350 603', email='ventas@proveedor3.example.com', direccion='C/ de la Estación, 21, 48008 Bilbao' WHERE id=3;

UPDATE proveedores SET nombre='Hortalizas Vega Sur, S. L.', nif='B1000004', telefono='0034 968 415 204', email='administracion@proveedor4.example.com', direccion='Avda. de Castilla, 45, 47008 Valladolid' WHERE id=4;

UPDATE proveedores SET nombre='Platanera Insular, S. Coop.', nif='B1000005', telefono='922450705', email='distribucion@proveedor5.example.com', direccion='Plaza de España, 3, 03001 Alicante' WHERE id=5;

UPDATE proveedores SET nombre='Frutos Secos La Encina, S. L.', nif='B1000006', telefono='+34 925 618 306', email='pedidos@proveedor6.example.com', direccion='Paseo del Parque, 6, 33203 Gijón' WHERE id=6;

UPDATE proveedores SET nombre='Aromáticas del Mediterráneo, S. L.', nif='B1000007', telefono='950.720.907', email='info@proveedor7.example.com', direccion='Av. de Galicia, 64, 15004 A Coruña' WHERE id=7;

UPDATE proveedores SET nombre='Fresas Marisma, S. Coop.', nif='B1000008', telefono='959 832 108', email='ventas@proveedor8.example.com', direccion='Calle del Mar, 16, 07012 Palma' WHERE id=8;

UPDATE proveedores SET nombre='Distribuciones Huerta Norte, S. L.', nif='B1000009', telefono='944-915-609', email='logistica@proveedor9.example.com', direccion='C/ de la Acequia, 4, 18010 Granada' WHERE id=9;

UPDATE proveedores SET nombre='Agrofruta Sierra Verde, S. L.', nif='B1000010', telefono='958026410', email='contacto@proveedor10.example.com', direccion='Calle de los Pinos, 30, 20009 Donostia' WHERE id=10;

UPDATE tiendas SET nombre='Frutería La Huerta — Centro', nif='B1000001', telefono='+34 910 120 301', email='centro@lahuerta.example.com', direccion='C/ del Olivo, 2, local 1, 28012 Madrid' WHERE id=1;

UPDATE tiendas SET nombre='Frutería La Huerta — Mercado', nif='B1000002', telefono='910 120 302', email='mercado@lahuerta.example.com', direccion='Plaza del Mercado, 8, puesto 14, 28005 Madrid' WHERE id=2;

UPDATE tiendas SET nombre='Frutería La Huerta — Norte', nif='B1000003', telefono='910-120-303', email='norte@lahuerta.example.com', direccion='Av. de los Pinos, 36, bajo, 28029 Madrid' WHERE id=3;

UPDATE usuarios SET nombre='Ana Belén', apellidos='López Romero', usuario='ana_belen1' WHERE id=1;

UPDATE usuarios SET nombre='Iñaki', apellidos='Etxeberria Martín', usuario='inaki_etxeberria2' WHERE id=2;

UPDATE usuarios SET nombre='Núria', apellidos='Puig Soler', usuario='nuria_puig3' WHERE id=3;

UPDATE usuarios SET nombre='Álvaro', apellidos='Muñoz Jiménez', usuario='alvaro_munoz4' WHERE id=4;

UPDATE usuarios SET nombre='Carmen', apellidos='De la Fuente Gil', usuario='carmen_delafuente5' WHERE id=5;

UPDATE usuarios SET nombre='Miguel Ángel', apellidos='Torres Navarro', usuario='miguel_angel6' WHERE id=6;

UPDATE usuarios SET nombre='Rocío', apellidos='Ortega Molina', usuario='rocio_ortega7' WHERE id=7;

UPDATE usuarios SET nombre='Héctor', apellidos='Castro Iglesias', usuario='hector_castro8' WHERE id=8;

UPDATE proveedores_productos pp JOIN productos p ON p.id=pp.productoId SET pp.precio_compra=ROUND(p.precio*(0.55+MOD(pp.proveedorId,4)*0.05),2);

COMMIT;
