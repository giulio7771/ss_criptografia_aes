import tabelas as tabelas

def log_matriz(matriz, titulo):
    print('****' + titulo + '****')
    for coluna in range(0,4):
        toPrint = ''
        for linha in range(0,4):
            toPrint += ' ' + hex(int(matriz[coluna][linha]))
        print(toPrint)

def log(round_schedule):
    rkIndex = 0
    for roundKey in range(0,11):
        print('****RoundKey=' + str(rkIndex) + '****')
        for coluna in range(0,4):
            toPrint = ''
            for linha in range(0,4):
                toPrint += ' ' + hex(int(round_schedule[roundKey][coluna][linha]))
            print(toPrint)
        rkIndex += 1

def divideByte(byte):
    # os 4 primeiro bytes representam a linha
    mais_significativos = ''
    # os 4 ultimos a coluna
    menos_significativos = ''
    bin_palavra = bin(byte)[2:]
    # se tiver mais de 4 bits significativos
    if(len(bin_palavra) > 4):
        mais_significativos = bin_palavra[:-4]
        menos_significativos = bin_palavra[-4:]
    else:
        menos_significativos = bin_palavra
    return [mais_significativos, menos_significativos]

def subByte(byte, tabela):
    bytes_divididos = divideByte(byte)
    # transforma os bits em int
    linha = 0
    coluna = 0
    if(bytes_divididos[0] != ''):
        linha = (int(bytes_divididos[0], 2))
    if(bytes_divididos[1] != ''):
        coluna = (int(bytes_divididos[1], 2))
    # substitui pela s_box
    return(tabela[linha][coluna])

def galois(byte_etapa3, byte_matriz):
    if (byte_etapa3 == 0 | byte_matriz == 0):
        return 0
    elif (byte_etapa3 == 1):
        return byte_matriz
    elif (byte_matriz == 1):
        return byte_etapa3

    termo1 = int(subByte(byte_etapa3, tabelas.l))
    termo2 = int(subByte(byte_matriz, tabelas.l))
    result_soma  = termo1 + termo2;
    if(result_soma > 255):
        result_soma = 255

    result = subByte(result_soma, tabelas.e)
    return result

def rodada5(matriz4, roundkey):
    result = [[0 for x in range(4)] for y in range(4)] 
    for y in range(4):
        for x in range(4):
            result[x][y] = matriz4[x][y] ^ roundkey[x][y]
    return result

def rodada4(matriz3):
    result = [[0 for x in range(4)] for y in range(4)]
    matriz_manipulacao = [[2,3,1,1],
                          [1,2,3,1],
                          [1,1,2,3],
                          [3,1,1,2]]
    for y in range(4):
        for x in range(4):
            for i in range(4):
                result[y][x] = galois(matriz3[0][y], matriz_manipulacao[y][0])
    return result

def rodada3(matriz):
    result = []
    nova_matriz = []
    for y in range(4):
        nova_linha = []
        for x in range(4):
            nova_linha.append(matriz[x][y])
        nova_matriz.append(nova_linha)
    result.append(nova_matriz[0])
    for q in range(1, 4):
        palavraRotacionada = rotWord(nova_matriz[q])
        for x in range(q - 1):
            palavraRotacionada = rotWord(palavraRotacionada)
        result.append(palavraRotacionada)
    return result

def rodada2(matriz):
    result = []
    for coluna in range(4):
        result.append(subWord(matriz[coluna], tabelas.s_box))
    return result

def rodada1(textoSimples, roundKey0):
    # xor textosimple, roundkey0
    result = []
    for coluna in range(4):
        y = []
        for linha in range(4):
            y.append(textoSimples[coluna][linha] ^ roundKey0[coluna][linha])
        result.append(y)
    return result

def cifragem(textoSimples, key_schedule):
    textoCifrado = rodada1(textoSimples, key_schedule[0])
    for i in range(11):
        log_matriz(textoCifrado, 'AddRoundKey-Round '+str(i))
        b = rodada2(textoCifrado)
        log_matriz(b, 'SubBytes-Round '+str(i))
        c = rodada3(b)
        log_matriz(c, 'ShiftRows-Round '+str(i))
        d = rodada4(c)
        log_matriz(d, 'MixedColumns-Round '+str(i))
        textoCifrado = rodada5(d,key_schedule[i])
        log_matriz(textoCifrado, 'addRoundKey-Round '+str(i))
    return textoCifrado

def generateRoundConstant(roundKeyIndex):
    # o numero da roundkey atual deve ser substituido na tabela
    table = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54]
    return [table[roundKeyIndex - 1], 0, 0, 0]

def subWord(palavra, tabela):
    # os bytes devem ser substituidos pela tabela da substitute_box.py
    s_result = []
    for i in range(4):
        result = subByte(palavra[i], tabela)
        s_result.append(result)
    return s_result

def rotWord(palavra):
    # o primeiro byte passa a ser o ultimo na lista
    result = [0 for x in range(0,4)]
    primeiro = palavra[0]
    for i in range(1,4):
        result[i - 1] = palavra[i]
    result[3] = primeiro
    return result

def generateFirstColunmRoundKey(round_key_nova, round_key_anterior, roundKeyIndex):
    # etapa 1
    ultima_palavra = round_key_anterior[3]
    # etapa 2
    palavra_rotacionada = rotWord(ultima_palavra)
    # etapa 3
    palavra_substituida = subWord(palavra_rotacionada, tabelas.s_box)
    # etapa 4
    roundConstant = generateRoundConstant(roundKeyIndex)
    # etapa 5
    xor_result = [0 for x in range(0,4)]
    for x in range(4):
        xor_result[x] = palavra_substituida[x] ^ roundConstant[x]
    result = [0 for x in range(0,4)]
    # etapa 6
    for x in range(4):
        round_key_anterior_IntValue = 0
        if(round_key_anterior[x] != b''):
            round_key_anterior_IntValue = int(round_key_anterior[0][x])
        result[x] = xor_result[x] ^ round_key_anterior_IntValue
    return result

def generateRoundKey(round_key_anterior, roundKeyIndex):
    round_key_nova = [[0 for x in range(4)] for y in range(4)]
    # primeira coluna é gerada separadamente
    round_key_nova[0] = generateFirstColunmRoundKey(round_key_nova, round_key_anterior, roundKeyIndex)
    palavra_anterior = round_key_nova[0]
    nova_rk = [0 for y in range(4)]
    # as outras 3 colunas são geradas com xor entre a primeira
    # coluna e a coluna correspondente na roundkey anterior
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
    # primeira roundkey é a matriz estado
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
    chave = [0x41, 0x45, 0x49, 0x4d, 
            0x42, 0x46, 0x4a, 0x4e, 
            0x43, 0x47, 0x4b, 0x4f, 
            0x44, 0x48, 0x4c, 0x50]
    textoSimples = [0x44, 0x45, 0x53, 0x45, 0x4e, 0x56, 0x4f, 0x4c, 0x56, 0x49, 0x4d, 0x45, 0x4e, 0x54, 0x4f, 0x21]

    matriz_estado = [[0 for x in range(4)] for y in range(4)] 
    idx = 0
    # gera matriz 4x4 com valores da chave
    for coluna in range(4):
        for linha in range(4):
            matriz_estado[linha][coluna] = chave[idx]
            idx += 1
    # retorna as 11 roundkeys
    key_schedule = expandirChave(matriz_estado)
    log(key_schedule)

    matriz_textoSimples = [[0 for x in range(4)] for y in range(4)] 
    idx = 0
    # gera matriz 4x4 com valores do texto simples
    for coluna in range(4):
        for linha in range(4):
            matriz_textoSimples[coluna][linha] = textoSimples[idx]
            idx += 1

    textoCifrado = cifragem(matriz_textoSimples, key_schedule)
    log_matriz(textoCifrado, 'Texto cifrado')

app()