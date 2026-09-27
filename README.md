# tunefinder-back-end

## Descrição do Projeto

Este projeto consiste no desenvolvimento de uma aplicação back-end para recomendações de músicos, à partir dos gostos musicais do usuário.

A aplicação foi desenvolvida como parte do MVP do módulo de **Arquitetura de Software** do curso de **Pós-Graduação em Engenharia de Software da PUC-RIO**,  com o objetivo de aplicar conhecimentos em sistemas compostos e comunicação REST.

## Funcionalidades

- Controle de autenticação
- Busca de artistas em base externa (Last.fm)
- Cadastro de artistas favoritos (inclusão, exclusão e inclusão de anotações)
- Recomendação de artistas

## Integração Externa - Last.fm

Esta aplicação faz integração com a [API da Last.fm](https://www.last.fm/api), para busca e recomendação de novos artistas. Para a utilização da API é necessária a autenticação através de API Key vinculada a uma conta de usuário.

Foram utilizadas as seguintes rotas:

- artist.seach (GET):  busca de artista à partir do nome
- artist.getSimilar (GET): lista de artistas similares ao artista informado

## Estrutura do Projeto

```text
tunefinder-back-end/
│
├── src/
│   ├── main.py                         # ponto de boot da aplicação
│   ├── clients/                        # inicializador do client externo
│   ├── db/                             # engine, Session e inicializador do banco de dados
│   ├── lastfm/                         # classe de interação com a API da Last.fm
│   ├── models/                         # classes dos modelos utilizados
│   │   ├── favorite_artist.py
│   │   └── user.py
│   ├── repositories/                   # classes de interação com o repositório de dados
│   ├── routes/                         # endpoints da API
│   ├── schemas/                        # schemas de interação com os endpoints
│   └── services/                       # camada de aplicação das regras negociais da aplicação
│
└── database/                           # arquivo sqlite (ignorado pelo git)
```


## Tecnologias Utilizadas

- Python (recomendado: 3.9+)
- Flask (API)
- flask-openapi3 (documentação OpenAPI/Swagger)
- flask-cors (CORS)
- flask-login (gestão de autenticação)
- SQLAlchemy (ORM)
- SQLite (banco local)
- Pydantic (validação / schemas)
- pip (gerenciador de pacotes)

Dependências do projeto estão listadas em [requirements.txt](requirements.txt).


## Requisitos

- Python 3.9 ou superior (instale via python.org / pyenv)
- pip
- criação de arquivo .env com as variáveis de ambiente necessárias
- permissão de escrita para criar o diretório `database/` (o arquivo SQLite é criado neste diretório por [`src/db/session.py`](src/db/session.py))
- uso de ambiente virtual: venv ou virtualenv (recomendado caso não seja utilizado o Docker)


## Variáveis de Ambiente

Para correto funcionamento da aplicação, é necessário o cadastro das seguintes variáveis de ambiente:

- `SECRET_KEY` - chave privada para autenticação dos usuários na aplicação
- `LASTFM_API_KEY` - API Key para autenticação com a API da Last.fm a ser gerada
- `LASTFM_API_URL` - URL padrão da API da Last.fm

## Inicialização através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t tunefinder-back .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, o seguinte comando:

```
$ docker run -p 5000:5000 tunefinder-back
```

Uma vez executando, para acessar a documentação Swagger da API, basta abrir o [http://localhost:5000](http://localhost:5000) no navegador.

## Contexto Acadêmico

Projeto desenvolvido para fins acadêmicos no curso de Pós-Graduação em Engenharia de Software da PUC-RIO.