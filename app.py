import os
from score_sheet_api import app
import socket

if __name__ == '__main__':
    # app.run(debug=True, host=socket.gethostbyname(socket.gethostname())) 
    app.run(host="0.0.0.0",port=5000) 