import substitute_box as s_box

def log(matriz):
    rkIndex = 0
    for roundKey in range(0,11):
        print('****RoundKey='+ str(rkIndex) +'****')
        for coluna in range(0,4):
            toPrint = ''
            for linha in range(0,4):
                toPrint += ' ' + hex(int(matriz[roundKey][coluna][linha]))
            print(toPrint)
        rkIndex += 1

def generateRoundConstant(roundKeyIndex):
    table = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54]
    return [table[roundKeyIndex -1], 0, 0, 0]

def subWord(palavra):
    s_result = []
    for i in range(4):
        mais_significativos = ''
        menos_significativos = ''
        bin_palavra = bin(palavra[i])[2:]
        # se tiver mais de 4 bits de extensão a partir do primeiro 1
        if(len(bin_palavra) > 4):
            mais_significativos = bin_palavra[:-4]
            menos_significativos = bin_palavra[-4:]
        else:
            menos_significativos = bin_palavra
        linha = 0
        coluna = 0
        if(mais_significativos != ''):
            linha = (int(mais_significativos, 2))
        if(menos_significativos != ''):
            coluna = (int(menos_significativos, 2))
        s_result.append(s_box.s_box[linha][coluna])
    return s_result

def rotWord(palavra):
    result = [0 for x in range(0,4)]
    primeiro = palavra[0]
    for i in range(1,4):
        result[i - 1] = palavra[i]
    result[3] = primeiro
    return result

def generateFirstColunmRoundKey(round_key_nova, round_key_anterior, roundKeyIndex):
    ultima_palavra = round_key_anterior[3]
    palavra_rotacionada = rotWord(ultima_palavra)
    palavra_substituida = subWord(palavra_rotacionada)
    roundConstant = generateRoundConstant(roundKeyIndex)
    xor_result = [0 for x in range(0,4)]
    for x in range(4):
        xor_result[x] = palavra_substituida[x] ^ roundConstant[x]
    result = [0 for x in range(0,4)]
    for x in range(4):
        round_key_anterior_IntValue = 0
        if(round_key_anterior[x] != b''):
            round_key_anterior_IntValue = int(round_key_anterior[0][x])
        result[x] = xor_result[x] ^ round_key_anterior_IntValue
    return result

def generateRoundKey(round_key_anterior, roundKeyIndex):
    round_key_nova = [[0 for x in range(4)] for y in range(4)]
    round_key_nova[0] = generateFirstColunmRoundKey(round_key_nova, round_key_anterior, roundKeyIndex)
    palavra_anterior = round_key_nova[0]
    nova_rk = [0 for y in range(4)]
    for coluna in range(1, 4):
        for linha in range(4):
            round_key_anterior_IntValue = 0
            if(round_key_anterior[coluna][linha] != b''):
                round_key_anterior_IntValue = int(round_key_anterior[coluna][linha])
            round_key_nova[coluna][linha] = round_key_anterior_IntValue ^ palavra_anterior[linha]
        palavra_anterior = round_key_nova[coluna]
    return round_key_nova

def expandirChave(round_key_original):
    key_schedule = []
    key_schedule.append(round_key_original)
    round_key_atual = round_key_original
    for i in range(1, 11):
        round_key_atual = generateRoundKey(round_key_atual, i)
        key_schedule.append(round_key_atual)
    return key_schedule

def app():
    #arq_origem_nome = input("Informe o arquivo a ser cifrado\n")
    #chave = input("Informe os bytes que compoem a chave de 128 bits.  Formato
    #-> '20,1,94,...'\n")
    #arq_cifrado_nome = input("Informe o nome do arquivo que será gerado\n")
    #texto_origem = open(arq_origem_nome, "r").read()
    chave =[0x41, 0x45, 0x49, 0x4d, 
            0x42, 0x46, 0x4a, 0x4e, 
            0x43, 0x47, 0x4b, 0x4f, 
            0x44, 0x48, 0x4c, 0x50]

    matriz_estado = [[0 for x in range(4)] for y in range(4)] 
    idx = 0
    for coluna in range(4):
        for linha in range(4):
            matriz_estado[linha][coluna] = chave[idx]
            idx += 1
    key_schedule = expandirChave(matriz_estado)
    log(key_schedule)

app()