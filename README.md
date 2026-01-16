# Proyecto Librería

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

## Funciones y Testing

## 1. Gestión del inventario de libros

**Descripción:** Cada libro debe tener la siguiente información:

 -Título

 -Autor

 -Código del libro (único)

 -Editorial

 -Precio

 -Cantidad disponible

 -Fecha de salida (puede ser Null)

 -Fecha de préstamo (puede ser Null)

### **Funcionalidades necesarias**

 -Añadir un libro nuevo al inventario

 -Modificar los datos de un libro existente

 -Eliminar un libro del inventario

 -Consultar libros (por título, autor o editorial)

 -Mostrar todos los libros disponibles

### **Pruebas (testing)**

 -Comprobar que no se pueden crear dos libros con el mismo código

 -Verificar que un libro puede tener fecha de salida o fecha de préstamo en Null

 -Comprobar que al vender o prestar un libro la cantidad se reduce correctamente

 -Verificar que no se puede vender o prestar un libro sin stock

## 2. Gestión de usuarios

**Descripción:** Cada usuario debe tener la siguiente información:

 -Nombre

 -Apellido

 -Tipo de usuario (socio, no socio, o admin)

 -Dirección

 -Teléfono

### **Funcionalidades necesarias**

 -Añadir un nuevo socio

 -Modificar los datos de un socio

 -Eliminar un socio

 -Consultar información de un socio

 -Mostrar la lista completa de socios

### **Pruebas (testing)**

 -Verificar que no se repiten códigos de socio

 -Comprobar que un socio se añade correctamente a la lista

 -Verificar que se puede modificar la información de un socio existente

 -Comprobar que al eliminar un socio deja de aparecer en el sistema

## 3. Sistema de préstamos

**Descripción:** El sistema tendrá que controlar los préstamos de las distribuidoras y controlar si un artículo hay que devolverlo a distribución si ha superado el tiempo límite.

### **Funcionalidades necesarias**

 -Registrar un préstamo de uno o varios libros.

 -Controlar la duración del préstamo.

 -Mostrar préstamos activos.

 -Detectar préstamos que están finalizados.

### **Pruebas (testing)**

 -Verificar que se incrementa el inventario al registrar préstamos.

 -Comprobar que la fecha de préstamo se guarda correctamente

 -Verificar que el sistema detecta los préstamos a devolver.

## 4. Devolución de préstamos

**Descripción:** Se deben gestionar las devoluciones de libros prestados.

### **Funcionalidades necesarias**

 -Devolver libros prestados

### **Pruebas (testing)**

 -Verificar que al devolver un libro a Editorial disminuye el stock

 -Comprobar que la fecha de préstamo se elimina o se marca como finalizada


## 5. Sistema de ventas

**Descripción:** El sistema permitirá la venta de libros a usuarios.

Características:

Se puede vender a socios y no socios

Los socios tienen un descuento X %

La venta reduce el stock del inventario

### **Funcionalidades necesarias**

 -Registrar una venta

 -Aplicar descuento si el comprador es socio

 -Calcular el precio final

 -Actualizar el inventario

### **Pruebas (testing)**

 -Comprobar que el descuento solo se aplica a socios

 -Verificar que el precio final es correcto

 -Comprobar que el stock se reduce tras la venta

 -Verificar que no se vende un libro sin stock

## 6. Sistema de preventas

**Descripción:** Las preventas tienen las siguientes condiciones:

Solo disponibles para socios

Libros con fecha de salida 1 mes en el futuro

Cantidad limitada disponible para preventa

### **Funcionalidades necesarias**

 -Registrar una preventa

 -Verificar que el usuario es socio

 -Comprobar la fecha de salida del libro

 -Controlar la cantidad disponible para preventa

### **Pruebas (testing)**

 -Verificar que un no socio no puede hacer preventas

 -Comprobar que solo se permiten libros con fecha futura

 -Verificar que la cantidad disponible se controla correctamente

## 7. Devolución de compras

**Descripción:** El sistema permitirá devolver un libro comprado.

Condiciones:

El libro vuelve al inventario

Se actualiza la cantidad disponible

### **Funcionalidades necesarias**

 -Registrar una devolución de compra

 -Actualizar el inventario

 -Verificar que el libro existe en el sistema

 ### **Pruebas (testing)**

 -Comprobar que el stock aumenta tras la devolución

 -Verificar que no se puede devolver un libro inexistente

 -Comprobar que la devolución se registra correctamente
