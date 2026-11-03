
import simulador_bags as sim


def mi_fallo(msgs):
    """Duplica algunos mensajes publicados por el filtro."""

    inicio = min(m[2] for m in msgs)
    resultado = []
    contador = 0

    for topic, tipo, instante, mensaje in msgs:

        # Conservamos siempre el mensaje original
        resultado.append((topic, tipo, instante, mensaje))

        # Simulamos duplicaciones entre los segundos 10 y 15
        if topic == '/distancia_filtrada':
            tiempo_relativo = instante - inicio

            if 10.0 <= tiempo_relativo < 15.0:
                contador += 1

                # Duplicamos uno de cada cinco mensajes
                if contador % 5 == 0:
                    resultado.append(
                        (topic, tipo, instante, mensaje)
                    )

    # Conservamos el orden cronologico de grabacion
    resultado.sort(key=lambda m: m[2])

    return resultado


if __name__ == '__main__':
    sim.generar('mi_fallo', 'bags', post=mi_fallo)
