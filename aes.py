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
    for i in chaves_mapa:
        print(type(i[0]))

app()