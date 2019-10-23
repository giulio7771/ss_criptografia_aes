
def rotacionar_palavra(palavra):
    retorno = []
    primeiro = palavra[0]
    for i in range(1,4):
        retorno[i - 1] = retorno [i]
    retorno[3] = primeiro
    return retorno

def generateFirstColunmRoundKey(round_key_nova, round_key_anterior):
    ultima_palavra = round_key_anterior[:][3]
    rotacionar_palavra(ultima_palavra)

def generateRoundKey(round_key_anterior):
    round_key_nova = [[0 for x in range(4)] for y in range(4)]
    round_key_nova = generateFirstColunmRoundKey(round_key_nova, round_key_anterior)
    for i in range(0,4):
        for j in range(1,4):
            round_key_nova[i][j] = round_key_anterior[i][j-1] ^ round_key_nova[i][j-1]
    return round_key_nova

def expandirChave(round_key_original):
    chave_mapa = []
    chave_mapa.append(round_key_original)
    round_key_atual = round_key_original
    for i in range(10):
        round_key_atual = generateRoundKey(round_key_atual)
        chave_mapa.append(round_key_atual)
    return chave_mapa

def app():
    #arq_origem_nome = input("Informe o arquivo a ser cifrado\n")
    #chave = input("Informe os bytes que compoem a chave de 128 bits. Formato -> '20,1,94,...'\n")
    #arq_cifrado_nome = input("Informe o nome do arquivo que será gerado\n")
    #texto_origem = open(arq_origem_nome, "r").read()
    chave = "1,2,3,4,5,6,7,8,9,10,A,12,13,14,15,16"
    chaves = chave.split(",")
    chaves_mapa = [[0 for x in range(4)] for y in range(4)] 
    idx = 0
    for i in range(4):
        for j in range(4):
            print(chaves[idx])
            chaves_mapa[j][i] = chaves[idx].encode()
            idx += 1
    expandirChave(chaves_mapa)

app()