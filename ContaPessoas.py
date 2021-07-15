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
areaContornoMin = 3000
limiarBinarizacao = 70
posicaoLinhas = 150

# Backup do arquivo dados anterior
os.system("cp dados.txt dados-backup.txt")
# Cria um novo arquivo de dados
os.system("> dados.txt")

arquivo = open("dados.txt", "a")
arquivo.write(str(contaEntrada) + ";" + str(contaSaida) + ";\n")
arquivo.close()

# Verifica se o corpo detectado esta entrando da area monitorada
def testaIntersecaoEntrada(y, linhaEntrada, linhaSaida):
    diferencaAbsoluta = abs(y - linhaEntrada)
    if ((diferencaAbsoluta <= 2) and (y < linhaSaida)):
        return 1
    else:
        return 0

# Verifica se o corpo detectado esta saindo da area monitorada
def testaInterseccaoSaida(y, linhaEntrada, linhaSaida):
    diferencaAbsoluta = abs(y - linhaSaida)
    if ((diferencaAbsoluta <= 2) and (y > linhaEntrada)):
        return 1
    else:
        return 0

# Abre fluxo video WebCam
cam = cv2.VideoCapture(0)

# Abre fluxo video Camera Intelbras utilizando protocolo RTSP
#cam = cv2.VideoCapture('rtsp://admin:VH4AX674@192.168.0.104:554/cam/realmonitor?channel=1&subtype=0')

# Forca resolucao de 1024x768 na camera
cam.set(3,1024)
cam.set(4,768)
primeiroFrame = None

# Realiza algumas leituras antes de iniciar a analise a fim da camera se acostumar com a luminosidade do local
for i in range(0,20):
    (grabbed, Frame) = cam.read()

while True:
    # Le o primeiro frame e determina resolucao da imagem
    (grabbed, Frame) = cam.read()
    altura = np.size(Frame,0)
    largura = np.size(Frame,1)

    # Se nao foi possivel obter frame, nada mais deve ser feito
    if not grabbed:
        break

    # Converte frame para escala de cinza
    frameGray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
    
    # Realca os contornos do frame
    frameGray = cv2.GaussianBlur(frameGray, (21, 21), 0)

    # Como a comparacao eh feita entre duas imagens subsequentes, inicializa o primeiro frame se ele for nulo
    if primeiroFrame is None:
        primeiroFrame = frameGray
        continue
    FrameDelta = cv2.absdiff(primeiroFrame, frameGray) # Calcula a diferenca entre dois frames
    FrameThresh = cv2.threshold(FrameDelta, limiarBinarizacao, 255, cv2.THRESH_BINARY)[1] # Filtro Limiar do OpenCV
    FrameThresh = cv2.dilate(FrameThresh, None, iterations=2) # Dilata a imagem
    _, cnts, _ = cv2.findContours(FrameThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Procura contornos na imagem

    # Desenha linhas de entrada e saida
    linhaEntrada = (altura / 2)-posicaoLinhas
    linhaSaida = (altura / 2)+posicaoLinhas
    cv2.line(Frame, (0,linhaEntrada), (largura,linhaEntrada), (255, 0, 0), 2)
    cv2.line(Frame, (0,linhaSaida), (largura,linhaSaida), (0, 0, 255), 2)

    # Percorre todos os contornos encontrados
    for c in cnts:
        if cv2.contourArea(c) < areaContornoMin:  # Ignora os contornos de areas muito pequenas
            continue

        # Obtem coordenadas do contorno e realca o contorno com um retangulo
        (x, y, w, h) = cv2.boundingRect(c) # x e y: coordenadas do vertice superior esquerdo w e h: respectivamente largura e altura do retangulo
        cv2.rectangle(Frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Desenha um circulo para indicar o ponto central do contorno
        coordenadaXCentroContorno = (x+x+w)/2
        coordenadaYCentroContorno = (y+y+h)/2
        pontoCentralContorno = (coordenadaXCentroContorno,coordenadaYCentroContorno)
        cv2.circle(Frame, pontoCentralContorno, 1, (0, 0, 0), 5)
        
    # Verifica a intersecao dos centros dos contornos com as linhas de entrada e saida e contabiliza quantas pessoas entraram no local
	if (testaIntersecaoEntrada(coordenadaYCentroContorno,linhaEntrada,linhaSaida)):
            contaEntrada += 1
            arquivo = open("dados.txt", "a")
            arquivo.write(str(contaEntrada) + ";" + str(contaSaida) + ";\n")
            arquivo.close()

    # Verifica a intersecao dos centros dos contornos com as linhas de entrada e saida e contabiliza quantas pessoas sairam no local
	if (testaInterseccaoSaida(coordenadaYCentroContorno,linhaEntrada,linhaSaida)):  
            contaSaida += 1
            arquivo = open("dados.txt", "a")
            arquivo.write(str(contaEntrada) + ";" + str(contaSaida) + ";\n")
            arquivo.close()
    
    # Escreve na imagem o numero de pessoas que entraram ou sairam. Se deixar comentada as proximas 6 linhas, o programa podera ser executado via ssh tambem
    cv2.putText(Frame, "Entradas: {}".format(str(contaEntrada)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(Frame, "Saidas: {}".format(str(contaSaida)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Trabalho de Sistemas Microprocessados Avancados", Frame)
    cv2.waitKey(1);

cam.release()    # Limpa a imagem da camera obtida pelo OpenCV
cv2.destroyAllWindows() # Fecha todas janelas abertas
