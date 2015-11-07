Característica: Pagina principal
    Como un guardia
    Quiero ingresar al sistema
    Para registrar ingresos

    Esquema del escenario: Iniciar sesión
        Dado que ingreso al sistema con el url "http://127.0.0.1:8000/"
        Y que he introducido mi nombre de usuario <username>
        Y mi contraseña <password>
        Cuando oprima el boton <button>
        Entonces debo ingresar al sistema

        Ejemplos:
            | username | password |
            | benjamin | asdf     |
            | gabe     | qwer     |


