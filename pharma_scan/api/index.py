from mangum import Mangum
from pharma_scan.main import app

handler = Mangum(app, lifespan="off")