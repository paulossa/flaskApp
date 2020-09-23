### MVP feat promoções e-commerce 

Objetivos do back: 
- [x] CRUD produtos {id, nome, preco}
- [ ] Promoções. Initial: 3por1, 3por10
- [ ] Checkout 


#####  Comandos úteis: 

- Rodar aplicação: ```FLASK_APP=app.py python -m flask run```
- Rodar testes: ```coverage run -m pytest```



##### Notas levantadas ao longo do desenvolvimento 

- Primeiro ciclo: 
    - Foi criada a estrutura inicial do projeto, testes, CI. 
- Segundo ciclo: 
    - Adicionado CRUD de produtos + testes. 
- Terceiro ciclo: 
    - Adição de promoções
    - Relacionamento de [Promoções] para [Produtos] de 1-N, ou seja,
    uma promoção poderá estar relacionada a 0 ou mais produtos.