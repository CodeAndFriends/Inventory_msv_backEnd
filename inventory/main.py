from typing   import Union
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from fastapi  import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
       host = "redis-10979.c300.eu-central-1-1.ec2.cloud.redislabs.com",
       port =10979,
       password="jXjcvlUXQB30ZQv9Bs170n4V76PISAK1",
       decode_responses=True
)

class Product(HashModel):
    name:str
    price:float
    quantity:int

    class Meta:
        database = redis

@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    product = Product.get(pk)
    return product.delete(pk)
