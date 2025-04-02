# 📰 Web Scraping - New York Times

Este projeto realiza **web scraping** no site do **New York Times**, coletando posts relacionados aos **Estados Unidos** e salvando os dados em um arquivo **CSV**.

**URL de Scraping**:  
O scraping é realizado na página [https://www.nytimes.com/international/section/us](https://www.nytimes.com/international/section/us).

## 📌 Funcionalidades

- 🚀 Extrai posts do New York Times relacionados aos EUA.
- 📄 Salva os posts coletados em um **arquivo CSV** com colunas separadas por vírgula.
- ⚙️ Permite configuração dinâmica via **parâmetros CLI**.
- 🐳 Suporte a execução via **Docker e Docker Compose**.

## 📥 Parâmetros

| Parâmetro        | Tipo   | Descrição                                                                             |
| ---------------- | ------ | ------------------------------------------------------------------------------------- |
| `--initial-page` | `int`  | Define a página inicial da busca. _Default: 1_                                        |
| `--last-page`    | `int`  | Define a página final da busca.                                                       |
| `--all-pages`    | `bool` | Se ativado, busca todas as páginas a partir da página inicial, ignorando `last-page`. |

### 🔄 Retorno

O script retorna um **booleano**, indicando se o arquivo CSV foi criado com sucesso.
A execução do container retorna uma mensagem de sucesso ou falha.

## 🛠️ Como Executar

### 1️⃣ **Executando com Docker Compose**

#### 🔹 Padrão

```sh
docker compose run --rm scraping
```

#### 🔹 Com parâmetros personalizados (opcionais)

```sh
docker compose run --rm scraping --initial-page=1 --last-page=2 --all-pages
```

---

### 2️⃣ **Executando com Docker**

#### 🔹 Construindo a imagem

```sh
docker build -t scraping .
```

#### 🔹 Rodando o container

```sh
docker run --rm -v .:/app scraping python3 -m script.scraping
```

#### 🔹 Rodando com parâmetros personalizados (opcionais)

```sh
docker run --rm -v .:/app scraping python3 -m script.scraping --initial-page=1 --last-page=2 --all-pages
```

---

## 🧪 Testes

Você pode rodar os testes do projeto usando **pytest**. Para isso, utilize os seguintes comandos:

### 1️⃣ **Com Docker Compose**

```sh
docker compose run --rm tests
```

### 2️⃣ **Com Docker**

```sh
docker run --rm scraping pytest -v tests/
```

---

## 📂 Saída do Script

Após a execução, o arquivo **posts.csv** será salvo dentro do diretório **/app** do container.  
Se estiver usando **Docker com volumes**, ele será salvo na pasta correspondente no seu sistema local.

📍 **Exemplo de saída esperada**:

```csv
title,content,owner,date
Titulo do post 1,Conteudo do post 1,Criador do post 1,Data do post 1
Titulo do post 2,Conteudo do post 2,Criador do post 2,Data do post 2
```
