def ask_file_name():
    return input("Insira o nome do arquivo para salvar \n")


def ask_file_path(measurement_name):
    return input(f"Insira o caminho do arquivo do {measurement_name} ramptime \n")


def ask_device_area():
    return float(input('Qual a área de sessão trasnversal da amostra? \n'))


def ask_device_thickness():
    return float(input('Qual a espessura da amostra? \n'))

