# Práctica P2 (Tema 2) — Informe

**Nombre:** Alvaro Maza
**Entorno usado:**  local

> Regla de oro: **hipótesis escrita ANTES de medir**. Cada afirmación lleva su evidencia (comando + salida o gráfica).

---

## Declaración de autoría y uso de IA

Trabajo individual.
Uso de asistentes de IA (para qué, o «ninguno»): He utilizado ChatGPT como herramienta de apoyo para interpretar resultados de ROS 2, comprender errores y configurar Git y GitHub Actions. He ejecutado la práctica  en mi entorno Ubuntu 24.04 con ROS 2 Jazzy, revisando los resultados obtenidos. 

## Ejercicio 1 — Caso 5 (`bags/caso_5_casa`)

| Campo | Contenido |
|---|---|
| Síntoma (lo que se observa) |El bag tiene una duración de 39,010 segundos y contiene 120 mensajes repartidos entre /distancia, /distancia filtrada y /cmd vel demo, con 40 mensajesen cada topic.|
| Hipótesis (escrita antes de ejecutar nada) |Sospecho que se trata de un fallo dinámico provocado por una frecuencia de publicación demasiado baja en el sensor de distancia. El sistema debería funcionar a 10 Hz, pero el número de mensajes sugiere un ritmo cercano a 1 Hz en toda la cadena.Como los tres topics tienen el mismo número de mensajes,inicialmente no parece existir una pérdida adicional en el filtro o el controlador. Espero que el análisis confirme un hallazgo RITMO_BAJO en el origen, aunque todavía no puedo asegurar la causa exacta. |
| Comando(s) | `python3 analiza_bag.py bags/caso_5_casa --esperado /distancia=10 --png informe_caso5.png` |
| Evidencia (salida / gráfica) | La herramienta detectó RITMO_BAJO en /distancia, con 1,00 Hz medidos frente a 10 Hz esperados. Los tres topics presentan la misma frecuencia. Las latencias medianas son 0,002 s en /distancia y 0,007 s en /distancia_filtrada. |
| Eslabón donde se rompe |El problema comienza en el origen de la cadena, antes del procesamiento de /distancia. |
| Familia (estructural / dinámico / tiempo / origen) |Es un fallo de comportamiento dinámico, concretamente de frecuencia de publicación. |
| Causa raíz probable |El nodo productor de /distancia podría tener configurada una frecuencia de publicación de 1 Hz en lugar de 10 Hz, por ejemplo, debido a un temporizador incorrecto o una limitación del sensor. El bag permite localizar el síntoma, pero no confirmar cuál de esas causas lo produce. |
| Arreglo concreto y cómo comprobarlo | Revisar el temporizador o parámetro de frecuencia del nodo sensor. Si utiliza un temporizador configurado a 1,0 segundos, cambiarlo a 0,1 segundos para conseguir 10 Hz, siempre que el hardware lo permita. Después, comprobar las frecuencias con ros2 topic hz /distancia, ros2 topic hz /distancia filtrada y ros2 topic hz /cmd vel demo. Finalmente, grabar otro bag y analizarlo esperando que los tres topics funcionen aproximadamente a 10 Hz y desaparezca RITMO_BAJO. |

¿Qué os dice el grafo del sistema y qué os dice el bag? (pista: comparad con el caso D de la S7)
El grafo permite visualizar qué nodos y topics forman el sistema y cómo están conectados,
 pero no permite saber si la comunicación se realiza a la frecuencia adecuada.

En cambio, el bag permite estudiar el comportamiento temporal. En nuestro caso, los tres topics publican
 a 1 Hz, cuando esperamos 10 Hz. Al tener todos la misma frecuencia, podemos localizar el problema en
 el origen de la cadena, sin observar una pérdida adicional en el filtro.

Este comportamiento coincide con el caso D de la Sesión 7, en el que la frecuencia del sensor
 es demasiado baja y los demás nodos mantienen ese mismo ritmo. Se trata de un fallo dinámico que no se
 detecta únicamente observando las conexiones.

Pregunta de control: ¿Qué ocurriría con un sensor diseñado a 1 Hz?

Si el sensor estuviera diseñado para publicar a 1 Hz, la herramienta produciría una falsa alarma al
 asumir automáticamente que debe funcionar a 10 Hz.

La frecuencia esperada debería estar definida en los requisitos del sistema y documentada en un archivo
 de configuración que utilicen tanto el sistema como las pruebas. Así se evita diagnosticar como fallo
 un comportamiento que realmente es correcto.

## Ejercicio 2 — Mis propios bags

Bags entregados (en `bags/`, nombres que empiezan por `mi_`):
bags/mi_sano: sistema funcionando correctamente.

bags/mi_hueco: sistema con interrupción de mensajes entre los segundos 10 y 14.

bags/mi_hueco_float32: mismo fallo, pero utilizando mensajes Float32 sin cabecera.

Cómo los generé (comandos):
import simulador_bags as sim

sim.generar('mi_sano', 'bags')
sim.generar('mi_hueco', 'bags', hueco=(10, 14))
sim.generar('mi_hueco_float32', 'bags',
            hueco=(10, 14), tipo_mensaje='Float32')

Hipótesis previas al análisis:

1. Bag mi_sano: contiene 400 mensajes por topic en aproximadamente 40 segundos. Espero obtener una frecuencia cercana a 10 Hz y el resultado TODO_OK, sin errores de ritmo, latencia ni huecos.

2. Bag mi_hueco: contiene 360 mensajes por topic, 40 menos que el sistema sano. Sospecho que existe una interrupción de aproximadamente cuatro segundos. Espero que la herramienta detecte HUECOS y permita identificar dónde comienza la interrupción.

3. Bag mi_hueco_float32: contiene también 360 mensajes por topic, pero /distancia y /distancia_filtrada utilizan mensajes Float32 sin cabecera. Espero detectar la interrupción mediante los tiempos de grabación, pero no poder calcular la latencia basada en header.stamp.

Tabla comparativa sano / con fallo (ritmos, latencia, hallazgos):
| Característica | mi_sano | mi_hueco | mi_hueco_float32 |
|---|---|---|---|
| Tipo de mensaje de distancia | Range | Range | Float32 |
| Mensajes por topic | 400 | 360 | 360 |
| Frecuencia media | 10,00 Hz | 9,00 Hz | 9,00 Hz |
| Intervalo máximo sin mensajes | 0,10 s | 4,10 s | 4,10 s |
| Latencia mediana /distancia | 0,002 s | 0,002 s | No disponible |
| Latencia mediana /distancia_filtrada | 0,007 s | 0,007 s | No disponible |
| Hallazgos | TODO_OK | HUECOS y HUECO_ORIGEN | HUECOS y HUECO_ORIGEN |

**Interpretación de los resultados:**

El bag sano presenta 400 mensajes por topic y una frecuencia de 10 Hz, por lo que la herramienta devuelve TODO_OK.

En los dos bags con fallo aparecen 360 mensajes por topic y una interrupción de 4,1 segundos entre los segundos 10,0 y 14,1. La herramienta detecta HUECOS en los tres topics y señala /distancia como origen de la interrupción.

El problema se clasifica como un fallo de origen aguas arriba que afecta al comportamiento temporal del sistema. El filtro y el controlador también dejan de recibir datos durante ese intervalo.

La frecuencia media disminuye a 9 Hz porque faltan 40 mensajes, aunque fuera del hueco los mensajes mantienen su periodicidad normal.

Las latencias en el bag Range son pequeñas y similares a las del sistema sano, por lo que no se observa un problema de retraso prolongado.
**¿Qué no puede medir la herramienta con mensajes sin cabecera (`Float32`)? ¿Por qué?**
Los mensajes `std_msgs/msg/Float32` no contienen el campo `header.stamp`, por lo que la herramienta no puede conocer el momento exacto en que se generó la medición. Por tanto, no puede calcular la latencia entre la generación del dato y su recepción, ni detectar un posible hallazgo `LATENCIA_ALTA` utilizando esa información.

Sin embargo, sí puede detectar interrupciones de comunicación, porque utiliza los instantes de grabación del bag para calcular los intervalos entre mensajes.

Esto se comprueba en nuestros experimentos: tanto `mi_hueco` como `mi_hueco_float32` presentan los hallazgos `HUECOS` y `HUECO_ORIGEN`, con una interrupción de 4,1 segundos. En este fallo concreto no desaparece ningún hallazgo; lo que se pierde es la medición de latencia, que podría revelar otros problemas de frescura de los datos.

Para medir la latencia en un sistema real, utilizaría un tipo de mensaje que incluyese una cabecera temporal, como `sensor_msgs/msg/Range`, o definiría un mensaje personalizado con el valor y una marca temporal de origen. Además, sería necesario garantizar que los relojes utilizados estuvieran sincronizados.

## Ejercicio 3 — Extensión de la herramienta

Comprobación(es) implementada(s): He implementado la función comprobar_rangos(muestras, topic, margen=0.0) en mis_comprobaciones.py. Esta función comprueba si las mediciones de distancia están dentro de los límites min_range y max_range del sensor. Cuando encuentra valores incorrectos, devuelve un único hallazgo RANGO_FUERA, indicando el número de muestras afectadas y el intervalo temporal en el que aparecen. Si todas las muestras son válidas, devuelve una lista vacía.

Decisiones de diseño (¿ERROR o WARN? ¿margen?, ¿qué falsos positivos hay?): He elegido la severidad ERROR porque una medición fuera de los límites declarados del sensor puede provocar decisiones incorrectas en el controlador. El margen por defecto es de 0,0 m, aunque puede ajustarse para admitir tolerancias justificadas. Podrían producirse falsos positivos por ruido, errores de calibración o valores especiales admitidos por determinados sensores. Por ello, en un sistema real revisaría las especificaciones del dispositivo antes de establecer las tolerancias.

Pruebas propias añadidas (nombre y qué comprueban):

test_valores_exactamente_en_los_limites: comprueba que las mediciones iguales a min_range y max_range se consideran válidas.

test_varios_errores_y_intervalo_temporal: comprueba que dos mediciones incorrectas generan un único hallazgo, con severidad ERROR, código RANGO_FUERA, topic correcto y el intervalo temporal correspondiente.

Salida de python3 -m unittest -v test_mis_comprobaciones: Se ejecutaron 11 pruebas en 0,135 segundos. Nueve finalizaron correctamente, ninguna falló y dos fueron omitidas porque corresponden a la ampliación opcional comprobar_frames(). Resultado final: OK (skipped=2).

Resultado sobre bags/mi_rango (antes: TODO_OK; ahora: ...): La herramienta original analiza_bag.py devuelve TODO_OK porque no comprueba los límites físicos del sensor. Sin embargo, nuestra nueva comprobación detecta 20 mediciones fuera de rango en /distancia, entre los segundos 10,10 y 12,00, con el hallazgo RANGO_FUERA y código de salida 1. Al ejecutar la misma comprobación sobre bags/mi_sano, se analizan 400 muestras sin encontrar errores y se obtiene código de salida 0.

## Ejercicio 4 — Un quinto fallo

**Hipótesis previa al análisis:** He introducido un fallo dinámico que provoca duplicaciones de mensajes en `/distancia_filtrada`. Los metadatos muestran 410 mensajes en ese topic, frente a los 400 de `/distancia` y `/cmd_vel_demo`.

Sospecho que `analiza_bag.py` podría no detectar el fallo, porque su análisis se centra en frecuencias bajas, huecos, latencias y problemas de reloj, pero no comprueba explícitamente los mensajes duplicados.

Espero que el sistema mantenga aproximadamente su ritmo normal y que la herramienta pueda devolver `TODO_OK`, a pesar de los mensajes adicionales. Esta hipótesis deberá contrastarse con el análisis completo.

**Ficha del fallo (SIN la solución; es lo que recibirá tu compañero):**

- **Nombre del bag:** `reto/reto_1`
- **Síntoma observable:** El sistema registra actividad en los tres topics y la herramienta de diagnóstico devuelve `TODO_OK`. Sin embargo, las cantidades de mensajes de las distintas etapas no coinciden exactamente.
- **Qué debe averiguar quien lo resuelva:** Identificar la anomalía, localizar el eslabón afectado, clasificar el fallo y explicar por qué la herramienta no lo detecta. Proponer una solución comprobable.

Solución:

Cómo se genera (parámetros o función `post`):** He creado `mi_fallo.py`, que utiliza la función `mi_fallo(msgs)` y el parámetro `post` de `simulador_bags.generar()`. El fallo consiste en duplicar una de cada cinco publicaciones de `/distancia_filtrada` entre los segundos 10 y 15. Los mensajes duplicados conservan el contenido y el instante de grabación originales. Como resultado, `/distancia_filtrada` contiene 410 mensajes, mientras que `/distancia` y `/cmd_vel_demo` tienen 400 cada uno.

Hallazgo(s) de `analiza_bag.py` que lo detectan, o por qué la herramienta no lo detecta: Al ejecutar `python3 analiza_bag.py bags/mi_fallo --esperado /distancia=10`, la herramienta devuelve `TODO_OK`. Los topics `/distancia` y `/cmd_vel_demo` mantienen 10,00 Hz, mientras que `/distancia_filtrada` alcanza 10,25 Hz. La herramienta no comprueba explícitamente la existencia de duplicados, por lo que el pequeño aumento de frecuencia no genera ningún hallazgo de error. Se trata de un punto ciego del analizador.

Eslabón, familia, causa y arreglo: El fallo aparece en la salida del filtro, concretamente en `/distancia_filtrada`. Pertenece a la familia de fallos dinámicos de procesamiento de mensajes. La causa es que algunas publicaciones se realizan dos veces. Para corregirlo, revisaría el callback del filtro y garantizaría que cada mensaje recibido genera una única publicación. Después repetiría la grabación y comprobaría que los tres topics contienen 400 mensajes, sin publicaciones duplicadas.

Resultado de la resolución del compañero: No se ha intercambiado

## Ejercicio 5 — Lista de comprobación ampliada

Las 7 preguntas de la clase + 3 mías (cada una con su herramienta, qué detecta y un caso que la justifique):

| # | Pregunta | Herramienta | Detecta | Caso que la justifica |
|---|---|---|---|---|
| 8 | ¿Los valores publicados por el sensor están dentro de sus límites físicos? | `mis_comprobaciones.py`, función `comprobar_rangos()` | Mediciones inferiores a `min_range` o superiores a `max_range`, que podrían ser utilizadas incorrectamente por el controlador. | En `mi_rango`, `analiza_bag.py` devuelve `TODO_OK`, pero nuestra comprobación identifica 20 mediciones de 9,9 m fuera del máximo permitido de 4 m. |
| 9 | ¿Se están publicando mensajes duplicados o más mensajes de los esperados en alguna etapa? | `analiza_bag.py --info` para comparar cantidades y un análisis de timestamps y contenidos del bag para confirmar duplicados. | Posibles publicaciones repetidas en un nodo que podrían provocar procesamiento adicional o respuestas duplicadas. | En `mi_fallo`, `/distancia_filtrada` contiene 410 mensajes frente a los 400 de los otros topics. El analizador devuelve `TODO_OK` pese a las duplicaciones introducidas. |
| 10 | ¿Los cambios del software mantienen los resultados esperados en los casos de referencia? | `regresion_bags.py` y GitHub Actions. | Regresiones y discrepancias entre el comportamiento obtenido y el contrato definido en `esperado.json`. | En el experimento de CI, cambié deliberadamente la salida esperada de `mi_rango` de 0 a 1. La regresión falló con 5/6 casos correctos y la CI se puso roja. Al corregirlo, volvió a verde. |

## Ejercicio 6 — Autoformación guiada

Puntos de control de la Guía de autoformación de la S8

**Etapa 0 — Preparación del entorno:** Comprobé el funcionamiento de `ros2 bag --help` en Ubuntu 24.04 con ROS 2 Jazzy, identificando los comandos de grabación, reproducción, inspección y conversión de bags.

**Etapa 1 — rosbag2 básico:** Utilicé turtlesim para grabar los topics `/turtle1/pose` y `/turtle1/cmd_vel`. El bag generado contiene 9541 mensajes y tiene una duración de 152,39 segundos. Posteriormente, reproduje la grabación con `ros2 bag play` y comprobé mediante `ros2 topic echo` que los mensajes de posición se recibían correctamente.

**Etapa 2 — rosbag2 avanzado:** Trabajé con el formato MCAP y realicé una conversión utilizando compresión Zstandard. El tamaño pasó de 677,9 KiB a 245,5 KiB, una reducción aproximada del 64 %, conservando los 9541 mensajes. También configuré un perfil QoS personalizado para `/turtle1/pose` y comprobé las políticas `BEST_EFFORT` y `VOLATILE` mediante `ros2 topic info --verbose`.

**Etapa 3 — RViz2 y tf2:** Creé una transformación estática entre `base_link` y `sensor_link`, con un desplazamiento vertical de 0,2 metros. Configuré RViz2 con `base_link` como Fixed Frame y generé el árbol de transformaciones mediante `view_frames`, comprobando la relación entre ambos marcos.

**Etapa 4 — Depuración de arquitectura:** Apliqué el método de formular una hipótesis, inspeccionar los metadatos, analizar las mediciones y localizar el eslabón afectado. En el caso 5 identifiqué un fallo dinámico de frecuencia: el sensor publicaba a 1 Hz frente a los 10 Hz esperados. También comparé bags sanos y defectuosos para estudiar huecos, latencias y limitaciones de los mensajes sin cabecera.

**Resumen de lo aprendido:** He comprendido que un bag permite reproducir y analizar fallos sin mantener el sistema original en funcionamiento. También he aprendido a diferenciar los problemas estructurales, dinámicos y temporales, a interpretar políticas QoS y a utilizar tf2 para representar relaciones entre marcos de referencia.

**Dudas y aspectos pendientes:** Queda por profundizar en la partición de bags grandes y en los criterios para elegir las políticas QoS más adecuadas en sistemas reales. También sería interesante comprobar cómo afectan las transformaciones tf2 incorrectas a la visualización de datos de sensores en RViz2.

## Ejercicio 7 — Repositorio Git con integración continua

| Campo | Contenido |
|---|---|
| URL del repositorio (público, o privado con acceso para el profesor) | https://github.com/AlvaroMazaEsco/P2_Arquitectura_Software |
| Nº de commits y rama(s) de trabajo | 8 commits en main, incluyendo la fusión del PR #1, y 2 commits adicionales en la rama experimental. Se han utilizado main, ej3-rango y ci-rojo-verde. |
| Pull Request (o merge) que integra una rama en `main` (URL) | PR #1: https://github.com/AlvaroMazaEsco/P2_Arquitectura_Software/pull/1. Integra la comprobación de rangos y sus pruebas unitarias desde ej3-rango hacia main. |
| Ejecución de CI en **verde** (URL de la ejecución en Actions) | https://github.com/AlvaroMazaEsco/P2_Arquitectura_Software/actions/runs/41640919716 |
| Ejecución de CI en **rojo** provocada a propósito (URL) y commit que la arregla |CI roja: https://github.com/AlvaroMazaEsco/P2_Arquitectura_Software/actions/runs/41640418330. Commit que provocó el fallo: b487084. Commit que lo corrigió: 4f45957. |
| Qué rompí a propósito y cómo lo diagnostiqué en el log |En la rama ci-rojo-verde modifiqué deliberadamente esperado.json, cambiando el código de salida esperado de mi_rango de 0 a 1. GitHub Actions detectó la discrepancia durante la regresión con bags: [FALLO] mi_rango, resultado esperado 1 y obtenido 0. La ejecución terminó con 5 de 6 casos correctos y código de salida 1. Restauré el valor original mediante un nuevo commit y la CI volvió a verde. |
| Bag(s) que añadí a `esperado.json` y por qué |Añadí mi_rango para ampliar el contrato de regresión y comprobar que analiza_bag.py sigue devolviendo salida 0 y ningún error. Este resultado también demuestra su limitación: no detecta mediciones fuera del rango físico. La nueva función comprobar_rangos() verifica ese problema mediante pruebas independientes. |

Si **no** has podido usar GitHub, escribe aquí por qué y adjunta en `evidencias/` el `git_log.txt`, la salida de `simula_ci.py` y las capturas `ci_rojo` / `ci_verde` de la simulación local: la nota máxima del ejercicio baja (ver enunciado).

## Memoria conceptual (con tus palabras; máximo 1 página en total)

### M1. Familias de fallo de arquitectura

Los fallos **estructurales** afectan a la comunicación entre componentes, por ejemplo, cuando dos nodos utilizan nombres de topics diferentes. Se pueden detectar con `ros2 topic list -t` y `ros2 topic info -v`.

Los **dinámicos** aparecen cuando el sistema está conectado, pero funciona incorrectamente. En el caso 5 detecté una frecuencia de 1 Hz frente a los 10 Hz esperados, utilizando `analiza_bag.py`.

Los fallos **de tiempo** afectan a la sincronización de relojes o marcas temporales, como `RELOJ_DESFASADO` del caso 2, detectable mediante el análisis del bag.

Los fallos **de origen aguas arriba** comienzan en el productor y afectan a toda la cadena. En `mi_hueco`, `analiza_bag.py` identificó `HUECO_ORIGEN` en `/distancia`.

### M2. Pruebas unitarias y especificaciones pendientes

Las pruebas unitarias permiten verificar que cada comprobación funciona correctamente y evitar regresiones después de modificar el código.

La expresión «un fallo no detectado es una especificación pendiente» significa que la herramienta todavía no contempla una condición de error que debería comprobar.

Lo demostramos con `mi_rango`: el analizador original devolvía `TODO_OK` pese a existir mediciones inválidas. Implementé `comprobar_rangos()` y añadí pruebas para cubrir ese comportamiento.

### M3. Conflictos de fusión en Git

Un conflicto ocurre cuando Git no puede combinar automáticamente cambios realizados sobre las mismas líneas o regiones de un archivo.

Git señala las versiones mediante `<<<<<<< HEAD`, `=======` y `>>>>>>> rama`. Para resolverlo, se revisan ambas modificaciones, se conserva el contenido correcto, se eliminan los marcadores y se ejecutan las pruebas antes de confirmar la resolución.

No debemos aceptar automáticamente nuestra versión porque podríamos eliminar cambios válidos de otra rama o introducir errores.

### M4. Qué garantiza una CI en verde

Una CI en verde confirma que las comprobaciones automatizadas configuradas han terminado correctamente para el código evaluado.

En nuestra P2 ejecutamos pruebas unitarias y regresiones con bags de referencia. Esto permite detectar cambios que incumplan el contrato definido en `esperado.json`.

Sin embargo, una CI verde no garantiza que el programa esté libre de errores ni que funcione correctamente en todas las situaciones reales.

Por ejemplo, nuestro bag `mi_fallo` contiene publicaciones duplicadas y `analiza_bag.py` devuelve `TODO_OK`. La CI no detectará ese defecto mientras no exista una prueba específica que lo compruebe.

## Opcional — `ros2 bag play` y RViz2

**Realizado.** Durante la autoformación de la Sesión 8 utilicé `ros2 bag play` para reproducir una grabación de turtlesim que contenía 9541 mensajes. Reproduje el bag a doble velocidad y comprobé mediante `ros2 topic echo /turtle1/pose` que los mensajes se recibían correctamente.

También utilicé RViz2 para visualizar los marcos de referencia `base_link` y `sensor_link`, conectados mediante una transformación estática de 0,2 metros. Configuré `base_link` como Fixed Frame y generé el árbol de transformaciones con `view_frames`.

Estas pruebas me permitieron comprobar la reproducción de datos grabados y comprender la importancia de los marcos de referencia para visualizar información en ROS 2.

## Reflexión final (5 líneas)

Lo más difícil fue comprender los distintos tipos de fallos y localizar el eslabón responsable a partir de los bags.

También supuso un reto implementar las comprobaciones de rangos y configurar correctamente GitHub Actions.

Mejoraría la herramienta incorporando detección de mensajes duplicados y comprobaciones automáticas de los límites físicos de los sensores.

Al bag le faltaba información sobre el código, los parámetros y los logs de los nodos para poder confirmar las causas exactas de los fallos.

Esta práctica me ha permitido comprender la importancia de las pruebas, la depuración sistemática y la integración continua en sistemas robóticos.
