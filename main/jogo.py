import cv2

#Variaveis
jogador1_score = 0
jogador2_score = 0
contador = 0

#Textos
def titulo():
    (cv2.putText(video_final, "Pedra, papel e tesoura", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA))

def jogador1_turn(jogada_esquerda):
    (cv2.putText(video_final, ("Jogador1: " + str(jogada_esquerda)), (25, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA))

def jogador2_turn(jogada_direita):
    (cv2.putText(video_final, ("Jogador2: " + str(jogada_direita)), (425, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1, cv2.LINE_AA))

def jogador1_placar(pontos_esquerda):
    (cv2.putText(video_final, "Jogador1: " + str(pontos_esquerda), (25, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA))

def jogador2_placar(pontos_direita):
    (cv2.putText(video_final, "Jogador2: " + str(pontos_direita), (425, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA))

def winner(vitoria):
    (cv2.putText(video_final, str(vitoria), (250, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA))



def gray_and_blur(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    k_size = (35, 35)
    filtro_blur = cv2.GaussianBlur(img_gray, k_size, 0)

    _, thresh = cv2.threshold(filtro_blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return thresh

#Identifica Jogadas
def area(contours):
    area_total = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > area_total:
            area_total = area

    return area_total
def contornos(thresh):
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours
def jogadas(area):
    if area > 14500 and area < 17000:
        jogada = "Papel"
        return jogada
    elif area > 11500 and area < 14000:
        jogada = "Pedra"
        return jogada
    elif area < 11500 and area > 6000:
        jogada = "Tesoura"
        return jogada

#Resultados
def vencedor(jogada_esquerda, jogada_direita):

    if jogada_esquerda == jogada_direita:
        resultado = "Empate"
        return resultado

    elif (jogada_esquerda == "Tesoura" and jogada_direita == "Papel"):
        resultado = "Jogador1 Venceu!"
        return resultado
    elif (jogada_esquerda == "Papel" and jogada_direita == "Tesoura"):
        resultado = "Jogador2 Venceu!"
        return resultado
    elif (jogada_esquerda == "Pedra" and jogada_direita == "Tesoura"):
        resultado = "Jogador1 Venceu!"
        return resultado
    elif (jogada_esquerda == "Tesoura" and jogada_direita == "Pedra"):
        resultado = "Jogador2 Venceu!"
        return resultado
    elif (jogada_esquerda == "Papel" and jogada_direita == "Pedra"):
        resultado = "Jogador1 Venceu!"
        return resultado
    elif (jogada_esquerda == "Pedra" and jogada_direita == "Papel"):
        resultado = "Jogador2 Venceu!"
        return resultado


def placarEsquerda(vitorioso, pontuacao_mao_esquerda):
    if vitorioso == "Jogador1 Venceu!":
        pontuacao_mao_esquerda = pontuacao_mao_esquerda + 1
    return pontuacao_mao_esquerda

def placarDireita(vitorioso, pontuacao_mao_direita):
    if vitorioso == "Jogador2 Venceu!":
        pontuacao_mao_direita = pontuacao_mao_direita + 1
    return pontuacao_mao_direita

def vencedorGeral(resultado_esquerda, resultado_direita):
    if resultado_esquerda > resultado_direita:
        return "Mão Esquerda ganhou mais que a direita!"
    elif resultado_direita > resultado_esquerda:
        return "Mão Direita ganhou mais que a esquerda!"
    else:
        return "As duas mãos ganharam a mesma quantidade de vezes!"

video = cv2.VideoCapture('pedra-papel-tesoura.mp4')



parar = 0

while parar <= 900:

    ret, rec = video.read()

    video_final = cv2.resize(rec, (800, 600))

    crop_video_esquerda = video_final[100:600, 100:450]

    crop_video_direita = video_final[100:600, 350:800]

    imagem_gray1 = gray_and_blur(crop_video_esquerda)
    imagem_gray2 = gray_and_blur(crop_video_direita)

    contorno_mao_esquerda = contornos(imagem_gray1)
    contorno_mao_direita = contornos(imagem_gray2)

    area_mao_esquerda = area(contorno_mao_esquerda)
    area_mao_direita = area(contorno_mao_direita)

    jogada_mao_esquerda = jogadas(area_mao_esquerda)
    jogada_mao_direita = jogadas(area_mao_direita)

    ganhador = vencedor(jogada_mao_esquerda, jogada_mao_direita)

    contador += 1
    if contador >= 90:
        contador = 0
        jogador1_score = placarEsquerda(ganhador, jogador1_score)
        jogador2_score = placarDireita(ganhador, jogador2_score)

    resultado_final = vencedorGeral(jogador1_score, jogador2_score)

    titulo()
    jogador1_turn(jogada_mao_esquerda)
    jogador2_turn(jogada_mao_direita)
    jogador1_placar(jogador1_score)
    jogador2_placar(jogador2_score)
    winner(ganhador)

    cv2.imshow("Video final", video_final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(resultado_final)
        break

    if not ret:
        break

    parar += 1

video.release()
cv2.destroyAllWindows()