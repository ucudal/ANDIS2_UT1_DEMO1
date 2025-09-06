<img src="https://www.ucu.edu.uy/plantillas/images/logo_ucu.svg" alt="UCU" width="200"/>

# Universidad Católica del Uruguay

## Facultad de Ingeniería y Tecnologías

### Análisis y diseño de aplicaciones II

<br/>

# Demo de disponibilidad

Esta demo tiene una sencilla [aplicación web](./main.py) que expone una API
REST; está implementada en Python usando [fastapi](https://fastapi.tiangolo.com)
y la ejecutamos con [uvicorn](https://www.uvicorn.org).

La API tiene un endpoint para devolver un saludo o un error dependiendo de
cierta probabilidad que se puede configurar; el valor predeterminado es 1
indicando que está siempre disponible.

El otro endpoint de la API permite cambiar la probabilidad por un valor entre 0
y 1.

La demo incluye también los scripts de
[K6](https://grafana.com/docs/k6/latest/set-up/install-k6/) para probarla.

Para ejecutar esta demo usa los comandos que están [aquí](./commands.azcli). Con
el complemento [Azure CLI
Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.azurecli)
es posible ejecutar los comandos directamente desde Visual Studio Code.

Una vez que ejecutes la aplicación, puedes ver la documentación de los endpoints
con [Swagger](http://localhost:5000/docs).

# Requisitos

* Python

* [K6](https://grafana.com/docs/k6/latest/set-up/install-k6/)

# Actividades

A partir de los resultados de K6 y utilizando diferentes valores de probabilidad
de disponibilidad determinar el tiempo operativo y el tiempo total; a partir de
allí calcular la disponibilidad.



# Demo de Disponibilidad con FastAPI

Esta demo implementa dos servicios FastAPI (A y B) para ilustrar tácticas de disponibilidad, junto con InfluxDB y Grafana en contenedores Docker.

## Estructura

- **service_a/**: API principal, consume Service B y aplica tácticas de disponibilidad.
- **service_b/**: Backend, simula fallas y permite configuración dinámica.
- **k6/**: Pruebas de carga.
- **commands.azcli**: Comandos para levantar, probar y detener los servicios.
- **docker-compose.yml**: InfluxDB y Grafana.

## Tácticas implementadas

- Monitoreo, ping/echo, heartbeat, shadowing, rollback, reintentos, degradación elegante, repuesto redundante (simulado), rejuvenecimiento, manejo de excepciones, validaciones, etc.

## Ejecución

Sigue los pasos en `commands.azcli` para levantar los servicios y ejecutar las pruebas.

