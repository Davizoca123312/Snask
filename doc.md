
📘 Documentação da Linguagem Snask
🛠️ Variáveis e Constantes

Comando	Descrição	Exemplo
make	Cria uma variável	make x = 10
set	Altera o valor de uma variável	set x = 20
zap	Remove uma variável	zap x
keep	Declara uma constante (imutável na prática futura)	keep PI = 3.14
🖨️ Entrada e Saída

Comando	Descrição	Exemplo
shoo	Exibe um valor no terminal	shoo "Olá"
grab	Recebe uma string do usuário	grab nome
grabnum	Recebe um número do usuário	grabnum idade
grabtxt	Recebe texto do usuário	grabtxt msg
🔁 Controle de Fluxo

Comando	Descrição	Exemplo
when	Executa bloco se condição for verdadeira	when idade > 18: shoo "maior"
spin	Enquanto condição for verdadeira	spin x < 5: shoo x set x = x + 1
loopy	Loop infinito	loopy: shoo "ok"
breaky	Encerra loop	breaky
skipit	Pula iteração (não implementado totalmente)	skipit
🧮 Expressões e Operadores

Operador	Significado
+	Soma ou concatenação
-	Subtração
*	Multiplicação
/	Divisão
is	Igualdade
aint	Diferença
==	Comparação (redundante com is)
🔣 Conversão de Tipos

Comando	Descrição	Exemplo
convert	Converte entre int e str	convert idade to str
🧰 Funções

Comando	Descrição	Exemplo
craft	Declara função	craft ola: shoo "oi"
back	Retorna valor de uma função	back x
nome_funcao	Chama uma função	ola
📦 Listas (Packs)

Comando	Descrição	Exemplo
pack	Cria uma lista	pack numeros = [1, 2, 3]
packadd	Adiciona item à lista	packadd numeros 4
packget	Acessa item da lista	make x = packget numeros 0
📦 Dicionários (Boxes)

Comando	Descrição	Exemplo
box	Cria dicionário	box pessoa = {nome: "Joao", idade: 30}
boxput	Adiciona/modifica valor	boxput pessoa idade 31
boxget	Acessa valor do dicionário	make x = boxget pessoa nome
🕒 Espera

Comando	Descrição	Exemplo
snooze	Espera segundos	snooze 2
📚 Bibliotecas

Comando	Descrição	Exemplo
to use nome	Importa biblioteca .snask	to use mathplus
🔁 Interno
Estes comandos são internos do interpretador e facilitam execução:

_resolve → resolve variáveis

_execute → executa blocos

✅ Exemplo de Código Snask
snask
Copiar
Editar
to use mathplus

make a = 2
make b = 4

shoo "A potência é:"
power

shoo "O maior é:"
make maior = maxvalue
shoo maior
