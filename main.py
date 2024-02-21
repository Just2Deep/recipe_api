from smilecook import app
from waitress import serve
import sys

sys.path.append("/smilecook")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
