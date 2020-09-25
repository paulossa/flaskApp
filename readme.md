### MVP Feature Promoções

Ìndice 
- [Motivação](#motivação)
- [Objetivos do back](#objetivos-do-back)
- [Comandos Úteis](#comandos-úteis)
- [Ciclos do refatoramento](#ciclos)

---

##### Motivação 

Neste repositório temos o código do backend da aplicação que é um esboço para um sistema de promoções do SW e-commerce S/A.

O intuito inicial era fazer um CRUD básico de produtos.  
Poder relacionar promoções a esses produtos. 
Assim como, realizar compras e fazer um 'checkout' do carrinho, gerando uma descrição dos itens e das promoções que possam estar relacionadas com subconjuntos desses items. 

##### Abordagem 
Foram criados 2 modelos/tabelas para solucionar esse problema, sendo eles: 
- **Produto**
  - Contém um *Identificador(único)*, *Nome*, *Valor* e pode estar associado a **uma** promoção. 
- **Promoção** 
  - Contém uma *Descrição* e *Bytes* associados. Esses bytes compreendem uma função python serializada, que se adequa a um contrato que dita parâmetros de entrada e saída para o calculo do valor de produtos associados aquela promoção.


Como o **produto** pode estar ligado a apenas uma promoção, conhece o seu valor/preço. Então, 
ele encapsula a responsabilidade de calcular o seu preço para uma determinada quantidade de items.

Ele faz isso verificando se está associado a uma **promoção**. 
E caso esteja, aplica o calculo que deveria ser feito pela função. 

Exemplificado abaixo. 

```python 
class Product:
    ...
    def get_calculated_values(self, quantity: int) -> float:
        out = [{
            'product': self.name,
            'value': self.value * quantity,
            'sale': None,
            'quantity': quantity,
        }]

        if self.sale:
            unpickled_func = pickle.loads(self.sale.str_func)
            out = unpickled_func(self, quantity)

        return out
```

E o **Serviço de Checkout** portanto, utiliza os produtos de uma maneira elegante para montar a 
descrição da cobrança dos itens em um carrinho de compras.  
```python
def calculate_checkout(cart):
    """
    Usado para calcular o valor dos items em um carrinho
    :param cart: Lista de items no formato {id_product:str, quantity: int}
    :return: Lista de items no formato {product:str, value: flaot, sale: Optional[str], quantity: int}
    """
    out = []
    for item in cart:
        product = session().query(Product).get(item.get('id_product'))
        if product:
            out += product.get_calculated_values(item.get('quantity'))

    return out
```

Desta forma criar uma promoção é tão simples quanto, serializar uma função para bytes e associa-la a um produto. 
Uma evolução do site por exemplo, poderia fornecer uma interface similar a de um editor onde o usuário colocaria o código da função, como se estivesse utilizando uma plataforma com "HackerRank", "Spoj" e afins. 

```python 
def test_new_sale_25_percent_off(tst):
    # Criar uma nova promoção consiste apenas em:
    # - Criar função que obedeça contrato
    # - Criar promoção serializando função de calculo de preço de produtos
    # - Associar promoção aos produtos desejados

    def sale_25_percent_off(product, quantity):
        return [{
            "product": product.name,
            "value": product.value * quantity * (1 - 0.25),
            "quantity": quantity,
            "sale": "Desconto de 25%",
        }]

    sale = Sale(description="Desconto de 25%", str_func=pickle.dumps(sale_25_percent_off))
    session().add(sale)
    session().flush()

    product = Product(identifier='i321', name="Smartphone TchauMe", value=1000, id_sale=sale.id)
    session().add(product)
    session().flush()

    assert product.get_calculated_values(1) == [
        {
            "product": 'Smartphone TchauMe',
            "value": 750.0,
            "quantity": 1,
            "sale": "Desconto de 25%",
        }
    ]
```

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
    
