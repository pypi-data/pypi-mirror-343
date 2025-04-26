# ENV Errors
ERROR_GETTING_ENV_VARIABLE = "Error al obtener la variable de entorno: %s"

# Order Warnings
WARNING_DOCTOR_NOT_FOUND = "No se encontró un médico con esa matrícula: %s"
WARNING_DUPLICATED_ORDER = "Existe un pedido duplicado, ID: %s"

# Order Errors
ERROR_PRODUCTS_NOT_IN_AGREEMENT = "El o los productos ingresados no están contemplados en el convenio: %s"

# Event Manager Errors
ERROR_PUBLISH_FAILED = "[%s] - Hubo un error al publicar el mensaje: %s"
ERROR_CONSUME_FAILED = "Hubo un error al consumir el mensaje, sera eliminado de la cola: %s"
ERROR_TOPIC_NOT_FOUND = "El topico %s no fue enviado al inicializar el Publisher"
ERROR_QUEUE_NOT_FOUND = "La queue %s no fue enviada al inicializar el Publisher"
ERROR_WAITING_TIMEDOUT = "No todos los servicios respondieron a tiempo: %s"

# Event Manager Warnings

# Event Manager Success
SUCCESS_MESSAGE_PUBLISHED = "[%s] - El mensaje fue publicado en el topico: %s - con el evento: %s"
SUCCESS_CONSUMER_STARTED = "El consumer %s fue inicializado, y ya esta recibiendo mensajes"

# Event Manager Info
INFO_MESSAGE_RECEIVED = "[%s] - Mensaje recibido en el publisher"
INFO_WAITING_FOR_RESPONSES = "[%s] - Esperando la respuesta de los servicios: %s"
INFO_STARTING_CONSUMER = "[%s] - Inicializando consumer"
INFO_MESSAGE_CODE_MATCH = "[%s] - El consumer recibio un evento que puede consumir: %s"
INFO_RESTARTING_CONSUMER = "Reiniciando el consumer" 

# AWS Boto3 Secrets Errors
ERROR_GETTING_SECRET = "Error al obtener el secreto: %s"

# AWS Boto3 Secrets Info
INFO_GETTING_SECRET = "Se está intentando acceder a un secreto: %s"