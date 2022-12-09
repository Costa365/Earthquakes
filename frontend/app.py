from flask import Flask, render_template
import redis
from threading import Thread
from flask_sse import sse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://redis"
app.register_blueprint(sse, url_prefix='/events')

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

earthquakes = []

def events():
    try:
        red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
        sub = red.pubsub()
        sub.subscribe('earthquakes')
        print("Listening for events...")
        for message in sub.listen():
            if message is not None and isinstance(message, dict):
                msg = eval(str(message['data']))
                try:
                    print(msg.get('place', 'Not Set'))
                    earthquakes.insert(0,msg)
                    with app.app_context():
                        sse.publish({"message": msg}, type='publish')
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


@app.route('/')
def home():
  return render_template('main.html',earthquakes=earthquakes)

if __name__ == "__main__":
  Thread(target=events).start()
  app.run(host="0.0.0.0", port="5005", debug=True)