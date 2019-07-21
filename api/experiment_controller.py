from flask import jsonify
from api import api_bp
from api.error import bad_request
import json
import config


@api_bp.route("/available_ip_num", methods=['GET'])
def get_available_ip_num():
    """
    获取可用的ip数目
    """
    with open(config.total_ips_file_path, 'r') as fp:
        ip_2_status = json.load(fp)
    all_status = ip_2_status.values()
    result = sum(map(lambda x: 1 if x['is_available'] else 0, all_status))
    return jsonify(dict(status_code=200,
                        message=result))


@api_bp.route("/experiments_list", methods=['GET'])
def get_experiments_list():
    """
    获取实验名称列表
    """
    with open(config.experiment_file_path, 'r') as fp:
        experiments = json.load(fp)
    assert isinstance(experiments, dict)
    return jsonify(dict(status_code=200,
                        message=list(experiments.keys())))


@api_bp.route("/experiments/<string:experiment_id>/ips", methods=['GET'])
def get_experiment_ips(experiment_id):
    """
    获取实验对应的ip列表
    """
    with open(config.experiment_file_path, 'r') as fp:
        experiments = json.load(fp)
    assert isinstance(experiments, dict)
    if experiment_id not in experiments:
        return bad_request('Experiment not exit')
    return jsonify(dict(status_code=200,
                        message=experiments[experiment_id]))


@api_bp.route("/experiments/release/<string:experiment_id>", methods=['GET'])
def release_experiment(experiment_id):
    """
    释放某个实验对应的ip资源
    """
    with open(config.experiment_file_path, 'r') as fp:
        experiments = json.load(fp)
    if experiment_id not in experiments:
        return bad_request('Experiment `%s` not exist' % experiment_id)

    release_ips = experiments[experiment_id]
    del experiments[experiment_id]
    with open(config.experiment_file_path, 'w') as fp:
        json.dump(experiments, fp)

    with open(config.total_ips_file_path, 'r') as fp:
        ip_2_status = json.load(fp)
    for ip in release_ips:
        ip_2_status[ip]['is_available'] = True
        ip_2_status[ip]['experiment'] = None
    with open(config.total_ips_file_path, 'w') as fp:
        json.dump(ip_2_status, fp)
    return jsonify(dict(status_code=200, message='Release Success'))


@api_bp.route("/experiments/create/<string:experiment_id>/<int:ip_num>", methods=['GET'])
def create_experiment(experiment_id, ip_num):
    """
    创建一个实验，并为其分配资源
    """
    if experiment_id is None or ip_num is None:
        return bad_request('Need experiment_id and ip_num')

    # 在total_ips中找到ip_num个可用的ip
    result = []
    with open(config.total_ips_file_path, 'r') as fp:
        ip_2_status = json.load(fp)
    for ip, status in ip_2_status.items():
        if len(result) == ip_num:
            break
        if status['is_available']:
            result.append(ip)

    if len(result) != ip_num:
        return bad_request("Can't find %d available ips" % ip_num)

    # 更新total_ip
    for ip in result:
        ip_2_status[ip]['is_available'] = False
        ip_2_status[ip]['experiment'] = experiment_id
    with open(config.total_ips_file_path, 'w') as fp:
        json.dump(ip_2_status, fp)

    # 更新experiments
    with open(config.experiment_file_path, 'r') as fp:
        experiments = json.load(fp)
    experiments[experiment_id] = result
    with open(config.experiment_file_path, 'w') as fp:
        json.dump(experiments, fp)

    return jsonify(dict(status_code=200,
                        message=dict(experiment_id=experiment_id,
                                     ip_num=ip_num,
                                     ip_list=result)))
