### MVP feat promoções e-commerce 

Objetivos do back: 
- [x] CRUD produtos
- [x] Promoções Iniciais: 
  - [x] 3 por 10 
  - [x] Pague 1 Leve 2
- [x] Checkout 


#####  Comandos úteis: 

- Rodar aplicação:
  - ```FLASK_APP=sw_api/app.py python -m flask run```
- Rodar testes gerando cobertura: 
  - ```coverage run --source sw_api/ -m pytest```
- Mostrar relatório de cobertura: 
  - ```coverage report```
  - ```coverage html``` | gera htmlcov/ com relatório em html interativo e mais detalhado

##### Notas levantadas ao longo do desenvolvimento 

- Primeiro ciclo: 
    - Foi criada a estrutura inicial do projeto, testes, CI. 
- Segundo ciclo: 
    - Adicionado CRUD de produtos + testes. 
- Terceiro ciclo:
    - Adição de promoções
    - Relacionamento de [Promoções] para [Produtos] de 1-N, ou seja,
    uma promoção poderá estar relacionada a 0 ou mais produtos.
    - Adição de bootstrap ao iniciar a aplicação.
- Quarto ciclo: 
    - Adição de testes de promoções
    - Aumentando cobertura de testes
    - Adição de endpoint de checkout + serviço de checkout
    - Adição de testes de checkout 