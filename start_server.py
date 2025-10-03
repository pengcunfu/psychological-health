from app import app
from psychological.config import cfg

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=cfg.get("app.debug"))
