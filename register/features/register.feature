# language: es

Característica: Pagina de registro
    Como un guardia
    Quiero registrar las salidas y retornos de los vehiculos
    Para almacenar los datos

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

    Esquema del escenario: Registrar vehiculo de la empresa
        Dado que vamos a la pagina de registro "http://127.0.0.1:8000/register/register_form/"
        Y registra el vehiculo con numero interno <num_interno> esta de <estado>
        Y sale/retorna del parqueo <parqueo>
        Y con el conductor con item <num_item>
        Y tiene el kilometraje <km>
        Y con las escaleras <escaleras>
        Y en fecha <fecha>
        Y en horas <hora>
        Cuando registre al vehiculo <num_interno> con su estado de <estado>
        Y lea el mensaje "Registro guardado exitosamente"
        Entonces guardo el registro del vehiculo <num_interno> correctamente

        Ejemplos: Datos de registro
            | parqueo  | num_interno | num_item  | km       | escaleras | fecha      | hora  | estado    |
            | muyurina | 123         | 1779      | 142601   | 23 43 12  | 22/09/2015 | 08:12 | salida    |
            | muyurina | I-04        | 1754      | 177395   | 99 98 90  | 22/09/2015 | 08:50 | salida    |
            | muyurina | 123         | 1779      | 142645   | 23 43 12  | 22/09/2015 | 18:52 | entrada   |
            | muyurina | I-02        | 1546      | 142080   | 90 78 11  | 22/09/2015 | 08:58 | salida    |
            | muyurina | I-02        | 1546      | 142120   | 90 78 11  | 22/09/2015 | 19:38 | entrada   |
            | muyurina | I-02        | 1546      | 142120   | 90 78 11  | 23/09/2015 | 08:18 | salida    |
            | muyurina | I-04        | 1754      | 177487   | 99 98     | 23/09/2015 | 13:05 | entrada   |
            | muyurina | I-02        | 1546      | 142153   | 90 78 11  | 23/09/2015 | 18:58 | entrada   |


