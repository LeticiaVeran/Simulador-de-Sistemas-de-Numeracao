
## 👓 Análise Técnica e Apresentação do Código

# 🏅 Estrutura Geral:
- Código foi escrito em Python, com foco em duas funcionalidades principais:
- Conversão de números entre bases (binária, octal, decimal e hexadecimal)  
- Calculadora entre bases (suporta operações entre números em diferentes bases)

**A interface foi feita com Tkinter**, permitindo ao usuário interagir com o programa de forma visual e intuitiva.

# ❗Módulo de Conversão de Bases:
Entrada do Usuário
O usuário digita um número e escolhe:
- A base de origem
- A base de destino

 Exemplo: Converter 1011 da base binária para decimal.

# ❗Funcionamento Interno:
O código primeiro detecta se o número possui:
- Ponto flutuante (.)
- Sinal negativo (-)

 # 👣Passo a passo de conversão:
- Se for ponto flutuante: separa parte inteira e fracionária, converte ambas e soma.
- Tudo é convertido primeiro para decimal usando funções como:
bin_dec(), octal_dec(), hexa_dec()
- Depois, converte do decimal para a base desejada com funções como:
dec_bin(), dec_octal(), dec_hexa()

# 🧮 Módulo da Calculadora:
Entrada do Usuário:
- Número 1 com base
- Número 2 com base
- Operação (+, -, *, /)
- Base desejada para o resultado

 Exemplo: A5 (hexadecimal) + 1011 (binário) → resultado em octal

# 😎Funcionamento Interno:
- Conversão dos dois números para decimal, respeitando o tipo (inteiro, float, fração).
- Aplica a operação matemática escolhida:
        if operacao == "+":
            resultado_decimal = num1_decimal + num2_decimal
            steps_operacao = [f"Somando: {num1_decimal} + {num2_decimal} = {resultado_decimal}"]
- O resultado é então convertido da base decimal para a base final escolhida.
O código imprime todos os passos intermediários na interface para que o usuário entenda o que foi feito.

# 🤳🏻Interface Gráfica (Tkinter):
A interface contém:
- Tela inicial com três opções: Conversão, calculadora ou sair
- As duas primeiras funções abrem sua própria janela e a última fecha o programa.
- Utiliza elementos do Tkinter:
  - Entry para entrada de texto
  - OptionMenu para escolher as bases e operações
  - Button para iniciar a conversão ou cálculo
  - Text para mostrar o resultado e os passos explicativos

# 🤩Diferenciais da Interface:
- Design simples e direto
- Foco em acessibilidade e clareza
- Saída com *feedback explicativo*, não só o resultado final

# ‼️Principais Funções e Lógica:
Conversão de Bases:
- def bin_dec(num): ...
- def dec_bin(num): ...
- def octal_dec(num): ...
- def dec_octal(num): ...

# ❗Cada uma trata:
- Parte inteira
- Parte fracionária (multiplicação sucessiva ou divisão)
- Números negativos

# ❗Conversão com Frações:
def tratar_entrada_decimal(valor):
def base_para_decimal(num, base):
Divide numerador e denominador após convertê-los para decimal.

# ❗Cálculo entre Bases:
def calcular(): 
Responsável por:
- Interpretar bases
- Aplicar operação
- Converter o resultado para a base final
 Exemplo de Execução

# ❗Entrada:
Número 1: 10111  (Binário)
Número 2: AF     (Hexadecimal)
Operação: +
Resultado em: Decimal

# 👣 Passos Realizados:👣
- 1011.1 → Decimal = 11.5
- A.F → Decimal = 10.9375
- Soma: 11.5 + 10.9375 = 22.4375
- Resultado final: 22.4375

 # 🕵️‍♀️ Detalhes Técnicos🕵️‍♀️
- Todas as conversões e cálculos são manuais (sem uso de int(num, base)), para garantir controle e permitir explicações passo a passo.
- Uso de try-except para tratamento de erros básicos (entrada inválida, divisão por zero).
- Estrutura modular e organizada.

# 🆙 Melhorias Futuras🆙
- Frações em seu funcionamento amplo (não apenas na calculadora)
- Suporte a conversões diretas sem passar por decimal
- Exportar resultado e passos para .txt
- Histórico de operações
- Tema escuro/claro


# 🔚 Conclusão🔚
Este projeto tem como objetivo educacional, demonstrando:
- Como funcionam as conversões entre diferentes bases numéricas
- Como realizar operações matemáticas com bases distintas
- Como transformar conceitos matemáticos em código funcional e interativo
Ele também serve como ferramenta de aprendizado, pois explica ao usuário como chegou a cada resultado.


# 👩🏻👩🏻‍🦰👱🏻‍♀️👩🏻 Responsáveis:
Desenvolvedoras: Leticia, Emanuela, Gabrielli
Gerente: Valentina Ragnini
