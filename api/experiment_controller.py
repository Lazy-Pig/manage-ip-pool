from flask import jsonify, request
from api import api_bp
from api.error import bad_request
import json


@api_bp.route("/experiments_list", methods=['GET'])
def get_experiments_list():
    """
    获取实验名称列表
    """
    content = _read_data()
    if content == '':
        return jsonify([])

    experiments = json.loads(content)
    assert isinstance(experiments, dict)
    return jsonify(list(experiments.keys()))


@api_bp.route("/experiments/<string:experiment_id>/ips", methods=['GET'])
def get_experiment_ips(experiment_id):
    content = _read_data()
    if content == '':
        return bad_request('No Experiment')

    experiments = json.loads(content)
    assert isinstance(experiments, dict)
    if experiment_id not in experiments:
        return bad_request('Experiment not exit')
    return jsonify(experiments[experiment_id])


@api_bp.route("/experiments/create/<string:experiment_id>/<int:ip_num>", methods=['GET'])
def create_experiment_ips(experiment_id, ip_num):
    pass


def _read_data():
    with open('data/experiments.json', 'r') as fp:
        content = fp.read()
    return content
