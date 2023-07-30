def convertir_segundos(segundos):
    horas = segundos // 3600
    segundos %= 3600
    minutos = segundos // 60
    segundos %= 60

    if horas > 0:
        return f"{int(horas)} hrs {int(minutos)} min {int(segundos)} sec"
    elif minutos > 0:
        return f"{int(minutos)} min {int(segundos)} sec"
    else:
        return f"{int(segundos)} sec"



if __name__ == "__main__":
    # Ejemplo de uso:
    segundos_totales = 40.1456465
    tiempo_formateado = convertir_segundos(segundos_totales)
    print(tiempo_formateado)

