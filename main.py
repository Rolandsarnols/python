import json

from flask import Flask
from flask import request
from pymongo import MongoClient
from config import mongo_conn, mongo_db


app = Flask(__name__)


def _connect_mongo(mongo_db, mongo_conn):
    conn = MongoClient(**mongo_conn)
    return conn[mongo_db]


@app.route("/api/user", methods=['GET', 'POST'])
def User():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            establishment = request.form.get('establishment')
            email = request.form.get('email')
            can_contact = request.form.get('can_contact')
            db = _connect_mongo(mongo_db, mongo_conn)
            user_id = db['User'].insert_one({'first_name': first_name,
                                             'last_name': last_name,
                                             'establishment': establishment,
                                             'email': email,
                                             'can_contact': can_contact,
                                             'last_badging_ts': None,
                                             'last_code': None}).inserted_id
            return str(user_id)
        except:
            return json.dumps({"status": "ERROR",
                               "message": "missing mandatory field",
                               "error": "missing mandatory field"})
    else:
        return 'There will be part 3'


if __name__ == '__main__':
    app.run()
