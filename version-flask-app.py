import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import mysql.connector


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = '109.186.214.255'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'noanoa123'
app.config['MYSQL_DATABASE_DB'] = 'schema'

mysql.init_app(app)

# VERSION = [
    # {
    #     'ID': "v2.6.11",
    #     'Release notes': ['Security Fixes- Bump vue-server-renderer\'s dependency of serialize-javascript to 2.1.2',
    #                       'Bug Fixes- types: fix prop constructor type inference (#10779) 4821149, closes #10779',
    #                       'Bug Fixes- fix function expression regex (#9922) 569b728, closes #9922 #9920',
    #                       'Bug Fixes- compiler: Remove the warning for valid v-slot value (#9917) 085d188, closes #9917',
    #                       'Bug Fixes- types: fix global namespace declaration for UMD bundle (#9912) ab50e8e, closes #9912'],
    #     'Release Date': 'Dec 13, 2019',
    #     'Author': 'Evan You yyx990803'
    # },
    # {
    #     'ID': "v2.6.10",
    #     'Release notes': ['Bug Fixes- codegen: support named function expression in v-on (#9709) 3433ba5, closes #9709 #9707',
    #                         'core: cleanup timeouts for async components (#9649) 02d21c2, closes #9649 #9648',
    #                         'core: only unset dom prop when not present f11449d, closes #9650',
    #                         'core: use window.performance for compatibility in JSDOM (#9700) 653c74e, closes #9700 #9698',
    #                         'scheduler: revert timeStamp check 22790b2, closes #9729 #9632',
    #                         'slots: fix slots not updating when passing down normal slots as $scopedSlots ebc1893, closes #9699',
    #                         'types: allow using functions on the PropTypes (#9733) df4af4b, closes #9733 #9692',
    #                         'types: support string type for style in VNode data (#9728) 982d5a4, closes #9728 #9727'],
    #     'Release Date': 'Mar 20, 2019',
    #     'Author': 'Evan You yyx990803'
    # },
    # {
    #     'ID': "v2.6.7",
    #     'Release notes': ['Security Fixes- Bump vue-server-renderer\'s dependency of serialize-javascript to 2.1.2',
    #                       'Bug Fixes- avoid errors thrown during dom props update 8a80a23, closes #9459',
    #                        'Bug Fixes- avoid possible infinite loop by accessing observables in error handler (#9489) ee29e41, closes #9489',
    #                        'Bug Fixes- ensure generated scoped slot code is compatible with 2.5 7ec4627, closes #9545',
    #                        'Bug Fixes- ensure scoped slots update in conditional branches d9b27a9, closes #9534',
    #                        'Bug Fixes- scoped slots should update when inside v-for 8f004ea, closes #9506',
    #                        'Bug Fixes- #9511: avoid promise catch multiple times (#9526) 2f3020e, closes #9511 #9526 #9511 #9511 #9511',
    #                        'Bug Fixes- compiler: handle negative length in codeframe repeat 7a8de91'],
    #     'Release Date': 'Dec 13, 2019',
    #     'Author': 'Evan You yyx990803'
    # }
# ]

# configuration
DEBUG = True


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/releases', methods=['GET', 'POST'])
def get_all_releases():
    response_object = {'status': 'success'}
    # VERSION = []
    response_object['releases'] = init_version()
    return jsonify(response_object)


def get_release_request(post_data):
    release = {
        'ID': post_data.get('ID'),
        'Release notes': post_data.get('Release notes'),
        'Release Date': post_data.get('Release Date'),
        'Author': post_data.get('Author')
    }
    return release


@app.route('/releases', methods=['POST'])
def insert_release():
    response_object = {'status': 'success'}
    release = get_release_request(request.get_json())
    insert_release_to_db(release)
    response_object['message'] = 'Book added!'
    return jsonify(response_object)


@app.route('/releases/<release_id>', methods=['PUT'])
def update_single_releases(release_id):
    response_object = {'status': 'success'}
    release = get_release_request(request.get_json())
    delete_release(release_id)
    insert_release_to_db(release)
    response_object['message'] = 'Release updated!'

    return jsonify(response_object)


@app.route('/releases/<release_id>', methods=['DELETE'])
def delete_single_release(release_id):
    response_object = {'status': 'success'}
    delete_release(release_id)
    response_object['message'] = 'Release removed!'


# def init_db():
#     for version in VERSION:
#         insert_release_to_db(version)


def insert_note_release_to_db(release_id, note):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO schema.ReleasesNotes(ID, ReleaseID, Note) VALUES (%s, %s, %s)",
                    (uuid.uuid4().hex, release_id, note))
    conn.commit()
    cur.close()


def insert_release_to_db(release):
    conn = mysql.connect()
    cur = conn.cursor()
    id = release['ID']
    release_notes = release['Release notes']
    release_date = release['Release Date']
    author = release['Author']
    cur.execute("INSERT INTO schema.Release(ID, ReleaseDate, Author) VALUES (%s, %s, %s)",
                (id, release_date, author))
    if release_notes:
        for note in release_notes:
            cur.execute("INSERT INTO schema.ReleasesNotes(ID, ReleaseID, Note) VALUES (%s, %s, %s)",
                        (uuid.uuid4().hex, id, note))
    conn.commit()
    cur.close()


def get_single_release(release_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM schema.Release WHERE ID = \'" + release_id + "\'")
    release = cur.fetchone()
    conn.commit()
    cur.close()

    id = release[0]
    release_date = release[1]
    author = release[2]
    notes = get_notes_of_release(release_id)

    # cur.execute("SELECT * FROM schema.ReleasesNotes WHERE ReleaseID = \'" + id + "\'")
    # releases_notes_db = cur.fetchall()
    # notes = []
    #
    # for note in releases_notes_db:
    #     notes.append(note[2])

    return {
        'ID': id,
        'Release notes': notes,
        'Release Date': release_date,
        'Author': author
    }


def get_notes_of_release(release_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM schema.ReleasesNotes WHERE ReleaseID = \'" + release_id + "\'")
    releases_notes_db = cur.fetchall()
    notes = [note[2] for note in releases_notes_db]

    conn.commit()
    cur.close()

    return notes


def delete_release(release_id):
    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM schema.ReleasesNotes WHERE ReleaseID = \'" + release_id + "\'")
    cur.execute("DELETE FROM schema.Release WHERE ID = \'" + release_id + "\'")

    conn.commit()
    cur.close()


def init_version():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM schema.Release")
    releases = cur.fetchall()

    conn.commit()
    cur.close()
    VERSION = []
    for version in releases:
        id = version[0]
        release_date = version[1]
        author = version[2]
        notes = get_notes_of_release(release_id=id)

        VERSION.append({
            'ID': id,
            'Release notes': notes,
            'Release Date': release_date,
            'Author': author
        })
    return VERSION


if __name__ == '__main__':
    # init_db()
    init_version()
    app.run()
