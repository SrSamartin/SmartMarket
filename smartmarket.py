import os

# Define o caminho do diretório desejado
caminho_desejado = "C:\\Users\\ander\\Desktop\\SmartMarket\\"

# Altera o diretório de trabalho atual
os.chdir(caminho_desejado)

# Recebe informação escrita do usuário (Referente ao bairro que o mesmo vive/se encontra.)
bairrousuario = input('Qual seu bairro? ')

def selecionar_itens(bairro):
    parceiros = {
        "Shopping Park": ["Super Maxi", "Luccas", "Celer", "Espark", "Mana", "Sempre Bom"],
        "Gavea Sul": ["Bahamas Mix"],
        "Jardim Karaiba": ["De Ville", "Bahamas Mix"],
        "Morada da Colina": ["Pao de Acucar", "Super Mercado BH"],
        "Jardim Holanda": ["Supermercado Leal"],
        "Sao Jorge": ["Super Maxi", "Bahamas Mix", "Supermercado Leal", "Bretas Atacarejo"],
        "Luizote": ["Super Maxi", "Emporio Alencar", "Emporio Nosso Lar", "Emporio Oliveira"],
        "Jardim Patricia": ["Bretas Atacarejo"]
    }

    if bairro in parceiros:
        return parceiros[bairro]
    else:
        return None

def ler_precos(bairro):
    mercados = selecionar_itens(bairro)
    precos = {}
    if mercados:
        for mercado in mercados:
            arquivo_precos = f"precos_{bairro.lower().replace(' ', '')}_{mercado.lower().replace(' ', '')}.txt"
            try:
                with open(arquivo_precos, "r") as arquivo:
                    linhas = arquivo.readlines()
                    precos[mercado] = {}
                    for linha in linhas:
                        item, preco = linha.strip().split(';')
                        # Limpar e formatar o preço
                        preco = preco.replace('R$ ', '').replace(',', '.').strip()
                        try:
                            precos[mercado][item] = float(preco)
                        except ValueError as e:
                            print(f"Erro ao converter o preço '{preco}' para float: {e}")
            except FileNotFoundError:
                print(f"Arquivo {arquivo_precos} não encontrado.")
    return precos

def melhor_custo_beneficio(precos):
    custo_final = {}
    for mercado, itens in precos.items():
        custo_total = sum(itens.values())
        custo_final[mercado] = custo_total
    melhor_mercado = min(custo_final, key=custo_final.get)
    return melhor_mercado, custo_final[melhor_mercado]

def melhor_custo_beneficio_item(precos):
    melhor_preco_por_item = {}
    for mercado, itens in precos.items():
        for item, preco in itens.items():
            if item not in melhor_preco_por_item or preco < melhor_preco_por_item[item][0]:
                melhor_preco_por_item[item] = (preco, mercado)
    return melhor_preco_por_item

# Obtemos a lista de mercados e seus preços para o bairro informado
precos = ler_precos(bairrousuario)

if precos:
    # Melhor custo-benefício de compra
    melhor_mercado, custo_total = melhor_custo_beneficio(precos)
    print(f"Melhor custo-benefício de compra: {melhor_mercado} com custo total de {custo_total:.2f}")

    # Melhor custo-benefício por preço de item
    melhor_preco_item = melhor_custo_beneficio_item(precos)
    print("Melhor custo-benefício por item:")
    for item, (preco, mercado) in melhor_preco_item.items():
        print(f"{item}: {preco:.2f} em {mercado}")
else:
    print("Não foi possível encontrar preços para o bairro informado.")
