# tent

### Repositorio (branch backend) que contiene el servidor Flask del proyecto Gestión Botillería. Desarrollado para la asignatura Taller Ingeniería de software INFO282, Universidad Austral de Chile.

Tiene también el Jenkinsfile y archivos de configuración para CI/CD

## Repositorios relacionados:

* Github documentación https://github.com/matiasbarram/info282

* Github implementación https://github.com/matiasbarram/info282-implementacion

## Actualmente desplegada en pythonanywhere

https://hiawvp.pythonanywhere.com/


# Instalación

Para replicar el ambiente de desarrollo localmente se necesita una instalación de mysql / mariadb y se recomienda usar linux + conda

```bash
$ mysql --version
mysql  Ver 8.0.28-0ubuntu0.20.04.3 for Linux on x86_64 ((Ubuntu))
```
clonar repo e ir al directorio raiz

```bash
$ conda create --name taller pip
$ conda activate taller
$ pip install -r requirements.py

$ export FLASK_APP=main.py
$ export FLASK_ENV=development
$ flask run

```

# Documentación

**Ver Productos**
----
  Retorna un arreglo de JSON con (los primeros) 10 productos
  
* **URL**

  /productos/

* **Method:**

  `GET`
  
*  **URL Params**

    **Optional:**

    ```page=[integer]```

    ```perpage=[integer]```

    ```filter=[string]```

    ```sortby=[string]```

    ```order=[string]```

* **Success Response:**

  * **Code:** 200 <br />
  * **Content:**
    
`[{"formato":"botella","codigoBarra":"1234342", ..., "idProducto":90},..., {"formato":null,"codigoBarra":null,..., "idProducto":120}]`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Login required" }`

* **Sample Call:**

  ```shell
  curl --location --request GET 'http:(ip):(port)/productos/'
  ```
    
    
**Ver un Producto**
----
  Retorna la información en JSON de un solo producto

* **URL**

  /productos/:id

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `id=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
  * **Content:** 
    
`{"formato":null,"codigoBarra":null,"categoria":null,"descripcion":null,"precioVenta":null,"valorItem":24680,"stock":1,"precioCompra":null,"nombre":"AUSTRAL LAGER 4PKX6 VNR330","cantidadRiesgo":null,"precioUnitario":24680,"idProducto":102}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "no se encontro producto" }`

  OR

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Login required" }`


* **Sample Call:**
 
  ```shell
  curl --location --request GET 'http:(ip):(port)/productos/'
  ```
