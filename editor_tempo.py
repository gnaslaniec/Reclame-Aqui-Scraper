""" VARIÁVEIS PARA TRATAMENTOS DO HORÁRIO! """
# Arredonda pra 00
grupo_1 = {'00', '01', '02', '03', '04', '05', '06',
           '07', '08', '09', '10', '11', '12',
           '13', '14', '15', '16', '17', '18',
           '19', '20', '21', '22', '23', '24',
           '25', '56', '57', '58', '59'}

# Verifica se será alterado o valor inicial
grupo_aumenta = {'56', '57', '58', '59'}

# Arredonda pra 30
grupo_2 = {'26', '27', '28', '29', '30', '31', '32', '33',
           '34', '35', '36', '37', '38', '39', '40', '41',
           '42', '43', '44', '45', '46', '47', '48', '49',
           '50', '51', '52', '53', '54', '55'}


# Arredondamentos para o horário
def arrendonda_hora(hora):
    if hora[-2:] in grupo_1:
        if hora[-2:] in grupo_aumenta:
            if hora[-5:-3] != '23':
                valor_novo = int(hora[-5:-3]) + 1
                hora = hora.replace(hora[-5:-3], str(valor_novo))
                hora = hora[:-2] + '00'
            else:
                valor_novo = '00'
                hora = hora.replace(hora[-5:-3], valor_novo)
                hora = hora[:-2] + '00'
        else:
            hora = hora[:-2] + '00'
    # Arredonda pra 30
    elif hora[-2:] in grupo_2:
        hora = hora[:-2] + '30'
    else:
        print('Horário inválido!')

    return hora
