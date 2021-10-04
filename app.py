import os
from score_sheet_api import app
import socket

if __name__ == '__main__':
    app.run(host=socket.gethostbyname(socket.gethostname()),port=3000) 
    # app.run(debug=True, host="0.0.0.0",port=8080) 