from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Define the JWKS (Replace keys with your own)
jwks = {
    "keys": [
        {
            "kty": "RSA",
            "use": "sig",
            "kid": "1",
            "alg": "RS256",
            "n": "lBS-cNSh_jlFwz_U9j-7pAIwDKOYyz0eR88DLSO_0KbNK4oL8nUklFho62AtCEhuVvNIgav-MA2xI-346qm_2ts3-Qiw_Gp1>
            "e": "AQAB"
        }
    ]
}


@app.route('/.well-known/jwks.json')
def jwks_endpoint():
    """Serve the JWKS document."""
    return jsonify(jwks)

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

