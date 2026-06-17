import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

try:
    print('Carregando dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep = ';', encoding= 'iso-8859-1')
    #print(df_ocorrencias.head(10))

    df_estelionato = df_ocorrencias [['mes_ano', 'estelionato']]
    #print(df_estelionato.head(10))

    df_estelionato = df_estelionato.groupby('mes_ano', as_index=False)['estelionato'].sum()
    #print(df_estelionato)

    df_estelionato = df_estelionato.sort_values(by = 'estelionato', ascending= False)
    #print(df_estelionato)
    
    df_estelionato_total = df_ocorrencias['estelionato'].sum()
    #print(df_estelionato_total)

except Exception as e:
    print(f'Erro ao obter os dados: {e}')



try:
    #print('Calculando medidas...')

    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia_percentual = abs((media_estelionato - mediana_estelionato)/ mediana_estelionato * 100)

    #print('\nMedidas de Tendência Central')
    #print(30 * '=')

    #print(f'Média de estelionatos: {media_estelionato:.2f}')
    #print(f'Mediana dos estelionatos: {mediana_estelionato:.2f}')
    #print(f'Distância percentual entre a média e a mediana: {distancia_percentual:.2f} %')


except Exception as e:
    print(f'Erro ao processar as medidas: {e}')


try:
    #print('Processado os quartis...')
    q1 = np.quantile(array_estelionato, .25)
    q3 = np.quantile(array_estelionato, .75)

    #print('\nQuartis')
    #print(30 * '=')

    #print(f'Q1 = {q1}')
    #print(f'Q3 = {q3}')
    
    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1]
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]

    #print(df_estelionato_menores)
    #print(df_estelionato_maiores)

except Exception as e:
    print(f'Erro ao obter a distribuição: {e}')



try:
    print('Calculando outliers...')

    maximo = np.max(array_estelionato)
    minimo = np.min(array_estelionato)
    amplitude = maximo - minimo


    iqr = q3 - q1

    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    #print(limite_inferior)
    #print(limite_superior)


except Exception as e:
    print(f'Erro ao calcular os outliers: {e}')



try:
    df_outliers_inferiores = df_estelionato[df_estelionato['estelionato'] < limite_inferior]
    df_outliers_superiores = df_estelionato[df_estelionato['estelionato'] > limite_superior]

    #print(f'Outliers inferiores {df_outliers_inferiores}')
    #print(f'Outliers superiores {df_outliers_superiores}')


except Exception as e:
    print(f'Erro ao calcular outliers: {e}')


print(f'\nTotal de estelionatos registrados: {df_estelionato_total} casos')

print(f'\nOs meses com casos de estelionato abaixo de: {q1} casos, entram nos meses com menores casos de estelionato, pois 75% dos casos registrados estão acima desse valor.')
print(f'\nMeses com os menores registros de casos de estelionato: \n{df_estelionato_menores.sort_values(by='estelionato', ascending=True)}')

print(f'\nOs meses com casos de estelionato acima de: {q3} casos, entram nos meses com maios casos de estelionato, pois 25% dos casos registrados estão abaixo desse valor.')
print(f'\nMeses com os maiores registros de casos de estelionato: \n{df_estelionato_maiores}')

print(f'\nUtilizando cálculos estatísticos não foi encontrado nenhum padrão nos casos de estelionátos, pois a distância entre a média e a mediana ultrapassa 25%, apresentando uma assimetria forte. ')
print(f'Distancia percentual entre média e mediana: {distancia_percentual:.2f}%')


print(f'\nUtilizando dados matemáticos, cálculamos os limites que funcionam como marca de corte para a nossa distribuição.')
print(f'Encontramos o limite inferior e superior dos casos de estelionato, períodos com casos de estelionáto fora desse intervalo são considerados muito abaixo ou muito acima do comportamento analisado!')
print(f'Limite inferior: {limite_inferior}')
print(f'Limite superior: {limite_superior}')

print('\nPeríodos de Outliers Inferiores')
print(30 * '=')

if len(df_outliers_inferiores) == 0:
    print('\nNão existem casos de estelionato que apresentem quantidade muito abaixo do comportamento dos demais períodos analisados!')
    print((f'Limite inferior: {limite_inferior}'))
else:
    print('\nCasos de estelionato muito abaixo do comportamento dos demais períodos analisados:')
    print(f'Limite inferior: {limite_inferior}')
    print(df_outliers_inferiores)

print('\nPeríodos de Outliers Superiores')
print(30 * '=')

if len(df_outliers_superiores) == 0:
    print('\nNão existem casos de estelionato que apresentem quantidade muito acima do comportamento dos demais períodos analisados!')
    print(f'Limite superior: {limite_superior}\n')
else:
    print('\nCasos de estelionato muito acima do comportamento dos demais períodos analisados:')
    print(f'Limite superior: {limite_superior}\n')
    print(df_outliers_superiores)



try:

    plt.subplots(2, 2, figsize=(18, 10))

    # POSIÇÃO 01 - BOXPLOT
    plt.subplot(2, 2, 1)
    #showfliers=False
    plt.boxplot(array_estelionato, vert=False, showmeans=True)
    plt.title('Boxplot da Distribuição')

    # POSIÇÃO 02 - MEDIDAS
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_estelionato}')
    plt.text(0.1, 0.8, f'Distância: {distancia_percentual}')
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior}')
    plt.text(0.1, 0.6, f'Mínimo: {minimo}')
    plt.text(0.1, 0.5, f'Q1: {q1}')
    plt.text(0.1, 0.4, f'Mediana: {mediana_estelionato}')
    plt.text(0.1, 0.3, f'Q3: {q3}')
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior}')
    plt.text(0.1, 0.1, f'Máximo: {maximo}')
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}')

    plt.axis('off')
    plt.title('Resumo Estatístico')

    #plt.subplot(2, 2, 3)


    plt.show()


except Exception as e:
    print(f'Erro ao visualizar os dados: {e}')
    exit()