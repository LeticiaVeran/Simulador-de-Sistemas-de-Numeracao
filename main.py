import tkinter as tk
from fractions import Fraction

#funcao para tratar as entradas em fracao na calculadora
def tratar_entrada_decimal(valor):
    """
    Aceita tanto número decimal quanto fração tipo '3/4' e converte para float.
    """
    try:
        if "/" in valor:
            return float(Fraction(valor))
        else:
            return float(valor)
    except ValueError:
        raise ValueError(f"Entrada inválida para número decimal: {valor}")
    
# === Funções de conversão ===

# Converte de Decimal para Binário com representações de sinal
def dec_bin(num):

    steps = []

    try:
        num = float(num)
    except ValueError:
        return "Erro: Número inválido!", ["Erro: Por favor, insira um número válido."]

    negativo = num < 0
    inteiro = int(abs(num))
    frac = abs(num) - inteiro

    # Parte inteira em binário usando o método do resto
    parte_inteira_bin = ''
    temp = inteiro
    steps.append("\nConvertendo parte inteira:")
    while temp > 0:
        resto = temp % 2
        parte_inteira_bin = str(resto) + parte_inteira_bin
        steps.append(f"{temp} ÷ 2 = {temp // 2} (resto = {resto}) -> binário parcial: {parte_inteira_bin}") 
        temp //= 2


    if inteiro == 0:
        parte_inteira_bin = '0'
        steps.append(f"Parte inteira 0 convertida: {parte_inteira_bin}")

    # Parte fracionária em binário usando o método do resto
    parte_frac_bin = ''
    temp_frac = frac
    count = 0
    steps.append("\nConvertendo parte fracionária:")
    while temp_frac > 0 and count < 10:  # Limite para garantir que fique dentro de 10 dígitos
        temp_frac *= 2
        bit = int(temp_frac)
        parte_frac_bin += str(bit)
        steps.append(f"{temp_frac/2} * 2 = {temp_frac} bit = {bit} -> binário parcial: {parte_frac_bin}")
        temp_frac -= bit
        count += 1

    # Monta binário bruto
    if parte_frac_bin:
        binario_bruto = parte_inteira_bin + '.' + parte_frac_bin
    else:
        binario_bruto = parte_inteira_bin

    if negativo:
        binario_bruto = '-' + binario_bruto
    steps.append(f"\nBinário bruto: {binario_bruto}")

    # ---------- Sinal e Magnitude ----------
    if negativo:
        sinal_mag = '1' + parte_inteira_bin + '.' + parte_frac_bin
    else:
        sinal_mag = '0' + parte_inteira_bin + '.' + parte_frac_bin

    steps.append(f"Sinal e Magnitude (adiciona 1 na frente para representar o sinal): {sinal_mag}")

    # ---------- Complemento de 1 ----------
    if negativo:
        bin_sem_ponto = parte_inteira_bin + parte_frac_bin
        comp1 = ''.join('1' if b == '0' else '0' for b in bin_sem_ponto)

        # Reinsere o ponto na posição correta
        if parte_frac_bin:
            pos_ponto = len(parte_inteira_bin)
            complemento_1 = comp1[:pos_ponto] + '.' + comp1[pos_ponto:]
        else:
            complemento_1 = comp1

        complemento_1 = '1' + complemento_1  # adiciona bit de sinal
    else:
        complemento_1 = '0' + binario_bruto.replace('-', '')

    steps.append(f"Complemento de 1 (inverte os digitos para números negativos): {complemento_1}")

    # ---------- Complemento de 2 ----------
    if negativo:
        # Soma 1 ao complemento de 1 (sem o ponto)
        comp1_sem_ponto = comp1
        soma = int(comp1_sem_ponto, 2) + 1
        comp2_bin = bin(soma)[2:].zfill(len(comp1_sem_ponto))

        # Reinsere o ponto
        if parte_frac_bin:
            complemento_2 = comp2_bin[:pos_ponto] + '.' + comp2_bin[pos_ponto:]
        else:
            complemento_2 = comp2_bin

        complemento_2 = '1' + complemento_2
    else:
        complemento_2 = complemento_1

    steps.append(f"Complemento de 2 (inverte os digitos e soma 1 para números negativos): {complemento_2}")

     # ---------- Representação Completa IEEE 754 ----------

    steps.append("\nRepresentação em ponto flutuante (IEEE 754):")

    # Normalizar número
    if parte_inteira_bin != '0':
        # Se a parte inteira não for 0, normaliza movendo o ponto
        deslocamento = len(parte_inteira_bin) - 1
        mantissa = (parte_inteira_bin[1:] + parte_frac_bin)[:23]  # Pega até 23 bits após o ponto
    else:
        # Se a parte inteira for 0, normaliza começando da parte fracionária
        deslocamento = -1
        for i, bit in enumerate(parte_frac_bin):
            if bit == '1':
                deslocamento -= i + 1
                mantissa = (parte_frac_bin[i + 1:])[:23]
                break
        else:
            mantissa = '0' * 23  # Número muito pequeno, mantissa é 0

    # Calcula expoente com "bias" de 127 (IEEE 754 de 32 bits)
    expoente = deslocamento + 127
    expoente_bin = f"{expoente:08b}"

    # Ajusta mantissa para ter 23 bits
    mantissa = mantissa.ljust(23, '0')

    # Monta IEEE 754
    bit_sinal = '1' if negativo else '0'
    ponto_fluante = f"{bit_sinal} {expoente_bin} {mantissa}"

    steps.append(f"Bit de sinal: {bit_sinal}")
    steps.append(f"Expoente (deslocamento + 127): {deslocamento} + 127 = {expoente} -> {expoente_bin}")
    steps.append(f"Mantissa (23 bits): {mantissa}")
    steps.append(f"Ponto flutuante (IEEE 754): {ponto_fluante}")

    resultados = binario_bruto


    return resultados, steps

# Converte de Binário para Decimal (suporta ponto flutuante e negativo)
def bin_dec(bin_str):
    steps = [f"Convertendo binário {bin_str} para decimal:\n"]

    # Verifica se o binário contém apenas 0s e 1s (permitindo '-' no começo)
    if any(bit not in '01' for bit in bin_str.replace('.', '').replace('-', '')):
        return "Erro: Número binário inválido!", ["Erro: O número binário só pode conter os dígitos 0 e 1."]

    # Detecta se é negativo
    negativo = bin_str.startswith('-')
    if negativo:
        bin_str = bin_str[1:]  # Remove o sinal pra calcular

    if '.' in bin_str:
        inteiro, frac = bin_str.split('.')
    else:
        inteiro, frac = bin_str, ''

    num = 0
    # Converte a parte inteira
    steps.append("Convertendo parte inteira para decimal:")
    for i, bit in enumerate(reversed(inteiro)):
        if bit == '1':
            valor = 2 ** i
            num += valor
            steps.append(f"1 * 2^{i} = {valor}, soma parcial = {num}")
        else:
            steps.append(f"0 * 2^{i} = 0, soma parcial = {num}")

    # Converte a parte fracionária
    steps.append("\nConvertendo parte fracionária para decimal:")
    for i, bit in enumerate(frac):
        if bit == '1':
            valor = 2 ** -(i + 1)
            num += valor
            steps.append(f"Parte fracionária: 1 * 2^-{i + 1} = {valor}, soma parcial = {num}")
        else:
            steps.append(f"Parte fracionária: 0 * 2^-{i + 1} = 0, soma parcial = {num}")

    if negativo:
        num = -num
        steps.append("\nComo o número original era negativo, aplicamos o sinal '-' ao resultado.")

    steps.append(f"\nResultado final em decimal: {num}\n")
    return str(num), steps

# Converte de Decimal para Octal (suporta ponto flutuante)
def dec_octal(num):
    steps = []
    try:
        num = float(num)
    except ValueError:
        return "Erro: Número inválido!", ["Erro: Por favor, insira um número válido."]

    sinal = '-' if num < 0 else ''
    inteiro = int(abs(num))
    frac = abs(num) - inteiro

    steps.append(f"Número recebido: {num}")
    steps.append(f"Sinal: {'Negativo' if sinal else 'Positivo'}")
    steps.append(f"Parte inteira: {inteiro}, Parte fracionária: {frac:.10f}")

    # Parte inteira
    parte_inteira = ''
    if inteiro == 0:
        parte_inteira = '0'
        steps.append("Parte inteira é 0, octal: 0")
    else:
        steps.append("\nConvertendo parte inteira para octal:")
        temp = inteiro
        while temp > 0:
            resto = temp % 8
            parte_inteira = str(resto) + parte_inteira
            steps.append(f"{temp} ÷ 8 = {temp // 8} (resto = {resto}) -> octal parcial: {parte_inteira}")
            temp //= 8

    # Parte fracionária
    parte_frac = ''
    count = 0
    temp_frac = frac
    if frac != 0:
        steps.append("\nConvertendo parte fracionária:")
    while temp_frac > 0 and count < 10:
        digito2 = temp_frac
        temp_frac *= 8
        digito = int(temp_frac)
        parte_frac += str(digito)
        steps.append(f"{digito2} * 8 = {temp_frac:.10f} -> parte inteira = {digito}, octal parcial: {parte_frac}")
        temp_frac -= digito
        count += 1

    octal = parte_inteira + ('.' + parte_frac if parte_frac else '')
    full_octal = sinal + octal
    steps.append(f"\nNúmero final em octal: {full_octal}")
    return full_octal, steps

# Converte de Decimal para Hexadecimal (suporta ponto flutuante)
def dec_hexa(num):
    steps = []
    try:
        num = float(num)
    except ValueError:
        return "Erro: Número inválido!", ["Erro: Por favor, insira um número válido."]

    sinal = '-' if num < 0 else ''
    inteiro = int(abs(num))
    frac = abs(num) - inteiro
    hex_digits = "0123456789ABCDEF"

    parte_inteira = ''
    if inteiro == 0:
        parte_inteira = '0'
        steps.append("Parte inteira 0 convertida para hexadecimal: 0")
    else:
        temp = inteiro
        steps.append("\nConvertendo parte inteira para hexadecimal:")
        while temp > 0:
            resto = temp % 16
            parte_inteira = hex_digits[resto] + parte_inteira
            steps.append(f"{temp} ÷ 16 = {temp // 16} (resto = {resto}, dígito = {hex_digits[resto]}) -> hexadecimal parcial: {parte_inteira}")
            temp //= 16

    parte_frac = ''
    count = 0
    temp_frac = frac
    if frac != 0:
        steps.append("\nConvertendo parte fracionária:")
    while temp_frac > 0 and count < 10:
        temp_frac *= 16
        digito = int(temp_frac)
        parte_frac += hex_digits[digito]
        steps.append(f"{temp_frac/16} * 16 = {temp_frac}, dígito = {hex_digits[digito]}, hexadecimal parcial: {parte_frac}")
        temp_frac -= digito
        count += 1

    hexa = parte_inteira + ('.' + parte_frac if parte_frac else '')
    full_hexa = sinal + hexa
    steps.append(f"\nNúmero hexadecimal final: {full_hexa}")
    return full_hexa, steps

#converte octal para decimal
def octal_dec(octal_str):
    steps = [f"Convertendo octal {octal_str} para decimal:\n"]
    
    # Detecta e trata o sinal
    sinal = -1 if octal_str.startswith('-') else 1
    octal_str = octal_str.lstrip('-')

    # Separa parte inteira e fracionária
    if '.' in octal_str:
        inteiro, frac = octal_str.split('.')
    else:
        inteiro, frac = octal_str, ''

    num = 0

    # Converte parte inteira
    steps.append(f"Parte inteira:")
    for i, dig in enumerate(reversed(inteiro)):
        valor = int(dig) * (8 ** i)
        num += valor
        steps.append(f"{dig} * 8^{i} = {valor}, soma parcial = {num}")

    # Converte parte fracionária
    steps.append(f"\nParte fracionária:")
    for i, dig in enumerate(frac):
        valor = int(dig) * (8 ** -(i + 1))
        num += valor
        steps.append(f"{dig} * 8^-{i + 1} = {valor}, soma parcial = {num}")

    resultado = sinal * num
    steps.append(f"\nResultado final em decimal: {resultado}")
    return str(resultado), steps

#converte hexa para decimal
def hexa_dec(hexa_str):
    steps = [f"Convertendo hexadecimal {hexa_str} para decimal:\n"]
    hex_digits = "0123456789ABCDEF"

    # Detecta e trata o sinal
    sinal = -1 if hexa_str.startswith('-') else 1
    hexa_str = hexa_str.lstrip('-').upper()

    # Separa parte inteira e fracionária
    if '.' in hexa_str:
        inteiro, frac = hexa_str.split('.')
    else:
        inteiro, frac = hexa_str, ''

    num = 0

    # Converte parte inteira
    steps.append(f"Parte inteira: ")
    for i, dig in enumerate(reversed(inteiro)):
        valor = hex_digits.index(dig) * (16 ** i)
        num += valor
        steps.append(f"{dig} * 16^{i} = {valor}, soma parcial = {num}")

    # Converte parte fracionária
    steps.append(f"\nParte fracionária:")
    for i, dig in enumerate(frac):
        valor = hex_digits.index(dig) * (16 ** -(i + 1))
        num += valor
        steps.append(f"{dig} * 16^-{i + 1} = {valor}, soma parcial = {num}")

    resultado = sinal * num
    steps.append(f"\nResultado final em decimal: {resultado}")
    return str(resultado), steps

# Funções combinadas para ponto flutuante
def bin_octal(bin_str):
    decimal, steps_decimal = bin_dec(bin_str)
    octal, steps_octal = dec_octal(decimal)
    return octal, steps_decimal + steps_octal[2:]

def bin_hexa(bin_str):
    decimal, steps_decimal = bin_dec(bin_str)
    hexa, steps_hexa = dec_hexa(decimal)
    # Junta todos os passos sem cortar o primeiro passo do hexa
    return hexa, steps_decimal + steps_hexa

def octal_bin(oct_str):
    decimal, steps_decimal = octal_dec(oct_str)
    binario, steps_bin = dec_bin(decimal)
    return binario, steps_decimal + steps_bin[1:]

def octal_hexa(oct_str):
    decimal, steps_decimal = octal_dec(oct_str)
    hexa, steps_hexa = dec_hexa(decimal)
    return hexa, steps_decimal + steps_hexa[1:]

def hexa_bin(hexa_str):
    decimal, steps_decimal = hexa_dec(hexa_str)
    binario, steps_bin = dec_bin(decimal)
    return binario, steps_decimal + steps_bin[1:]

def hexa_octal(hexa_str):
    decimal, steps_decimal = hexa_dec(hexa_str)
    octal, steps_octal = dec_octal(decimal)
    return octal, steps_decimal + steps_octal[1:]

# Funções da interface gráfica
def abrir_conversao():
    menu_frame.pack_forget()
    calculadora_frame.pack_forget()
    conversao_frame.pack(pady=20)

def abrir_calculadora():
    menu_frame.pack_forget()
    conversao_frame.pack_forget()
    calculadora_frame.pack(pady=20)

def voltar_menu():
    conversao_frame.pack_forget()
    calculadora_frame.pack_forget()
    menu_frame.pack(pady=50)

def executar():
    entrada = entry.get()
    origem = from_option.get()
    destino = to_option.get()

    entrada = entrada.replace(',', '.')

    # Verificar se a entrada binária é válida antes de qualquer outra verificação
    if origem == "Binário" and any(bit not in '01' for bit in entrada.replace('.', '').replace('-', '')):
        resultado = "Erro: Número binário inválido!"
        steps = ["Erro: O número binário só pode conter os dígitos 0 e 1, além de um possível sinal de negativo '-'."]
    elif origem == destino:
        resultado = entrada
        steps = ["Origem e destino são iguais! Resultado: " + resultado]
    elif origem == "Decimal" and destino == "Binário":
        resultado, steps = dec_bin(entrada)
    elif origem == "Binário" and destino == "Decimal":
        resultado, steps = bin_dec(entrada)
    elif origem == "Decimal" and destino == "Octal":
        resultado, steps = dec_octal(entrada)
    elif origem == "Decimal" and destino == "Hexadecimal":
        resultado, steps = dec_hexa(entrada)
    elif origem == "Octal" and destino == "Decimal":
        resultado, steps = octal_dec(entrada)
    elif origem == "Hexadecimal" and destino == "Decimal":
        resultado, steps = hexa_dec(entrada)
    elif origem == "Binário" and destino == "Octal":
        resultado, steps = bin_octal(entrada)
    elif origem == "Binário" and destino == "Hexadecimal":
        resultado, steps = bin_hexa(entrada)
    elif origem == "Octal" and destino == "Binário":
        resultado, steps = octal_bin(entrada)
    elif origem == "Octal" and destino == "Hexadecimal":
        resultado, steps = octal_hexa(entrada)
    elif origem == "Hexadecimal" and destino == "Binário":
        resultado, steps = hexa_bin(entrada)
    elif origem == "Hexadecimal" and destino == "Octal":
        resultado, steps = hexa_octal(entrada)
    else:
        resultado = "Conversão não implementada! 🚧"
        steps = [resultado]

    result_label_conv.config(text=f"Resultado: {resultado}")
    steps_text_conv.delete(1.0, tk.END)
    steps_text_conv.insert(tk.END, "\n".join(steps))

def converter_resultado(resultado, base_destino):
    steps = []
    
    # Verifica se o número é float ou string
    try:
        # Tenta converter para float, se não for possível, mantemos como string
        num = float(resultado)
    except ValueError:
        num = resultado
    
    # Faz a conversão para a base de destino
    if base_destino == "Decimal":
        return str(num), steps
    elif base_destino == "Binário":
        return dec_bin(num)
    elif base_destino == "Octal":
        return dec_octal(num)
    elif base_destino == "Hexadecimal":
        return dec_hexa(num)
    else:
        return "Base de saída inválida!", []

def base_para_decimal(num, base):
    steps = []

    # Se o número for uma fração (ex: 1011/01)
    if "/" in num:
        numerador, denominador = num.split('/')
        steps.append(f"Número recebido como fração: {num}")
        steps.append(f"Separando numerador: {numerador} e denominador: {denominador}")

        # Converte o numerador e denominador para decimal de acordo com a base
        try:
            # Verifica a base e converte numerador e denominador
            if base == "Binário":
                numerador_decimal, steps_numerador = bin_dec(numerador)
                denominador_decimal, steps_denominador = bin_dec(denominador)
            elif base == "Octal":
                numerador_decimal, steps_numerador = octal_dec(numerador)
                denominador_decimal, steps_denominador = octal_dec(denominador)
            elif base == "Hexadecimal":
                numerador_decimal, steps_numerador = hexa_dec(numerador)
                denominador_decimal, steps_denominador = hexa_dec(denominador)
            else:
                raise ValueError("Base inválida para conversão!")

            steps += steps_numerador + steps_denominador
        except ValueError as e:
            return f"Erro: {e}", ["Erro: Não foi possível converter a fração."]

        # Verifica se o denominador é 0
        if float(denominador_decimal) == 0:
            return "Erro: Divisão por zero!", ["Erro: O denominador da fração não pode ser zero."]

        # Realiza a divisão
        resultado = float(numerador_decimal) / float(denominador_decimal)
        steps.append(f"Realizando divisão: {numerador_decimal} ÷ {denominador_decimal} = {resultado}")
        return str(resultado), steps

    # Caso contrário, converte diretamente (caso seja inteiro ou decimal sem fração)
    else:
        # Verifica se a string é válida conforme a base
        if base == "Binário":
            # Verifica se o número binário é válido
            if any(bit not in '01' for bit in num.replace('.', '').replace('-', '')):
                return "Erro: Número binário inválido!", ["Erro: O número binário só pode conter os dígitos 0 e 1."]
        elif base == "Octal":
            # Verifica se o número octal é válido
            if any(bit not in '01234567' for bit in num.replace('.', '').replace('-', '')):
                return "Erro: Número octal inválido!", ["Erro: O número octal só pode conter os dígitos de 0 a 7."]
        elif base == "Hexadecimal":
            # Verifica se o número hexadecimal é válido
            if any(bit not in '0123456789ABCDEFabcdef' for bit in num.replace('.', '').replace('-', '')):
                return "Erro: Número hexadecimal inválido!", ["Erro: O número hexadecimal só pode conter os dígitos de 0-9 e A-F."]
        else:
            raise ValueError("Base inválida!")

    # Converte o número diretamente de acordo com a base
    if base == "Binário":
        resultado, steps = bin_dec(str(num))  # Passa como string para a função bin_dec
        return resultado, steps
    elif base == "Octal":
        resultado, steps = octal_dec(str(num))  # Passa como string para a função octal_dec
        return resultado, steps
    elif base == "Hexadecimal":
        resultado, steps = hexa_dec(str(num))  # Passa como string para a função hexa_dec
        return resultado, steps 
    else:
        raise ValueError("Base inválida!")

def calcular():
    num1 = num1_entry.get()
    num2 = num2_entry.get()
    operacao = operacao_var.get()
    base1 = base1_var.get()
    base2 = base2_var.get()
    base_resultado = base_resultado_var.get()

    num1 = num1.replace(',', '.')
    num2 = num2.replace(',', '.')

    try:
        # Converte os números para decimal
        if base1 == "Decimal":
            num1_decimal = tratar_entrada_decimal(num1)
            steps1 = [f"Entrada em base 10: {num1} -> {num1_decimal}"]
        else:
            num1_decimal, steps1 = base_para_decimal(num1, base1)

        if base2 == "Decimal":
            num2_decimal = tratar_entrada_decimal(num2)
            steps2 = [f"Entrada em base 10: {num2} -> {num2_decimal}"]
        else:
            num2_decimal, steps2 = base_para_decimal(num2, base2)

        # Certificando-se de que os números são de tipo float ou int para operação matemática
        num1_decimal = float(num1_decimal)  # Garante que é um número decimal
        num2_decimal = float(num2_decimal)

        # Realiza a operação matemática conforme o tipo de operação
        if operacao == "+":
            resultado_decimal = num1_decimal + num2_decimal
            steps_operacao = [f"Somando: {num1_decimal} + {num2_decimal} = {resultado_decimal}"]
        elif operacao == "-":
            resultado_decimal = num1_decimal - num2_decimal
            steps_operacao = [f"Subtraindo: {num1_decimal} - {num2_decimal} = {resultado_decimal}"]
        elif operacao == "*":
            resultado_decimal = num1_decimal * num2_decimal
            steps_operacao = [f"Multiplicando: {num1_decimal} * {num2_decimal} = {resultado_decimal}"]
        elif operacao == "/":
            if num2_decimal == 0:
                raise ValueError("Não é possível dividir por zero!")
            resultado_decimal = num1_decimal / num2_decimal
            steps_operacao = [f"Dividindo: {num1_decimal} / {num2_decimal} = {resultado_decimal}"]
        else:
            raise ValueError("Operação inválida!")

        # Converte o resultado para a base desejada
        resultado, steps_conversao = converter_resultado(str(resultado_decimal), base_resultado)  # Converte para string aqui
        steps = steps1 + steps2 + steps_operacao + steps_conversao

        # Exibe o resultado e os passos no GUI
        result_label_calc.config(text=f"Resultado: {resultado}")
        steps_text_calc.delete(1.0, tk.END)
        steps_text_calc.insert(tk.END, "\n".join(steps))

    except ValueError as e:
        # Em caso de erro, exibe a mensagem de erro
        result_label_calc.config(text=f"Erro: {e}")
        steps_text_calc.delete(1.0, tk.END)
        steps_text_calc.insert(tk.END, f"Erro: {e}")

# Interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conversor e Calculadora")
    root.geometry("700x700")

    # Menu principal
    menu_frame = tk.Frame(root)
    menu_frame.pack(pady=50)

    menu_label = tk.Label(menu_frame, text="Escolha uma opção:", font=("Arial", 16))
    menu_label.pack(pady=20)

    conversao_button = tk.Button(menu_frame, text="1. Conversão de Bases", font=("Arial", 14), command=abrir_conversao)
    conversao_button.pack(pady=10)

    calculadora_button = tk.Button(menu_frame, text="2. Calculadora", font=("Arial", 14), command=abrir_calculadora)
    calculadora_button.pack(pady=10)

    sair_button = tk.Button(menu_frame, text="3. Sair", font=("Arial", 14), command=root.destroy)
    sair_button.pack(pady=10)

    # Tela de conversão
    conversao_frame = tk.Frame(root)
    label = tk.Label(conversao_frame, text="Digite o número:", font=("Arial", 14))
    label.pack(pady=10)
    entry = tk.Entry(conversao_frame, font=("Arial", 14))
    entry.pack(pady=5)

    from_option = tk.StringVar(conversao_frame)
    from_option.set("Decimal")
    to_option = tk.StringVar(conversao_frame)
    to_option.set("Binário")

    frame_options = tk.Frame(conversao_frame)
    frame_options.pack(pady=10)
    tk.Label(frame_options, text="De:", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    tk.OptionMenu(frame_options, from_option, "Decimal", "Binário", "Octal", "Hexadecimal").grid(row=0, column=1)
    tk.Label(frame_options, text="Para:", font=("Arial", 12)).grid(row=0, column=2, padx=10)
    tk.OptionMenu(frame_options, to_option, "Decimal", "Binário", "Octal", "Hexadecimal").grid(row=0, column=3)

    button = tk.Button(conversao_frame, text="Converter", command=executar, font=("Arial", 14), bg="lightblue")
    button.pack(pady=20)

    result_label_conv = tk.Label(conversao_frame, text="Resultado:", font=("Arial", 14), fg="green")
    result_label_conv.pack(pady=10)

    steps_text_conv = tk.Text(conversao_frame, width=80, height=20, font=("Arial", 10))
    steps_text_conv.pack(pady=10)

    voltar_button1 = tk.Button(conversao_frame, text="Voltar ao Menu", command=voltar_menu, font=("Arial", 12), bg="lightgrey")
    voltar_button1.pack(pady=10)

    # Tela da calculadora
    calculadora_frame = tk.Frame(root)

    num1_label = tk.Label(calculadora_frame, text="Número 1:", font=("Arial", 12))
    num1_label.pack()

    num1_entry = tk.Entry(calculadora_frame)
    num1_entry.pack(pady=5)

    base1_var = tk.StringVar()
    base1_var.set("Decimal")

    base1_menu = tk.OptionMenu(calculadora_frame, base1_var, "Decimal", "Binário", "Octal", "Hexadecimal")
    base1_menu.pack(pady=5)

    opr_label = tk.Label(calculadora_frame, text="Operação:", font=("Arial", 12))
    opr_label.pack()

    operacao_var = tk.StringVar()
    operacao_var.set("+")

    operacao_menu = tk.OptionMenu(calculadora_frame, operacao_var, "+", "-", "*", "/")
    operacao_menu.pack(pady=5)

    num2_label = tk.Label(calculadora_frame, text="Número 2:", font=("Arial", 12))
    num2_label.pack()

    num2_entry = tk.Entry(calculadora_frame)
    num2_entry.pack(pady=5)

    base2_var = tk.StringVar()
    base2_var.set("Decimal")

    base2_menu = tk.OptionMenu(calculadora_frame, base2_var, "Decimal", "Binário", "Octal", "Hexadecimal")
    base2_menu.pack(pady=5)

    base_resultado_var = tk.StringVar()
    base_resultado_var.set("Decimal")

    base_resultado_label = tk.Label(calculadora_frame, text="Base do Resultado:", font=("Arial", 10))
    base_resultado_label.pack(pady=5)

    base_resultado_menu = tk.OptionMenu(calculadora_frame, base_resultado_var, "Decimal", "Binário", "Octal", "Hexadecimal")
    base_resultado_menu.pack(pady=5)

    calcular_button = tk.Button(calculadora_frame, text="Calcular", command=calcular, font=("Arial", 14), bg="lightblue")
    calcular_button.pack(pady=10)

    result_label_calc = tk.Label(calculadora_frame, text="Resultado: ", font=("Arial", 12), fg="green")
    result_label_calc.pack(pady=5)

    steps_text_calc = tk.Text(calculadora_frame, height=10, width=60)
    steps_text_calc.pack()

    voltar_button2 = tk.Button(calculadora_frame, text="Voltar ao Menu", command=voltar_menu, font=("Arial", 12), bg="lightgrey")
    voltar_button2.pack(pady=10)

    root.mainloop()