from resources import AnimalsController, ReturnAlwaysOkController, EchoStatusController, HelloController, \
    AnimalDetailsController, ErrorController, SlowController
import os

from flask import Flask
from flask_restful import Api
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__, static_url_path='')
api = Api(app)
PrometheusMetrics(app)

api.add_resource(AnimalsController, '/animals')
api.add_resource(AnimalDetailsController, '/animals/<string:animal_id>')
api.add_resource(ReturnAlwaysOkController, '/ok')
api.add_resource(EchoStatusController, '/echostatus/<int:status_code>')
api.add_resource(HelloController, '/')
api.add_resource(ErrorController, '/areyoulucky')
api.add_resource(SlowController, '/slow')

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
