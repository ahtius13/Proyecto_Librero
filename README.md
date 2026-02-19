```
proyecto_libreria/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── libros.py
│   │   ├── usuarios.py
│   │   ├── prestamos.py
│   │   ├── ventas.py
│   │   └── preventas.py
│   ├── libros.py
│   │── usuarios.py
│   │── prestamos.py
│   │── ventas.py
│   │── preventas.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── json_functions.py
├── data/
│   ├── libros.json
│   └── usuarios.json
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_libros.py
│   ├── test_usuarios.py
│   ├── test_prestamos.py
│   ├── test_ventas.py
│   └── test_preventas.py
├── requirements.txt
└── README.md

```
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

 -Registrar un libro nuevo al inventario (POST: /libros/)

 -Modificar los datos de un libro existente (PUT: /libros/)

 -Eliminar un libro del inventario (DELETE: /libros/)

 -Consultar libros (por título, autor o editorial) --> Función de socio (GET: /libros/ISBN)

 -Mostrar todos los libros disponibles --> Función de socio (GET: /libros/all)

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

 -Añadir un nuevo socio (POST: /usuarios/)

 -Modificar los datos de un socio (PUT: /usuarios/numero_socio)

 -Eliminar un socio (DELETE: /usuarios/numero_socio)

 -Consultar información de un socio (GET: /usuarios/numero_socio)

 -Mostrar la lista completa de socios

### **Pruebas (testing)**

 -Verificar que no se repiten socios. Se compara su número de socio con el de la base de datos.

 -Comprobar que un socio se añade correctamente al archivo JSON.

 -Verificar que se puede modificar la información de un socio existente.

 -Comprobar que al eliminar un socio deja de aparecer en el sistema

## 3. Sistema de préstamos

**Descripción:** El sistema tendrá que controlar los préstamos de las distribuidoras y controlar si un artículo hay que devolverlo a distribución si ha superado el tiempo límite.

### **Funcionalidades necesarias**

 -Registrar un préstamo de uno o varios libros. (POST: prestamos/)

 -Controlar la duración del préstamo. 

 -Mostrar préstamos activos. (GET: prestamos/)

 -Detectar préstamos que están finalizados. (GET: prestamos/finalizados)

### **Pruebas (testing)**

 -Verificar que se incrementa el inventario al registrar préstamos.

 -Comprobar que la fecha de préstamo se guarda correctamente

 -Verificar que el sistema detecta los préstamos a devolver.

## 4. Devolución de préstamos

**Descripción:** Se deben gestionar las devoluciones de libros prestados por una editorial. Todos los que no se vendan en el plazo marcado deben devolverse a la Editorial.

### **Funcionalidades necesarias**
-Devolver libros prestados (POST: /devolucion/prestamos/ISBN)

### **Pruebas (testing)**
-Verificar que al devolver un libro a Editorial disminuye el stock de la cantidad que se devuelve.
-Comprobar que la fecha de préstamo se elimina o se marca como finalizada.
-Comprobar que no se pueden devolver más libros de los que hay en stock.


## 5. Sistema de ventas

**Descripción:** El sistema permitirá la venta de libros a usuarios.

Características:

Se puede vender a socios y no socios

Los socios tienen un descuento X %

La venta reduce el stock del inventario

### **Funcionalidades necesarias**

 -Comprar un libro (Aplicar descuento si el comprador es socio) --> Función de socio (POST: /ventas/ISBN)


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

 -Reservar una preventa --> Función de socio (POST: preventa/ISBN)
 

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

 -Registrar una devolución de compra (POST: /devolucion/compra/ISBN)

 ### **Pruebas (testing)**

 -Comprobar que el stock aumenta tras la devolución

 -Verificar que no se puede devolver un libro inexistente

## Entidades

### Libro

- ISBN
- Titulo
- Autor
- Editorial
- Precio
- Stock 
- Fecha Salida
- Fecha Prestamo

### Usuarios

- Id_Usuario
- Nombre
- Apellido
- Dirección
- Tlf
- Tipo de Usuario

#### Acciones

En negrita las acciones que solo puede hacer el Usuario Administrador.
Futura y opcional acción del administrador Busqueda de Ventas y de Devoluciones.

- Buscar Libro
- Comprar Libro
- Devolver Libro
- **Añadir Libro**
- **Eliminar Libro**
- **Modificar Libro**
- **Añadir Usuario**
- **Eliminar Usuario**
- **Modificar Usuario**
- **Buscar Usuario**

### Venta

- Id_Venta
- Fecha_Venta
- Id_Usuario
- ISBN
- Cantidad
- Precio_total
- Preventa

### Devolución

- Id_Devolución
- Fecha_Devolución
- Id_Venta
- Cantidad