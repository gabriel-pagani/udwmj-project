# Descrição
Site de pesquisa de receitas culinárias

# Site
Acesse o site do projeto [aqui](https://recipedia.online/)

# Pré-requisitos
- Python 3.9+
- Git 2.43+

# Instalação
- Clone o repositório
```
git clone https://github.com/gabriel-pagani/udwmj-project.git
```
- Entre na pasta clonada
```
cd udwmj-project
```
- Crie um ambiente virtual
```
python -m venv venv
```
- Ative o ambiente virtual
```
source venv/bin/activate
```
- Instale as dependências
```
pip install -r requirements.txt
```
- Aplique as migrações
```
python .\manage.py migrate
```
- Crie um super usuário
```
python .\manage.py createsuperuser
```

# Estrutura do Projeto
```
udwmj-project/
├── app/
├── project/
├── static/
├── templates/
├── venv/
├── .gitignore
├── db.sqlite3
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```

# Mode de Uso
- Execulte o servidor de desenvolvimento
```
python manage.py runserver
```

# Licença 
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/gabriel-pagani/udwmj-project/blob/main/LICENSE) para mais detalhes. A Licença MIT é uma licença de software livre que permite o uso, cópia, modificação e distribuição do código, desde que incluída a nota de direitos autorais e a permissão original.

# Contato 
Email - gabrielpaganidesouza@gmail.com
