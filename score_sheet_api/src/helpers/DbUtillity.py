from flask import jsonify

def Convert_to_Json(row_headers, datas):

    json_data = []
    for data in datas:
        json_data.append(dict(zip(row_headers,data)))
        
    return jsonify(json_data), 200

def Covert_to_Object_Json(header, data):
    return dict(zip(header,data))

def Handle_error(err, status_code):
    msg = [str(x) for x in err.args]
    response = {
        'success': False,
        'error': {
            'type': err.__class__.name,
            'message': msg
        }
    }
    
    
    return jsonify(response), status_code