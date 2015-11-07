
Característica: Pagina de registro
    Como un guardia
    Quiero registrar las salidas y retornos de los vehiculos
    Para almacenar los datos

    Esquema del escenario: Registrar vehiculo de la empresa
        Dado que el vehiculo con numero interno <num_interno> esta de <estado>
        Y sale/retorna del parqueo <parqueo>
        Y con el conductor de con item <num_item>
        Y tiene el kilometraje <km>
        Y con las escaleras <escaleras>
        Y en fecha <fecha>
        Y en horas <hora>
        Cuando registre al vehiculo <num_interno> con su estado de <estado>
        Y los datos del vehiculo <num_interno> sean validos
        Entonces guardo el registro del vehiculo <num_interno>
        Pero si hay notificaciones se las envia al administrador

        Ejemplos: Datos de registro
            | parqueo  | num_interno | num_item | km      | escaleras | fecha      | hora  | estado    |
            | muyurina | 123         | 543      | 10100   | 23 43 12  | 18/02/2014 | 08:12 | salida    |
            | km 0     | 321         | 432      | 20100   | 45 14 54  | 18/02/2014 | 08:34 | salida    |
            | muyurina | I-02        | 564      | 15210   | 78 46 11  | 18/02/2014 | 08:43 | salida    |
            | muyurina | I-04        | 101      | 10010   | 99 98 90  | 18/02/2014 | 08:50 | salida    |
            | muyurina | I-01        | 110      | 12110   | 90 78 11  | 18/02/2014 | 08:58 | salida    |
            | muyurina | 321         | 432      | 20159   | 45 14     | 18/02/2014 | 10:05 | entrada   |
            | muyurina | 321         | 432      | 20159   | 45 14 54  | 18/02/2014 | 10:50 | salida    |
            | taller   | 321         | 432      | 20249   | 45 14 54  | 18/02/2014 | 15:50 | entrada   |
            | taller   | 321         | 432      | 20249   | 45 14 54  | 18/02/2014 | 18:10 | salida    |
            | muyurina | 123         | 505      | 10189   | 23 43 12  | 18/02/2014 | 18:52 | entrada   |
            | muyurina | I-01        | 110      | 12184   | 90 78 11  | 18/02/2014 | 19:38 | entrada   |
            | sucre    | I-02        | 564      | 15256   | 78 46 11  | 18/02/2014 | 20:00 | entrada   |
            | muyurina | 321         | 432      | 20293   | 45 14 54  | 18/02/2014 | 20:35 | entrada   |
            | muyurina | I-01        | 110      | 12184   | 90 78 11  | 19/02/2014 | 08:18 | salida    |
            | muyurina | I-04        | 1305     | 10000   | 99 98     | 19/02/2014 | 13:05 | entrada   |
            | muyurina | I-01        | 120      | 12110   | 90 78 11  | 20/02/2014 | 08:58 | salida    |
            | muyurina | I-01        | 110      | 12987   | 90 78 11  | 25/02/2014 | 08:14 | entrada   |

