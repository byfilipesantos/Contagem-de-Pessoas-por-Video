import os
import datetime
import math
import cv2
import numpy as np

# Variaveis globais
largura = 0
altura = 0
contaEntrada = 0
contaSaida = 0
AreaContornoLimiteMin = 3000  # Este valor pode ser alterado
ThresholdBinarizacao = 70  # Este valor pode ser alterado
OffsetLinhasRef = 150  # Este valor pode ser alterado

# Backup do arquivo dados anterior
os.system("cp dados.txt dados-backup.txt")
# Cria um novo arquivo de dados
os.system("> dados.txt")

# Verifica se o corpo detectado esta entrando da area monitorada
def testaIntersecaoEntrada(y, coordenadaYLinhaEntrada, coordenadaYLinhaSaida):
    diferencaAbsoluta = abs(y - coordenadaYLinhaEntrada)
    if ((diferencaAbsoluta <= 2) and (y < coordenadaYLinhaSaida)):
        return 1
    else:
        return 0

# Verifica se o corpo detectado esta saindo da area monitorada
def testaInterseccaoSaida(y, coordenadaYLinhaEntrada, coordenadaYLinhaSaida):
    diferencaAbsoluta = abs(y - coordenadaYLinhaSaida)
    if ((diferencaAbsoluta <= 2) and (y > coordenadaYLinhaEntrada)):
        return 1
    else:
        return 0

camera = cv2.VideoCapture(0)

# Forca resolucao de 1024x768 na camera
camera.set(3,1024)
camera.set(4,768)

primeiroFrame = None

# Realiza algumas leituras antes de iniciar a analise a fim da camera se acostumar com a luminosidade do local
for i in range(0,20):
    (grabbed, Frame) = camera.read()

while True:
    # Le o primeiro frame e determina resolucao da imagem
    (grabbed, Frame) = camera.read()
    altura = np.size(Frame,0)
    largura = np.size(Frame,1)

    # Se nao foi possivel obter frame, nada mais deve ser feito
    if not grabbed:
        break

    # Converte frame para escala de cinza e realca os contornos
    frameGray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
    frameGray = cv2.GaussianBlur(frameGray, (21, 21), 0)

    # Como a comparacao eh feita entre duas imagens subsequentes, inicializa o primeiro frame se ele for nulo
    if primeiroFrame is None:
        primeiroFrame = frameGray
        continue
    
    FrameDelta = cv2.absdiff(primeiroFrame, frameGray)
    FrameThresh = cv2.threshold(FrameDelta, ThresholdBinarizacao, 255, cv2.THRESH_BINARY)[1]
    FrameThresh = cv2.dilate(FrameThresh, None, iterations=2)
    _, cnts, _ = cv2.findContours(FrameThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contaContornos = 0

    # Desenha linhas de referencia 
    coordenadaYLinhaEntrada = (altura / 2)-OffsetLinhasRef
    coordenadaYLinhaSaida = (altura / 2)+OffsetLinhasRef
    cv2.line(Frame, (0,coordenadaYLinhaEntrada), (largura,coordenadaYLinhaEntrada), (255, 0, 0), 2)
    cv2.line(Frame, (0,coordenadaYLinhaSaida), (largura,coordenadaYLinhaSaida), (0, 0, 255), 2)


    # Percorre todos os contornos encontrados
    for c in cnts:
        # Ignora os contornos de areas muito pequenas
        if cv2.contourArea(c) < AreaContornoLimiteMin:
            continue

        # Contabiliza os contornos encontrados para fins de depuracao
        contaContornos = contaContornos+1    

        # Obtem coordenadas do contorno e realca o contorno com um retangulo
        (x, y, w, h) = cv2.boundingRect(c) #x e y: coordenadas do vertice superior esquerdo
                                           #w e h: respectivamente largura e altura do retangulo

        cv2.rectangle(Frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Desenha um circulo para indicar o ponto central do contorno
        coordenadaXCentroContorno = (x+x+w)/2
        coordenadaYCentroContorno = (y+y+h)/2
        pontoCentralContorno = (coordenadaXCentroContorno,coordenadaYCentroContorno)
        cv2.circle(Frame, pontoCentralContorno, 1, (0, 0, 0), 5)
        
    # Verifica a intersecao dos centros dos contornos com as linhas de entrada e saida e contabiliza quantas pessoas entraram no local
	if (testaIntersecaoEntrada(coordenadaYCentroContorno,coordenadaYLinhaEntrada,coordenadaYLinhaSaida)):
            contaEntrada += 1
            arquivo = open("dados.txt", "a")
            arquivo.write(str(contaEntrada) + ";" + str(contaSaida) + ";\n")
            arquivo.close()

    # Verifica a intersecao dos centros dos contornos com as linhas de entrada e saida e contabiliza quantas pessoas sairam no local
	if (testaInterseccaoSaida(coordenadaYCentroContorno,coordenadaYLinhaEntrada,coordenadaYLinhaSaida)):  
            contaSaida += 1
            arquivo = open("dados.txt", "a")
            arquivo.write(str(contaEntrada) + ";" + str(contaSaida) + ";\n")
            arquivo.close()
    
    # Imprime em tela as informacoes de entrada e saida
    #print "Contornos: "+str(contaContornos)+" Entradas: "+str(contaEntrada)+" Saidas: "+str(contaSaida)
    
    # Escreve na imagem o numero de pessoas que entraram ou sairam. Se deixar comentada as proximas 6 linhas, o programa podera ser executado via ssh tambem
    cv2.putText(Frame, "Entradas: {}".format(str(contaEntrada)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(Frame, "Saidas: {}".format(str(contaSaida)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Trabalho de Sistemas Microprocessados Avancados", Frame)
    cv2.waitKey(1);

# Limpa a camera e fecha as janelas abertas
camera.release()
cv2.destroyAllWindows()
