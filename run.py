from app_fb import app
import json

if __name__ == '__main__':
    config = json.load(open('./config.json', 'r'))
    app.run(config['host'], config['port'], debug=True, threaded=True)
