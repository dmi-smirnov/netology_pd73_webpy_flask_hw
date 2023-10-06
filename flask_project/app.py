from flask import Flask
from flask import request
from flask.views import MethodView

import db


app = Flask(__name__)


class APIAdvView(MethodView):
    def get(self, adv_id: int):
        adv = db.get_adv(adv_id)
        if not adv:
            return {
                'status': 'error',
                'description': f'Advertisement with id={adv_id} not found.'
            }, 404
        return adv.to_dict(), 200
    
    def post(self):
        if not request.json: 
            return {
                'status': 'error',
                'description': "There is no JSON data in the request"
            }, 400
        new_adv_id = db.create_adv(request.json)
        return {'id': new_adv_id}, 201

    def delete(self, adv_id: int):
        if not db.delete_adv(adv_id):
            return {
                'status': 'error',
                'description': f'Advertisement with id={adv_id} not found.'
            }, 404
        return '', 204


api_route = '/api'
adv_view = APIAdvView.as_view('adv')
app.add_url_rule(
    rule=f'{api_route}/adv/<int:adv_id>',
    view_func=adv_view,
    methods=['GET', 'DELETE']
)
app.add_url_rule(
    rule=f'{api_route}/adv/',
    view_func=adv_view,
    methods=['POST']
)