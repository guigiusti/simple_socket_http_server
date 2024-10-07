# Simple Socket HTTP Server

Um servidor simples de HTTP implemetado em Python utilizando Socket.

## Descrição

Este é um servidor HTTP 1.1 escrito em Python, com o objetivo de aprofundar meus conhecimentos na linguagem e no protocolo HTTP. Utiliza o módulo Socket para receber e responder aos _requests_ do navegador e os cabeçalhos são construídos utilizando os módulos HTTP e Mimetypes.

Os metodos implementados são GET e POST. Sendo o metódo POST apenas implementado de forma específica para demonstrar o potencial da aplicação. Os outros metodos não se encontram implementados retornando um cabeçalho com status _405 Method Not Allowed_.

## Demonstração

O servidor está preparado para ser utilizado com arquivos de HTML, CSS, Javascript, Imagens, Áudios, Vídeos, PDFs, entre outros. A página index.html disponibilizada neste repositório, retorna o seguinte exemplo:

![Exemplo 1]('static/example_1.png')
![Exemplo 2]('static/example_2.png')

## Rodando a aplicação

Utilizando o terminal, clone o repositório:

```bash
git clone https://github.com/guigiusti/simple_socket_http_server.git
```

Navegue para o diretório do projeto e execute-o

```bash
cd simple_socket_http_server && python3 servidor.py
```

Por padrão o programa irá rodar no seguinte endereço:

```bash
http://localhost:8080/
```

Porém no cabeçalho do arquivo de Python, podem ser editas as constantes de Host e Porta qual o servidor utiliza para funcionar. Fazendo essa alteração o novo endereço será exibido no próprio terminal.

## Configurando o Servidor

Algumas opções deste servidor podem ser editadas diretamente no arquivo Python. Como Host, Porta, Mensagem do Servidor, o caminho dos erros de status 404 e 500, mas principalmente os caminhos de arquivos que podem ser acessados pelo cliente.

### Configurando Host e Porta

Para alterar o caminho qual o servidor escutará por requisições, basta alterar as constantes HOST e PORT. Lembrando que valores abaixo de 1000 requerem acesso de administrador (como as portas de HTTP e HTTPS padrões).

### Configurando os Caminhos

Para alterar os diferentes caminhos que podem receber requisição e seus respectivos arquivos, modifique o dicionário localizado na constante ALLOWED_PATHS, adicionando como a Chave o caminho HTTP, e como seu valor o caminho dentro do sistema de arquivo do computador.

Também é possível aqui editar a constante PATH_NOT_FOUND, referente ao caminho do arquivo de HTML do erro de status 404. Da mesma forma com a constante INTERNAL_SERVER_ERROR, referente ao erro de status 500.

## Limitações

- O servidor não verifica e filtra requests possivelmente maliciosos.
- Não faz implementação dos metodos DELETE, PUT e PATCH
- Faz uma implementação simples do metodos POST, apenas para demonstrar uma possível expansão da aplicação para APIs.
- Pode facilmente ser transformado em um servidor dinâmico, mas funciona primariamente como um servidor de arquivos estáticos.
