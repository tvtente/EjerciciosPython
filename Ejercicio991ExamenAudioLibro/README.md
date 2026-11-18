# Audiolibro: usabilidad y accesibilidad

Abre index.html con doble clic. La página usa audiolibro-datos.js para generar el HTML descargable del audiolibro, que puedes abrir en un navegador compatible con síntesis de voz. No necesita servidor ni depende de archivos en carpetas internas.

El archivo audiolibro.csv contiene una copia de los capítulos y sus párrafos, separados por punto y coma. La página utiliza audiolibro-datos.js; modificar el CSV no actualiza automáticamente esos datos.

Los registros se guardan en el navegador y dispositivo donde se rellena el formulario. En «Preparar y gestionar» se pueden descargar en CSV o data.json e importar un JSON exportado anteriormente. El JSON no se actualiza automáticamente. Otros navegadores o dispositivos tienen sus propios registros, y borrar los datos del navegador puede eliminarlos. El acceso mediante correo no verifica la identidad.


La página incluye un selector entre español y catalán. El idioma elegido también determina el texto del audiolibro generado y las voces compatibles mostradas. Se muestran hasta tres voces instaladas; si no hay voces para ese idioma, hay que instalarlas en el dispositivo.

La raíz también contiene audiolibro-ca.csv y Audiollibre_Usabilitat_Accessibilitat.html con la traducción catalana. Al seleccionar «Català», SpotyWifi genera y descarga la versión catalana; al seleccionar «Español», genera la versión española. Los archivos CSV son copias para consulta: la página utiliza los datos de audiolibro-datos.js y audiolibro-ca.js.

El idioma y el tema elegidos se recuerdan en este navegador. En «Gestionar registros» hay una tabla consultable y una búsqueda por nombre, apellidos o correo. La tabla muestra únicamente los datos locales o importados en ese navegador. La navegación principal y las ventanas se pueden usar con teclado: Tab y Mayús+Tab para recorrer controles, Enter o espacio para activarlos y Escape para cerrar las ventanas.
