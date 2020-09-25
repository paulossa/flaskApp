### MVP Feature Promoções

Ìndice 
- [Motivação](#motivação)
- [Objetivos do back](#objetivos-do-back)
- [Comandos Úteis](#comandos-úteis)
- [Ciclos do refatoramento](#ciclos)

---

##### Motivação 

Neste repositório temos o refatoramento da solução, permitindo a consolidação da ideia original. 
Permitindo uma escalabilidade muito maior da aplicação. Com criação de novas promoções 
sem a necessidade de fazer deploy da aplicação. 

Para criar uma **promoção** seria necessário apenas de uma função serializada no formato de 
bytes. Essa função seria serializada e salva no banco e quando necessário seria desserializada
para fazer o calculo no preço dos produtos.  
Vale salientar que essa função deve *aderir a um contrato de entrada e saída*, para que o cálculo do preço 
de um carrinho de compras seja sempre consistente.

**O produto** encapsula a responsabilidade de calcular o seu preço para uma determinada quantidade de items.
Pois ele sabe, quando é o caso, se está associado a alguma promoção e a utiliza para calculo do preço.

E o **Serviço de Checkout** portanto, utiliza os produtos de uma maneira elegante para montar a 
descrição da cobrança dos itens em um carrinho de compras.  

--- 

#####  Objetivos do back 
- [x] CRUD produtos
- [x] Promoções Iniciais: 
  - [x] 3 por 10 
  - [x] Pague 1 Leve 2
  - [x] Facilidade de implementar novas promoções
- [x] Checkout 

--- 
#####  Comandos úteis: 
- Rodar aplicação:
  - ```FLASK_APP=sw_api/app.py python -m flask run```
- Rodar testes gerando cobertura: 
  - ```coverage run --source sw_api/ -m pytest```
- Mostrar relatório de cobertura: 
  - ```coverage report```
  - ```coverage html``` | gera htmlcov/ com relatório em html interativo e mais detalhado

--- 
##### Ciclos 
- Primeiro ciclo: 
    - Foi criada a estrutura inicial do projeto [backend], testes, CI. 
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
- Quinto ciclo: 
    - Ajustes no front para ligar com o novo backend.
    - Ajustes markdown com instruções sobre os projetos 
    