<img src="https://www.ucu.edu.uy/plantillas/images/logo_ucu.svg" alt="UCU" width="200"/>

# Universidad Católica del Uruguay

## Facultad de Ingeniería y Tecnologías

### Análisis y diseño de aplicaciones II

<br/>

# Demo de disponibilidad

Esta demo tiene una sencilla [aplicación web](./main.py) que expone una API REST; está implementada en Python usando [fastapi](https://fastapi.tiangolo.com) y la ejecutamos con [uvicorn](https://www.uvicorn.org).

La API tiene un endpoint para devolver un saludo o un error dependiendo de cierta probabilidad que se puede configurar; el valor predeterminado es 1 indicando que está siempre disponible.

El otro endpoint de la API permite cambiar la probabilidad por un valor entre 0 y 1.

La demo incluye también los scripts de [K6](https://grafana.com/docs/k6/latest/set-up/install-k6/) para probarla.

Los comandos para hacer la demo están [aquí](./commands.azcli). Con el complemento [Azure CLI Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.azurecli) es posible ejecutar los comandos directamente desde Visual Studio Code.

# Requisitos

* Python

* [K6](https://grafana.com/docs/k6/latest/set-up/install-k6/)

# Actividades

A partir de los resultados de K6 y utilizando diferentes valores de probabilidad de disponibilidad determinar el tiempo operativo y el tiempo total; a partir de allí calcular la disponibilidad.
