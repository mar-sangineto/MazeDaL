# Maze

## Parse
Primeiro foi criado o parse para fazer o tratamento do `config.txt`, arquivo que define as configurações do labirinto.

No programa já existe um config básico, as `keys`: `SEED`, `ALGORITHM` e `DISPLAY_MODE` são opcionais e possuem um valor pré-definido caso não esteja no arquivo de configuração, além dissi caso o valo da `KEY` não possa ser possível, ele ignora e usa o valor pré-definido.

```
WIDHT=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=1
ALGORITHM=BFS
DISPLAY_MODE=ASCII
```

## Maze structure
Foi criado um `maze_structure.py` o qual monta a estrutura básica do Maze, com sua célula e a estrutura necessária para gerar um Maze como:
- Pegar uma célula
- Achar os vizinhos
- Verificar se célula está na borda
- Remover parede entrre duas células

Inicialmente o Maze é gerado todo preenhcido e no Maze Generator que é gerado com os critérios necessários.

## Maze generator
Gera um Maze aleatoriamente (podendo setar uma `seed`), com base na `class Maze`. É utilizado o algortimo *DFS* (busca em profundida), onde o labirinto é contruido descendo as colunas e volta (*backtraking*) quando não é possível continuar.

Atendendo aos critérios também é gerado a célula de entrada e saída (seguindo o arquivo de configuração passado).

> Falta: adicionar no maze_generator caminhos quando `PERFECT=False` (ou seja, com loops).

## Maze Ing
Arquivo principal do programa. Foi implementado o salvamento do Maze no `OUTPUT_FILE` com as respectivas entradas (`ENTRY`) e saídas (`EXIT`), conforme especificações requeridas. 

> Falta: Adicionar a solução no `OUTPUT_FILE`

## Solution
> Falta: Fazer o arquivo `solve.py`, o qual conterá o algoritmo para solução do labirinto.

## Render
> Falta: Fazer o `render.py`, o qual conterá o programa que mostrará em ASCII (e possívelmente em MLX) o labirinto. Este também mostrará o caminho.
