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

## O que foi feito
     Primeiramente instalamos o Sistema Operacional Raspbian (versão 10 Buster), após instalado, atualizamos o sistema, liberamos acesso remoto via VNC e SSH e na sequência fizemos liberações de firewall para permitir o acesso remoto, bem como o tráfego de dados na porta 80.
O próximo passo foi fazer a instalação do Python 3 e OpenCV, juntamente com algumas dependências obrigatórias para seu funcionamento. A instalação demorou pouco mais de 5 horas para ser finalizada, visto que o OpenCV para melhor funcionamento recomenda-se ser compilado e esta é a etapa mais demorada do processo.
A próxima etapa foi a instalação do Apache e configuração para funcionamento da nossa página onde é exibida os nossos dados de entrada e saída. Uma configuração adicional que foi feita no apache foi a habilitação para funcionamento do CGI (common gateway interface) que é um elemento que proporciona uma ligação entre a nossa página html e o sistema operacional. Dentro do CGI utilizamos alguns comandos linux para coleta dos dados salvos.


![IMG-01](https://user-images.githubusercontent.com/42256808/125874144-d4dfaf25-433e-4029-93b2-e6419d0f14d8.png)

Figura 1 - Tecnologia utilizada para exibir os dados


## Como foi feito
A contagem de objetos é baseada nas seguintes características:
- São detectados apenas objetos em movimento;
- É avaliado a direção do movimento do objeto;
- Somente é contabilizado objetos que cruzarem as linhas de entrada ou saída;
- Desta maneira é possível definir quantos objetos entraram ou saíram da área monitorada.


![IMG-02](https://user-images.githubusercontent.com/42256808/125874540-2bd62e74-1ce7-490b-b47e-59cf7d98604a.png)
Figura 2 - Definições da área monitorada


A contagem de objetos em movimento é feita da seguinte forma:
Quando um objeto cruza a linha azul (entrada), vindo da direção da linha vermelha (saída), é contabilizada uma entrada na área monitorada.
Quando um objeto cruza a linha vermelha (saída), vindo da direção da linha azul (entrada), é contabilizada uma saída da área monitorada.

Os frames obtidos através da captura de vídeo são tratados por meio da biblioteca openCV, onde é convertida a imagem para uma escala de cinza, facilitando a qualquer operação matemática pixel a pixel. Após é realçado os objetos em movimento e binarizada a imagem, reduzindo drasticamente o processamento de hardware. O próximo passo é a dilatação da imagem que deixará os objetos em uma massa de pixels de uma única cor. Um dos últimos passos é a procura de contornos e seu centro. O centro do contorno é o fator que irá contabilizar as entradas e saídas da área monitorada, uma vez que o mesmo ultrapassar as linhas de referência.
Para o desenvolvimento do trabalho, criamos um diretório com o nome “Projeto” dentro de /home/pi. Dentro do diretório “/home/pi/Projeto/” encontrasse o código principal do projeto com nome de “ContaPessoas.py” e dois arquivos de dados, o “dados.txt” que contém todos os registros de entrada/saída e o arquivo “dados-backup.txt” que é o arquivo de dados referente a última execução do programa.

![IMG-03](https://user-images.githubusercontent.com/42256808/125874541-09186b65-f521-4cfc-b18d-6f34786ab76b.PNG)

Figura 3 - Arquivos do projeto


Para executar o programa, entramos no diretório “/home/pi/Projeto/” e utilizamos o comando “python ContaPessoas.py”. Uma das primeiras coisas que o programa irá fazer será mover o arquivo “dados.txt” para “dados-backup.txt” a fim de preservar a informação da última execução do programa. O programa irá abrir uma janela exibindo a imagem da câmera, as linhas de entrada e saída e os valores retornados da quantidade de objetos em movimento que entraram e saíram da área monitorada.

![crossline_system](https://user-images.githubusercontent.com/42256808/125875040-0bb49e16-ae53-4a43-97e3-84e6c5b064ae.jpg)
Figura 4 - Imagem de como ficou instalada a câmera

Os dados de entrada e saída, salvos com nome “dados.txt”, é formado por números inteiros e ponto e vírgula, organizados da seguinte forma: número de pessoas que entrou, ponto e vírgula, número de pessoas que saiu, ponto e vírgula e uma quebra de linha. A cada pessoa que entra ou sai, o programa grava os dados neste arquivo, sempre em uma nova linha. 

![IMG-04](https://user-images.githubusercontent.com/42256808/125874542-1a200789-b85d-449a-86c0-f057e58f1ff4.PNG)

Figura 5 - Arquivo “dados.txt”


Para realizar a leitura dos dados obtidos pela câmera, criamos uma página html com nome de “index.html” dentro do diretório “/var/www/html/”. Esta página é extremamente simples pois ela apenas faz uma chamada para nosso arquivo CGI que é responsável por mostrar o resultado obtido nas leituras e saídas do local. 
Dentro do diretório “/usr/lib/cgi-bin/” criamos o nosso “index.cgi” que é chamado pela página html citada anteriormente. Apesar do CGI ser de certa forma ultrapassado, optamos pela utilização do mesmo devido a facilidade de execução de códigos shell. Na imagem abaixo fica bem claro a estrutura do código CGI, que basicamente é formado por códigos html além de duas execuções paralelas do comando “tail”, uma para leitura da entrada e uma para leitura da saída.


![IMG-06](https://user-images.githubusercontent.com/42256808/125874537-56dc9a13-5f11-4e19-95ca-89fd4061d59e.PNG)

Figura 6 - Arquivo “index.cgi”


Por fim, chegamos a nossa tela que pode ser acessada por qualquer dispositivo que tenha acesso a rede local onde encontrasse o Raspberry instalado. Para disponibilizar o acesso a esta página, além do “index.html” e o “index.cgi”, foi necessário fazer algumas configurações básicas no apache.


![IMG-05](https://user-images.githubusercontent.com/42256808/125874543-ec74132a-2a40-4856-a69d-9ea27d94df0c.PNG)

Figura 7 - Tela de monitoramento


## Referências
https://www.raspberrypi.org/
https://opencv.org/
https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/





