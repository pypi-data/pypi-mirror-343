Pré-requisitos:

Python 3.7+: Certifique-se de ter uma versão compatível do Python instalada.
Poetry: Instale o Poetry seguindo as instruções em https://python-poetry.org/ .
Conta no PyPI: Crie uma conta no PyPI em https://pypi.org/ . Você precisará verificar seu e-mail.
API Token do PyPI: Gere um token de API no seu perfil do PyPI. Isso é necessário para autenticar suas publicações. (Vá para "Account" -> "API tokens" no PyPI).
1. Criando um Projeto Poetry:

Se você já tem um projeto, pule para a etapa 2. Caso contrário, crie um novo projeto Poetry:
```
poetry new meu_projeto
cd meu_projeto
```
Isso criará uma estrutura de diretórios básica para o seu projeto.

2. Definindo o pyproject.toml:

O arquivo pyproject.toml é o coração do seu projeto Poetry. Verifique se ele está configurado corretamente. Aqui está um exemplo:
```
[tool.poetry]
name = "meu_projeto"
version = "0.1.0"
description = "Uma breve descrição do seu projeto."
authors = ["Seu Nome <seu.email@example.com>"]
license = "MIT"  # Escolha uma licença apropriada

[tool.poetry.dependencies]
python = "^3.8"  # Especifique a versão mínima do Python
# Adicione suas dependências aqui, por exemplo:
# requests = "^2.25.1"

[tool.poetry.dev-dependencies]
# Adicione dependências de desenvolvimento aqui, por exemplo:
# pytest = "^6.2.5"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

- name: O nome do seu pacote (deve ser único no PyPI).
- version: A versão inicial do seu pacote.
- authors: Uma lista de autores.
- license: A licença sob a qual seu código é distribuído.
- dependencies: As dependências do seu projeto.
- dev-dependencies: As dependências usadas apenas para desenvolvimento (testes, linting, etc.).

3. Escrevendo o Código:

Crie o código do seu projeto dentro do diretório meu_projeto. Por exemplo, crie um arquivo meu_projeto/meu_projeto.py com o seguinte conteúdo:

```
def hello_world():
  print("Olá, mundo!")
```

export PYPI_TOKEN=pypi-AgEIcHlwaS5vcmcCJDQwMDRmM2NlLTM5YjctNGNhOS1iMDM3LTcxNmU1ZjJmNGJjYwACKlszLCI4NGE0ODc5MC0zZTIzLTQ0MjEtYWRmOS1jNmU1ZGFjOTE1MTciXQAABiCxO0hIbjYpN5I_Ijgk5dU6s-AvbQLsYmjnyA0yk1otGQ