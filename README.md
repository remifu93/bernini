# Bernini APIRest

```code
git clone https://github.com/remifu93/bernini
cd bernini
docker-compose up --build
```

Para ingresar al proyecto ir a la url http://127.0.0.1:8000/

# Usuarios
Usuario admin: admin@admin.com
Usuario normal: user@user.com

En ambos usuarios la **password** es **123456**

# API KEY
La api key es **api_key**
Se debe enviar el header **x-api-key** con el valor antes dicho para las endoints que lo requieran.


# Estructura
En este caso, tenemos los recursos users, products y orders, por lo que usaremos las siguientes URL: /users/ , /products/ y /orders/

POST > **/api/users/token/**
Hacer login, devuelve un access token
```sh
JSON
{
    "email": "admin@admin.com",
    "password": "123456"
}
```

GET > **/api/products?search=<termino busqueda>&page=<numero>**
Listar productos con parametros opcionales de paginacion y busqueda
```
search - Parametro de busqueda por nombre
page - Numero de pagina del listado de resultados
page_size - Definir resultados por pagina.
```

GET > **/api/orders**
Trae las ordenes del usuario logueado, si es admin trae todas las ordenes
- Necesita header **Authorization** con value **Bearer + access token**
- Necesita header **x-api-key** con value **api_key**

GET > **/api/orders/<order_id>**
Detalle de una orden, un admin puede ver todas, un usuario normal solo sus ordenes
- Necesita header **Authorization** con value **Bearer + access token**
- Necesita header **x-api-key** con value **api_key**

POST > **/api/orders**
Crea una orden nueva a nombre del usuario logueado
- Necesita header **Authorization** con value **Bearer + access token**
- Necesita header **x-api-key** con value **api_key**
```sh
JSON
{
	"shipment_method": "E",
	"products": [{"id": <id producto>, "quantity": <cantidad>}]
}
```
shipment_methods >  **E** Express, **S** Standar y **P** Pickup sucursal (gratis)

## Documentacion
- Se utilizo la generacion de documentacion con swagger la cual se accede desde el indice de la aplicacion (es necesario haber iniciado sesion en el panel de admin de django previamente para poder verla).

## Cliente de solicitudes HTTP
Para testear los endpoints en este caso utilice
https://insomnia.rest/

El proyecto incluye un fichero llamado **insomnia_requests** por si quereis testear la api de una forma mas sencilla

## Django Tests
Para correr los tests de django dentro de docker yo suelo utilizar:

```sh
docker run -it <docker_image_web> bash
python3 manage.py test
```