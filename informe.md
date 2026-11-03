# Práctica P2 (Tema 2) — Informe

**Nombre:** Alvaro Maza
**Entorno usado:**  local, versión de Python: 

> Regla de oro: **hipótesis escrita ANTES de medir**. Cada afirmación lleva su evidencia (comando + salida o gráfica).

---

## Declaración de autoría y uso de IA

Trabajo individual.
Uso de asistentes de IA (para qué, o «ninguno»): Creación de entorno y git / github

## Ejercicio 1 — Caso 5 (`bags/caso_5_casa`)

| Campo | Contenido |
|---|---|
| Síntoma (lo que se observa) |El bag tiene una duración de 39,010 segundos y contiene 120 mensajes 
repartidos entre /distancia, /distancia filtrada y /cmd vel demo, con 40 mensajes
 en cada topic.|
| Hipótesis (escrita antes de ejecutar nada) |Sospecho que se trata de un fallo dinámico
 provocado por una frecuencia de publicación demasiado baja en el sensor de distancia. 
El sistema debería funcionar a 10 Hz, pero el número de mensajes sugiere
 un ritmo cercano a 1 Hz en toda la cadena.
Como los tres topics tienen el mismo número de mensajes,
inicialmente no parece existir una pérdida adicional en el filtro o el controlador. 
Espero que el análisis confirme un hallazgo RITMO_BAJO en el origen, aunque todavía
 no puedo asegurar la causa exacta. |
| Comando(s) | `python3 analiza_bag.py bags/caso_5_casa --esperado /distancia=10 --png informe_caso5.png` |
| Evidencia (salida / gráfica) | La herramienta detectó RITMO_BAJO en /distancia, con 1,00 Hz
 medidos frente a 10 Hz esperados. Los tres topics presentan la misma frecuencia.
 Las latencias medianas son 0,002 s en /distancia y 0,007 s en /distancia_filtrada. |
| Eslabón donde se rompe |El problema comienza en el origen de la cadena, antes del procesamiento 
de /distancia. |
| Familia (estructural / dinámico / tiempo / origen) |Es un fallo de comportamiento dinámico,
 concretamente de frecuencia de publicación. |
| Causa raíz probable |El nodo productor de /distancia podría tener configurada una frecuencia de 
publicación de 1 Hz en lugar de 10 Hz, por ejemplo, debido a un temporizador incorrecto o una limitación
 del sensor. El bag permite localizar el síntoma, pero no confirmar cuál de esas causas lo produce. |
| Arreglo concreto y cómo comprobarlo | Revisar el temporizador o parámetro de frecuencia del nodo sensor.
 Si utiliza un temporizador configurado a 1,0 segundos, cambiarlo a 0,1 segundos para conseguir 10 Hz,
 siempre que el hardware lo permita. Después, comprobar las frecuencias con ros2 topic hz /distancia,
 ros2 topic hz /distancia filtrada y ros2 topic hz /cmd vel demo. Finalmente, grabar otro bag y analizarlo
 esperando que los tres topics funcionen aproximadamente a 10 Hz y desaparezca RITMO_BAJO. |

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

Bags entregados (en `bags/`, nombres que empiezan por `mi_`): <<RELLENAR>>
Cómo los generé (comandos): <<RELLENAR>>

Tabla comparativa sano / con fallo (ritmos, latencia, hallazgos): <<RELLENAR>>

**¿Qué no puede medir la herramienta con mensajes sin cabecera (`Float32`)? ¿Por qué?** <<RELLENAR>>

## Ejercicio 3 — Extensión de la herramienta

Comprobación(es) implementada(s): <<RELLENAR>>
Decisiones de diseño (¿ERROR o WARN? ¿margen?, ¿qué falsos positivos hay?): <<RELLENAR>>
Pruebas propias añadidas (nombre y qué comprueban): <<RELLENAR>>
Salida de `python3 -m unittest -v test_mis_comprobaciones`: <<RELLENAR>>
Resultado sobre `bags/mi_rango` (antes: TODO_OK; ahora: ...): <<RELLENAR>>

## Ejercicio 4 — Un quinto fallo

Ficha del fallo (SIN la solución; es lo que recibirá tu compañero):
- Nombre del bag: <<RELLENAR>>
- Síntoma observable: <<RELLENAR>>
- Qué debe averiguar quien lo resuelva: <<RELLENAR>>

**Solución (aparte, en sobre cerrado hasta que el compañero entregue):**
- Cómo se genera (parámetros o función `post`): <<RELLENAR>>
- Hallazgo(s) de `analiza_bag.py` que lo detectan, o por qué la herramienta no lo detecta: <<RELLENAR>>
- Eslabón, familia, causa y arreglo: <<RELLENAR>>

Resultado de la resolución del compañero (¿acertó? ¿qué le faltó? Si no hubo intercambio, «sin intercambio» y por qué): <<RELLENAR>>

## Ejercicio 5 — Lista de comprobación ampliada

Las 7 preguntas de la clase + 3 mías (cada una con su herramienta, qué detecta y un caso que la justifique):

| # | Pregunta | Herramienta | Detecta | Caso que la justifica |
|---|---|---|---|---|
| 8 | <<RELLENAR>> | | | |
| 9 | <<RELLENAR>> | | | |
| 10 | <<RELLENAR>> | | | |

## Ejercicio 6 — Autoformación guiada

Puntos de control de la *Guía de autoformación de la S8* (resumen de lo aprendido y dudas): <<RELLENAR>>

## Ejercicio 7 — Repositorio Git con integración continua

| Campo | Contenido |
|---|---|
| URL del repositorio (público, o privado con acceso para el profesor) | <<RELLENAR>> |
| Nº de commits y rama(s) de trabajo | <<RELLENAR>> |
| Pull Request (o merge) que integra una rama en `main` (URL) | <<RELLENAR>> |
| Ejecución de CI en **verde** (URL de la ejecución en Actions) | <<RELLENAR>> |
| Ejecución de CI en **rojo** provocada a propósito (URL) y commit que la arregla | <<RELLENAR>> |
| Qué rompí a propósito y cómo lo diagnostiqué en el log | <<RELLENAR>> |
| Bag(s) que añadí a `esperado.json` y por qué | <<RELLENAR>> |

Si **no** has podido usar GitHub, escribe aquí por qué y adjunta en `evidencias/` el `git_log.txt`, la salida de `simula_ci.py` y las capturas `ci_rojo` / `ci_verde` de la simulación local: la nota máxima del ejercicio baja (ver enunciado).

## Memoria conceptual (con tus palabras; máximo 1 página en total)

**M1.** Familias de fallo de arquitectura (estructural, dinámico, de tiempo, de origen aguas arriba): un ejemplo de cada una y la herramienta más barata que la detectaría. <<RELLENAR>>

**M2.** ¿Por qué una herramienta de análisis necesita pruebas unitarias, y qué significa que «un fallo no detectado es una especificación pendiente»? <<RELLENAR>>

**M3.** ¿Qué ocurre exactamente en un conflicto de fusión en Git, cómo se ve en el fichero y cómo se resuelve? ¿Por qué no se debe «aceptar el mío» sin leer? <<RELLENAR>>

**M4.** ¿Qué garantiza y qué NO garantiza una CI en verde? Usa como ejemplo el contrato de regresión con bags. <<RELLENAR>>

## Opcional — `ros2 bag play` y RViz2

<<RELLENAR o "No realizado">>

## Reflexión final (5 líneas)

¿Qué fue lo más difícil? ¿Qué cambiarías en la herramienta? ¿Qué le faltó al bag para estar seguro de la causa? <<RELLENAR>>
