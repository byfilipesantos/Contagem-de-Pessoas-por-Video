# Contagem-de-Pessoas-por-Video

## Características gerais
Desenvolvimento de um sistema para detecção da quantidade de pessoas em um determinado ambiente. O programa fará o monitoramento de uma sala através de uma câmera, e informará o usuário, por meio de uma interface, caso o número de pessoas esteja excedendo o máximo permitido no local

## Características específicas
- Será desenvolvido uma página web para disponibilizar as informações ao operador do sistema. A página poderá ser acessada dentro da empresa.
- Utilizaremos uma webcam para fazer a contagem de pessoas, a mesma será conectada ao Raspberry Pi que funcionará como uma central para o funcionamento da solução.
- No Raspberry Pi, será desenvolvido uma aplicação em Python para fazer a leitura dos dados obtidos pela Webcam, será instalada a biblioteca OpenCV que será responsável pela contagem de pessoas.
- Utilizando a Biblioteca OpenCV, será traçado duas linhas virtuais que quando ultrapassadas irão contabilizar a entrada ou saída de pessoas de uma sala, a câmera estará instalada na entrada do local.
