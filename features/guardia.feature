Característica: Pagina principal
    Como un guardia
    Quiero ingresar al sistema
    Para registrar ingresos

    Esquema del escenario: Iniciar sesión
        Dado que he introducido mi nombre de usuario <username>
        Y mi contraseña <password>
        Cuando oprima el boton <button>
        Entonces debo ingresar al sistema

        Ejemplos:
            | username | password | button          |
            | benji    | asdf     | iniciar_sesion  |
            | gabe     | qwer     | iniciar_sesion  |

    Esquema del escenario: Registrar visita
        Dado que ingresa una persona con documento <type_doc>
        Y con numero de docuento <num_doc>
        Y con el siguiente nombre <name>
        Y proviene de la ciudad <city>
        Y con el siguinte motivo <reason>
        Cuando registre a la persona
        Y el <num_doc> sea valido
        Entonces regitro a la persona <name> con documento <num_doc>

        Ejemplos:
            | type_doc   | num_doc | name | city | reason |
            | pasaporte  | 123456  | juan | br   | asdf   |
            | CI         | 654321  | carl | lpz  | qwer   |

