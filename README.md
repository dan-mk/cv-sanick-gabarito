# Gabarito do desafio de visão computacional Sanick

Repositório criado a fim de construir coletivamente o gabarito de cápsulas e grãos defeituosos para o desafio de visão computacional da Sanick Equipamentos de Precisão (https://github.com/Sanick-Equipamentos/desafioVisao). O objetivo deste repositório é auxiliar todos a identificarem quais objetos devem ser apontados por seus algoritmos. Sinta-se livre para modificar os códigos disponíveis aqui da forma que lhe for útil.

## Utilização

Inicie o programa escolhendo o vídeo em que deseja trabalhar.

```sh
python3 main.py (soja|capsula-marrom|capsula-rosa)-(treinamento|teste)
```

Considerando que as cápsulas e grãos não alteram muito a sua aparência enquanto atravessam o quadro do vídeo, apenas 1 a cada 6 frames foram salvos. Essa frequência garante que cada objeto apareça **inteiramente** em pelo menos 2 e em no máximo 4 frames salvos.

O programa exibirá sempre 4 frames salvos consecutivos ao usuário. As teclas Z e X podem ser utilizadas para respectivamente voltar e avançar a sequência de frames. Para adicionar um objeto defeituoso, primeiramente enquadre todas as ocorrências do objeto nos 4 frames exibidos pelo programa. Depois pressione A, clique no centro do objeto defeituoso em todos os frames em que ele aparece, e pressione S para salvar ou C para cancelar. Os dados dessa anotação serão salvos em um arquivo independente na pasta *labels* dentro da pasta do vídeo correspondente.