import io

caminho_arquivo = '/home/fernando-araujo/Documentos/Desenvolvimentos/EFD/12.2025 SPED SC 88.txt'

with io.open(caminho_arquivo, 'r', encoding='ISO-8859-1') as file:
    linhas = list(file)

d100_atual = None
d100_com_problema = []

for i in range(len(linhas)):
    partes = linhas[i].split('|')
    if len(partes) < 2:
        continue

    registro = partes[1].strip()

    # Captura D100 completo
    if registro == 'D100':
        d100_atual = linhas[i].rstrip()  # mantém a linha inteira

    # Captura D190 dentro do D100
    elif registro == 'D190' and d100_atual:
        pares_completos = 0
        esperando_D197 = False
        encontrou_d195_ou_d197 = False
        j = i + 1

        while j < len(linhas):
            partes_j = linhas[j].split('|')
            if len(partes_j) < 2:
                j += 1
                continue

            reg_j = partes_j[1].strip()

            # Fim do D190
            if reg_j in ('D190', 'D100'):
                break

            if reg_j == 'D195':
                encontrou_d195_ou_d197 = True
                if esperando_D197:
                    # Encontrou D195 sem fechar par anterior
                    esperando_D197 = True
                else:
                    esperando_D197 = True

            elif reg_j == 'D197':
                encontrou_d195_ou_d197 = True
                if esperando_D197:
                    pares_completos += 1
                    esperando_D197 = False

            j += 1

        # REGRA FINAL: pelo menos 1 D195/D197 e pares < 3
        if encontrou_d195_ou_d197 and pares_completos < 3:
            d100_com_problema.append(d100_atual)

# OUTPUT FINAL
print('D100 com problema (faltando par(es) D195→D197):')
for d100 in d100_com_problema:
    print(d100)
