from app import jwt


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'admin': True}
    else:
        return {'admin': False}


@jwt.expired_token_loader
def expired_callback():
    return jsonify({
        "massage": "The token has expired"
    }), 401


@jwt.invalid_token_loader
def invalid_callback(err):
    return jsonify({
        "massage": "The token is invalid",
        "err": err
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback():
    return jsonify({
        "massage": "The token unauthorized"
    }), 401


@jwt.needs_fresh_token_loader
def fresh_callback():
    return jsonify({
        "massage": "The token have to be freshed"
    }), 401


@jwt.revoked_token_loader
def revoked_callback():
    return jsonify({
        "massage": "The token has revoked"
    }), 401
