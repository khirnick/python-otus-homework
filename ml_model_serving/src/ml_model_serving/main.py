from fastapi.applications import FastAPI

from ml_model_serving.handlers.ping import ping
from ml_model_serving.handlers.login import login_for_access_token
from ml_model_serving.handlers.models import model_inference
from ml_model_serving.models import initialize_models


app = FastAPI(root_path='/api/v1')
app.add_api_route('/ping', ping, methods=['GET'])
app.add_api_route('/token', login_for_access_token, methods=['POST'])
app.add_api_route('/models/{model_name}/inference', model_inference, methods=['POST'])
initialize_models()
