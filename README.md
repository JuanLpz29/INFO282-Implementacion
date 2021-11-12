# tent

### Repositorio (branch gokussj4) que contiene el servidor Flask del proyecto Gestión Botillera. Desarrollado para la asignatura Taller Ingeniería de software INFO282, Universidad Austral de Chile.

Tiene también el Jenkinsfile y archivos de configuración para CI/CD

## Repositorios relacionados:

* Github documentación https://github.com/matiasbarram/info282

* Github implementación https://github.com/matiasbarram/info282-implementacion



```
export FLASK_APP=main.py
flask run

```

# Documentación

**Ver Productos**
----
  Retorna un arreglo de JSON con (los primeros) 30 productos
  
  *Pendiente*: modificar endpoind para retornar páginas 

* **URL**

  /productos/

* **Method:**

  `GET`
  
*  **URL Params**

    `None`

* **Success Response:**

  * **Code:** 200 <br />
  * **Content:**
    
`[{"formato":"botella","codigoBarra":"1234342", ..., "idProducto":90},..., {"formato":null,"codigoBarra":null,..., "idProducto":120}]`
 
* **Error Response:**

*pendiente*

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

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
  
  *pendiente*

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**
 
  ```shell
  curl --location --request GET 'http:(ip):(port)/productos/'
  ```
