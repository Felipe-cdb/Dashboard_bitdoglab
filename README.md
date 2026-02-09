# Dashboard_bitdoglab
Dashboard criado com servidor flask que recebe dados da bitdoglab para analisar a quantidade de visitas e compras  de um estabelecimento

## 📦 Preparação do Ambiente

### Clonar o repositório

``` bash
git https://github.com/Felipe-cdb/Dashboard_bitdoglab.git
cd Dashboard_bitdoglab
```

### Instalar Python no Windows
Garanta que o Python esteja instalado corretamente:

Baixe em: https://www.python.org/downloads/

IMPORTANTE: Marque a opção “Add Python to PATH” na instalação

Verifique se o pyhon foi instalado no terminal (cmd ou PowerShell):
python --version

Minha versão utilizada: python 3.11.9

### Criar e ativar ambiente virtual (Venv)

#### Criar venv
Venv deve ser criado na raiz do projeto.

``` bash
python -m venv venv
```

#### Ativar venv

-   **Bash (Linux/MacOS):**

    ``` bash
    source venv/bin/activate
    ```

-   **Bash (gitbash com Windowns):**

    ``` bash
    source venv/Scripts/activate
    ```

-   **PowerShell (Windows):**

    ``` powershell
    .\venv\Scripts\activate
    ```

-   **CMD (Windows):**

    ``` cmd
    venv\Scripts\activate
    ```

#### Instalar dependências Python

``` bash
pip install -r requirements.txt
```

### Executar o projeto

Para iniciar a aplicação

``` bash
python run.py
```

### Alimente o Banco de dados SQLite
Para Visualizar os graficos e tabela pode utilizar o seed para alimentar o banco com dados fictícios, o scriot presente em app/seeds gera dados anterior a data e hora ao dia que o script for executado. Use esse script toda vez que desejar gerar novos dados para o servidor.

``` bash
python -m app.seeds.seed_database
```
