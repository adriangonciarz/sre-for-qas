from resources import AnimalsController, ReturnAlwaysOkController, EchoStatusController, HelloController, \
    AnimalDetailsController
import os

from flask import Flask
from flask_restful import Api
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__, static_url_path='')
api = Api(app)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='0.0.1')

api.add_resource(AnimalsController, '/animals')
api.add_resource(AnimalDetailsController, '/animals/<string:animal_id>')
api.add_resource(ReturnAlwaysOkController, '/ok')
api.add_resource(EchoStatusController, '/echostatus/<int:status_code>')
api.add_resource(HelloController, '/')

port = int(os.environ.get('PORT', 8080))
app.run(debug=True, host='0.0.0.0', port=port)
