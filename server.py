import connexion
from config import connex_app

# Create the application instance
# app = connexion.App(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
connex_app.add_api('swagger.yml')

def set_cors_headers_on_response(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS'
    return response

connex_app.app.after_request(set_cors_headers_on_response)

# If we're running in stand alone mode, run the application
if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    parser.add_argument(
        "-d",
        "--debug",
        default=True,
        type=bool,
        help="Run app on debug mode, defaults to false",
    )
    args = parser.parse_args()
    port = args.port
    debug = args.debug

    connex_app.run(host="0.0.0.0", port=port, debug=debug)
