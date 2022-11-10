from typing   import Union
from redis_om import get_redis_connection
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
    return Product.all_pks()


@app.post('/products')
def create(product: Product):
    return product.save()

