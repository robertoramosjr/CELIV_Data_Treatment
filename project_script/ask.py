def file_name(data_name):
    return input(f"Insira o nome do arquivo para salvar os dados de {data_name} \n")


def file_path(measurement_name):
    return input(f"Insira o caminho do arquivo do {measurement_name} CELIV \n")


def device_area():
    return float(input('Qual a área de sessão trasnversal da amostra em cm quadrados? \n'))


def device_thickness():
    return float(input('Qual a espessura da amostra em nm? \n'))


def scan_rate():
    return float(input('Qual a taxa de varredura?'))


def initial_ramp_rate():
    return int(input('Qual a velocidade da primeira rampa da medida em V/s? \n'))


def final_ramp_rate():
    return int(input('Qual a velocidade da última rampa da medida em V/s? \n'))


def meas_number():
    return int(input('Quantas medidas de um mesmo tipo os arquivos possuem? \n'))


def ramp_step():
    return int(input('Qual o passo de variação da rampa de potencial entre uma medida e outra em V/s? \n'))
