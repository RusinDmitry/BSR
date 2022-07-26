import pandas as pd
from app import app

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


if __name__ == '__main__':
    app.run_server(debug=False)