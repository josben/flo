# language: es

Característica: Pagina principal
    Como un guardia
    Quiero ingresar al sistema
    Para registrar ingresos

    Esquema del escenario: Iniciar sesión
        Dado que ingreso al sistema con el url "http://127.0.0.1:8000/"
        Y voy a la opcion "Ingresar"
        Y entro con mi nombre de usuario <username>
        Y mi contraseña <password>
        Cuando oprima el boton "Ingresa"
        Entonces ingreso al sistema y leo el mensaje "Bienvenido"

        Ejemplos:
            | username | password |
            | benjamin | asdf     |


