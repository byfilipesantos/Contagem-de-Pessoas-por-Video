#!/bin/bash
  
echo "content-type: text/html"
echo
echo
echo "<html> <head> <meta charset='utf-8' /> <title> CROSSLINE </title> <meta http-equiv="refresh" content="2" > </head> <body>"

echo "<center>"

echo "<font size="5" face="Verdana">"
echo "<h1>SISTEMAS MICROPROCESSADOS AVANÇADOS</h1>"
echo "<h1>Contagem de Pessoas por Vídeo:</h1>"
echo "<br>"
echo "</font>"
echo "<font size="6" face="Verdana">"
echo "<h2>Entrou: $(tail -f | tail -1 /home/pi/Projeto/dados.txt | cut -f1 -d';')</h2>"
echo "<h2>Saiu: $(tail -f | tail -1 /home/pi/Projeto/dados.txt | cut -f2 -d';')</h2>"
echo "<br>"
echo "</font>"
echo "<p align="center"> <img src="http://192.168.1.103/univates.jpg" width="300" /> </center>" 
echo "
  </body>
  </html>
  "