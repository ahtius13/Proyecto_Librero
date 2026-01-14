# Proyecto_Librero
Proyecto para fin de curso A2 Python

(Null) = permite que no tenga valor

Ideas básicas:

-implementa un inventario de libros (solo dueño): titulo, autor, código libro, editorial, precio, cantidad, fecha salida(Null), fecha prestamo(Null)

-lista socios: Nombre, apellido, código socio, dirección, tlf

-sistema de prestamos: X libros con un tiempo de venta Y, los que queden se devuelven

-sistema de ventas: venta de libros a usuarios, si es socio x % descuento

-sistema de preventas: Solo socios, libros con fecha salida 1 mes en el futuro, X cantidad disponible

-devolucion del prestamo: Los libros que quedan por editorial cuya fecha de prestamo termina en 1 día

-devolución de compra: Devuelve al inventario un libro comprado por un Usuario

-busqueda de libros con las cantidades (solo usuario)

Definición de Proyecto:

Esta es una API de gestión para Librerias, en la cual el dueño del local puede controlar su inventario con una especial atención al sistema de prestamos de las editoriales.
Este sistema de prestamos permite visuavilizar los libros que otorga cada editorial, incluyendo una fecha de devolución que queda registrada para dar un aviso en el futuro. Este aviso incluye todos los libros disponibles para devolver, si no se han vendido, ordenados en cada una de sus respectivas editoriales.

Otra funcionalidad de la API es la gestión de los usuarios
