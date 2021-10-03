import os
from score_sheet_api import app

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=8080) 