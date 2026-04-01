from flask import Flask
from app.routes.task_routes import task_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(task_bp)

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}, 200

    return app


if __name__ == "__main__":
    from app.config import Config
    app = create_app()
    app.run(host="0.0.0.0", port=Config.PORT)
