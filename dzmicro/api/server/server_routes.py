from flask import request, Flask

def route_registration(app: Flask) -> None:
    @app.route('/health')
    def health_check():
        return 'OK'
