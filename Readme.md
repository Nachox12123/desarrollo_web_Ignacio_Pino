Hola, sobre mi tarea 1:

## Estructura
- /html → archivos HTML
- /css → estilos
- /js → scripts de validación y selects dinámicos
- /imagenes → fotos de ejemplo

# Detalles
 - En el formulario de adopción si hay un error sale arriba el campo que esta fallando
 - Los selects se encuentran todos en un archivo
 - En la pantalla Detalle nunca estuve seguro si el nombre era de la mascota o del dueño, asi que puse la mascota por descarte
 - Al igual que la anterior en el listado completo, la columna "Nombre Contacto" puse como si fuera el nombre del perro y el nombre de la persona como si fuera su instagram o alguna red social.

Hola sobre mi tarea 2:

## Estructura
- /tempaltes → HTML
- /static/css →  estilos
- /static/js → select y validaciones
- /database →  archivos SQL con modelos, datos iniciales,etc
- app.py →  archivo principal

# Detalles
- Tuve problemas con el Formulario, me entregaba que la comuna era None
- En Portada.html me sale este error: "';' expected.javascript", la verdad no estoy seguro que es pero investigue y dice que es confucion del vscode
- en uploads hay una carpeta imagenes, porque ahi tengo las imagenes de la tarea pasada


Hola sobre mi tarea 3:

## Estructura
- /templates → HTML (Detalle.html actualizado con comentarios y Estadisticas.html)
- /static/css → (nuevos Detalle.css y Estadisticas.css para comentarios y graficos)
- /static/js → validation.js actualizado con validaciones de comentarios
- /database → mismos archivos SQL, nueva tabla comentario se crea automaticamente
- app.py → nuevas APIs y modelo Comentario

# Detalles
- Implemente sistema de comentarios completo en pagina de detalle
- Nueva pagina de estadisticas con 3 graficos: linea (avisos por dia), torta (por tipo mascota), barras (por mes y tipo)
- Use Flot Charts para los graficos, se cargan con fetch API
- Todas las operaciones de comentarios son asincronas con JavaScript
- Validacion en tiempo real para comentarios 
- Las validaciones de comentarios estan en validation.js para mejor organizacion
- Los graficos muestran datos de los ultimos 30 dias/12 meses segun corresponda

Hola sobre mi tarea 4:

## Estructura
- /templates/evaluaciones.html → nueva interfaz que permite evaluar los avisos de adopcion
- /js/evaluacion.js → implementacion de funcion, validacion
- /static/css/evaluaciones.css → estilo de la nueva interfaz
- app.py → Nuevos modelos: Nota y relacion, funciones de calculo de promedios

## Detalles
- Decidí crear una interfaz nueva para no saturar las que ya estaban en la portada o el detalle
- la ruta de acceso a esta interfaz de evaluacion es desde la portada en el menu lateral
- Decicí crear una archivo js aparte por comodidad, ya que los otros estaban muy largos y confusos



