Característica: Programacion de mantenimiento
    Como sistema
    Quiero programar automaticamente el mantenimiento faltando 200 km
    Para prevenir peores daños

    Esquema del escenario: Cargar automaticamente las fechas de mantenimiento
        Dado el vehiculo <num_interno>
        Y el kilometraje del ultimo mantenimiento fue <km_last_maintenance>
        Y su siguiente mantenimiento es <next_km_maintenance>
        Y el kilometraje actual es <current_km>
        Cuando los datos son analizados
        Entonces se asigna el vehiculo para mantenimiento

        Ejemplos:
            | num_interno | km_last_maintenance | current_km | next_km_maintenance |
            | 19          | 19900               | 20700      | 20900               |
            | I-01        | 1100                | 2500       | 3000                |
            | I-05        | 14790               | 16890      | 17000               |

