 Proyecto_Librero/
 │
 ├── src/ 
 │   ├── libros.py 
 │   ├── usuarios.py 
 │   ├── prestamos.py 
 │   ├── ventas.py 
 │   ├── preventas.py 
 │   ├── main.py 
 │
 ├── tests/ 
 │   ├── test_libros.py 
 │   ├── test_usuarios.py 
 │   ├── test_prestamos.py 
 │   ├── test_devoluciones.py 
 │   ├── test_ventas.py 
 │   ├── test_preventas.py 
 │ 
 └── pytest.ini

# Proyecto Librería

## Definición de Proyecto:

**Esta es una API de gestión para Librerias**, en la cual el dueño del local puede controlar su inventario con una especial atención al sistema de prestamos de las editoriales, además de poder administrar los diferentes usuarios relacionandolos con las compras que realizan.

### Administración de inventario y usuarios:

Estos sistemas trabajan de la misma forma; con un CRUD de los distintos libros y de los diferentes usuarios en dos JSON diferentes.

Los usuarios podrán realizar busquedas de libros, sin posibilidad de modificación del inventario.

Los socios además de la búsqueda podran precomprar libros que estarán a la venta en un futuro cercano.

El dueño es el que tiene todos los permisos de administración y podrá realizar todas las funciones.

### Sistema de préstamos:

El sistema de prestamos permite visuavilizar los libros que otorga cada editorial, incluyendo una fecha de devolución que queda registrada para dar un aviso en el futuro. Este aviso incluye todos los libros disponibles para devolver, si no se han vendido, ordenados en cada una de sus respectivas editoriales.

Una vez se dé el visto bueno, la cantidad de libros será modificada en el inventario.

### Sistema de ventas:

El sistema de ventas modifica en el inventario la cantidad de libros comprados por un usuario, quedando registrada dicha compra.

También permite la devolución de dichas compras, modificando de nuevo el inventario.

# Funciones y Testing

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

 -Registrar un libro nuevo al inventario

 -Modificar los datos de un libro existente

 -Eliminar un libro del inventario

 -Consultar libros (por título, autor o editorial) --> Función de socio

 -Mostrar todos los libros disponibles --> Función de socio

### **Pruebas (testing)**

 -Comprobar que no se pueden crear dos libros con el mismo código. Compara el código del libro con los del inventario para verificar
 si coincide con alguno.

 -Verificar que el libro registrado no tenga una fecha de salida anterior a la actual.

 -Comprobar que al vender o prestar un libro el campo cantidad se reduce correctamente.

 -Verificar que no se puede vender o prestar un libro sin stock.

## 2. Gestión de usuarios

**Descripción:** Cada usuario debe tener la siguiente información:

 -Nombre

 -Apellido

 -Número de socio

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

 -Verificar que no se repiten socios. Se compara su número de socio con el de la base de datos.

 -Comprobar que un socio se añade correctamente al archivo JSON.

 -Verificar que se puede modificar la información de un socio existente.

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

 -Comprar un libro (Aplicar descuento si el comprador es socio) --> Función de socio


### **Pruebas (testing)**

 -Comprobar que el descuento solo se aplica a socios

 -Comprobar que el stock se reduce tras la venta

 -Verificar que no se vende un libro sin stock

## 6. Sistema de preventas

**Descripción:** Las preventas tienen las siguientes condiciones:

Solo disponibles para socios

Libros con fecha de salida 1 mes en el futuro

Cantidad limitada disponible para preventa

### **Funcionalidades necesarias**

 -Reservar una preventa --> Función de socio
 

### **Pruebas (testing)**

 -Verificar que un no socio no puede hacer preventas.

 -Comprobar que solo se permiten libros con fecha futura.

 -Verificar que no deja realizar más reservas cuando la cantidad disponible llegue a 0.

## 7. Devolución de compras

**Descripción:** El sistema permitirá devolver un libro comprado.

Condiciones:

El libro vuelve al inventario

Se actualiza la cantidad disponible

### **Funcionalidades necesarias**

 -Registrar una devolución de compra

 ### **Pruebas (testing)**

 -Comprobar que el stock aumenta tras la devolución

 -Verificar que no se puede devolver un libro inexistente

