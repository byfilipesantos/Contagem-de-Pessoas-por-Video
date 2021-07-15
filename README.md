# Contagem-de-Pessoas-por-Video

## Características gerais
Desenvolvimento de um sistema para detecção da quantidade de objetos em movimento em um determinado ambiente, com contagens independentes para objetos que entram e saem da área monitorada. O programa fará o monitoramento de uma sala através de uma câmera, e exibirá os dados por meio de uma página web.

## Características específicas
- Desenvolvimento de uma página web para disponibilizar as informações ao operador do sistema. A página poderá ser acessada dentro da rede local.
- Utilizaremos uma câmera/webcam para fazer a contagem de pessoas, a mesma será conectada ao Raspberry Pi que funcionará como uma central para o funcionamento da solução.
- No Raspberry Pi, foi desenvolvido uma aplicação em Python para fazer a leitura dos dados obtidos pela Webcam, foi instalada a biblioteca OpenCV que é responsável pela contagem de pessoas.
- Utilizando a Biblioteca OpenCV, será traçado duas linhas virtuais que quando ultrapassadas irão contabilizar a entrada ou saída de pessoas de uma sala, a câmera estará instalada na entrada do local.

## Material utilizado
Para realização deste projeto, foi utilizado os seguintes materiais:
- Raspbery Pi 3B com cartão Micro SD de 16 GB e fonte de alimentação;
- WebCam Multilaser;
- Câmera de Segurança Intelbras Mibo iM4.
