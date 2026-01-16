## Definición de Proyecto:

**Esta es una API de gestión para Librerias**, en la cual el dueño del local puede controlar su inventario con una especial atención al sistema de prestamos de las editoriales, además de poder administrar los diferentes usuarios relacionandolos con las compras que realizan.

### Administración de inventario y usuarios:

Estos sistemas trabajan de la misma forma; con un CRUD de los distintos libros y de los diferentes usuarios en dos JSON diferentes.
Los usuarios podrán realizar busquedas de libros, sin posibilidad de modificación del inventario.
Los socios además de la busqueda podran precomprar libros que estarán a la venta en un futuro cercano.
El dueño es el que tiene todos los permisos de administración y podrá realizar todo el CRUD tanto de los libros como de los usuarios.

### Sistema de prestamos:

El sistema de prestamos permite visuavilizar los libros que otorga cada editorial, incluyendo una fecha de devolución que queda registrada para dar un aviso en el futuro. Este aviso incluye todos los libros disponibles para devolver, si no se han vendido, ordenados en cada una de sus respectivas editoriales.
Una vez se dé el visto bueno, la cantidad de libros será modificada en el inventario.

### Sistema de ventas:

El sistema de ventas modifica en el inventario la cantidad de libros comprados por un usuario, quedando registrada dicha compra.
Tambien permite la devolución de dichas compras, modificando de nuevo el inventario.

