## 🛠️ Configuração do Ambiente Local (VS Code)

Para executar os notebooks desta pesquisa localmente sem conflitos de dependência, é recomendado o uso de um ambiente virtual (venv). Siga os passos abaixo:

### 1. Criar o Ambiente Virtual

Abra o terminal integrado do VS Code na pasta raiz do projeto e execute:

```bash
python3 -m venv .venv
```

2. Ativar o Ambiente

Dependendo do seu sistema operacional, rode o comando correspondente no terminal:

    Mac/Linux:
    Bash

    source .venv/bin/activate

    Windows (Prompt de Comando/PowerShell):
    Bash

    .venv\Scripts\activate

    Nota: O ambiente estará ativo quando aparecer (.venv) no início da linha do seu terminal.

3. Instalar Dependências

Com o ambiente ativado, instale os pacotes de análise de dados e o motor de execução do Jupyter:
Bash

pip install ipykernel pandas matplotlib seaborn

4. Conectar o Notebook no VS Code

   Abra o arquivo .ipynb do projeto.

   No canto superior direito da tela, clique no botão Select Kernel (ou onde aparece a versão do Python).

   Selecione a opção Python Environments.

   Escolha o ambiente recém-criado (geralmente marcado com uma estrela ou indicando o caminho /.venv/).

Pronto! Agora você pode executar as células de código normalmente.
