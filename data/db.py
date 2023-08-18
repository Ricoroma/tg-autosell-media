import os
import random
import sqlite3
import datetime
from os import system
from zipfile import ZipFile


def is_video_file(filename):
    video_file_extensions = (
        '.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec',
        '.aep', '.aepx',
        '.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf',
        '.asx', '.avb',
        '.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik',
        '.bin', '.bix',
        '.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine',
        '.cip',
        '.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat',
        '.dav', '.dce',
        '.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm',
        '.dmsm3d', '.dmss',
        '.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms',
        '.dvx', '.dxr',
        '.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp',
        '.fcproject',
        '.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp',
        '.h264', '.hdmov',
        '.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf',
        '.ivr', '.ivs',
        '.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg',
        '.m1v', '.m21',
        '.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv',
        '.mj2', '.mjp',
        '.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie',
        '.mp21',
        '.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex',
        '.mpl',
        '.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb',
        '.mvc',
        '.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv',
        '.nvc', '.ogm',
        '.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist',
        '.plproj',
        '.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr',
        '.pxv',
        '.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd',
        '.rmd',
        '.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk',
        '.sbt',
        '.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi',
        '.smi',
        '.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf',
        '.swi',
        '.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts',
        '.tsp', '.ttxt',
        '.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg', '.vem', '.vep', '.vf',
        '.vft',
        '.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7',
        '.vpj',
        '.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx',
        '.wot', '.wp3',
        '.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog',
        '.yuv', '.zeg',
        '.zm1', '.zm2', '.zm3', '.zmv')
    if any(i in filename for i in video_file_extensions):
        return True
    return False


def check_db():
    _ = system("cls")
    _datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    databaseFile = "data/database.db"
    db = sqlite3.connect(databaseFile, check_same_thread=False)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        print("----   Database was found   ----")
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, nickname TEXT, reg_date"
                       " TEXT, ref_id INT, balance INT, watched TEXT)")
        db.commit()
        print("----   Database was create   ---")
    try:
        cursor.execute("SELECT * FROM settings")
    except sqlite3.OperationalError:
        cursor.execute(
            "CREATE TABLE settings(id INTEGER PRIMARY KEY AUTOINCREMENT, qiwi TEXT, video INT, photo INT, stbal INT, "
            "bonus INT)")
        cursor.execute(f"INSERT INTO settings(qiwi, video, photo, stbal, bonus) VALUES ('89876543210', 10, 5, 30, 30)")
        db.commit()
    try:
        cursor.execute("SELECT * FROM albums")
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE albums(id INTEGER PRIMARY KEY, name TEXT, preview INTEGER, link TEXT, "
                       "photo_price INTEGER, video_price INTEGER, album_price INTEGER, description TEXT)")
        db.commit()
    try:
        cursor.execute("SELECT * FROM files")
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE files(id INTEGER PRIMARY KEY, type TEXT, file BLOB, album TEXT)")

    print(f"-----   {_datetime}   -----")
    print(f"---------   Users: {len(get_all_users())}   --------\n")


# ------------------------------

def get_now_date():
    date = datetime.date.today()
    return date


def add_user_to_db(user_id, nickname, ref_id, balance):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    if not (cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'").fetchone()):
        cursor.execute(
            f"INSERT INTO users(user_id, nickname, reg_date, ref_id, balance) VALUES ({user_id}, '{nickname}', "
            f"'{get_now_date()}', {ref_id}, {balance})")
    db.commit()


def update_nickname(user_id, nickname):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET nickname = '{nickname}' WHERE user_id = {user_id}")
    db.commit()


def get_settings():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM settings")
    row = cursor.fetchone()
    return row


def update_settings(command, value):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE settings SET {command} = '{value}'")
    db.commit()


def get_users_exist(user_id):
    db = sqlite3.connect("data/database.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
        return False
    else:
        return True


def get_info(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    row = cursor.fetchone()
    return row


def get_balance(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE user_id = {user_id}")
    row = cursor.fetchone()
    return row[0]


def set_balance(user_id, balance):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET balance = {balance} WHERE user_id = {user_id}")
    db.commit()


def set_balance_nickname(nickname, balance):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET balance = {balance} WHERE nickname = '{nickname}'")
    db.commit()


def get_refs(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE ref_id = {user_id}")
    row = cursor.fetchall()
    return len(row)


def get_pre_ref(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT ref_id FROM users WHERE user_id = {user_id}")
    row = cursor.fetchone()
    return row[0]


def get_top_ref(limit):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(
        f"SELECT COUNT(ref_id) AS ref_count, * FROM USERS WHERE ref_id != 0 GROUP BY ref_id ORDER BY COUNT(ref_id)"
        f" DESC LIMIT {limit}")
    row = cursor.fetchall()
    return row


def get_top_balance(limit):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users ORDER BY balance DESC LIMIT 5;")
    row = cursor.fetchall()
    return row


def get_all_users():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM users")
    row = cursor.fetchall()
    return row


def get_old_users(days):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(
        f"SELECT user_id FROM users WHERE ([reg_date] BETWEEN date('now', '-{days} day') AND date('now', '+1 day'))")
    row = cursor.fetchall()
    return row


def get_file(_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    db.commit()
    file = cursor.execute(f"SELECT * FROM files WHERE id = '{_id}'").fetchone()
    return file


def get_all_files(*_type):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    db.commit()
    request = f"SELECT * FROM files"
    if (_type):
        request = request + f" WHERE type = '{_type[0]}'"
    files = cursor.execute(request).fetchall()
    return files


def media_to_db(file, album, zip: ZipFile = None):
    if zip:
        with zip.open(file) as f:
            blob = f.read()
    else:
        with open(file, 'rb') as f:
            blob = f.read()

    type = 'video' if is_video_file(file) else 'photo'
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO files(type, file, album) VALUES(?,?,?)", (type, blob, album))
        conn.commit()


def create_album(name, preview, link, path, prices, desc):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        create_preview(name, preview, cursor)
        cursor.execute("INSERT INTO albums(name, preview, link, photo_price, video_price, album_price, description) "
                       "VALUES(?,?,?,?,?,?,?)", (name, cursor.lastrowid, link, *prices, desc))
        conn.commit()

    with ZipFile(path, 'r') as zip:
        for obj in zip.infolist():
            if obj.is_dir():
                continue
            zip.open(obj.filename)
            media_to_db(obj.filename, name, zip)


def create_preview(album, preview, cursor):
    with sqlite3.connect('data/database.db') as conn:
        cursor.execute("INSERT INTO files(type, file, album) VALUES(?,?,?)", ('photo', preview, album))
        conn.commit()


def get_random_photo(user_id):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        watched = get_info(user_id)[6]

        cursor.execute('SELECT * FROM files WHERE type="photo"')
        photos = cursor.fetchall()
        while True:
            photo = random.choice(photos)
            if str(photo[0]) in str(watched):
                continue
            else:
                return photo


def get_random_video(user_id):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        watched = get_info(user_id)[6]

        cursor.execute('SELECT * FROM files WHERE type="video"')
        videos = cursor.fetchall()
        while True:
            video = random.choice(videos)
            if str(video[0]) in str(watched):
                continue
            else:
                return video


def update_watched(user_id, new):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        watched = get_info(user_id)[6]
        cursor.execute("UPDATE users SET watched=? WHERE user_id=?", (f'{watched}|{new}', user_id))
        conn.commit()


def get_all_albums():
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM albums")
        return cursor.fetchall()


def get_album(album_id):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM albums WHERE id=?", (album_id,))
        return cursor.fetchone()


def get_photo_and_video_amount(name):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM files WHERE type="video" AND album=?', (name,))
        vid_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM files WHERE type="photo" AND album=?', (name,))
        ph_count = cursor.fetchone()[0]
        return ph_count, vid_count


def add_file_id(id, file_id):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE files SET file=? WHERE id=?', (file_id, id))
        conn.commit()


def get_photo_from_album(album, user_id):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        watched = get_info(user_id)[6]

        cursor.execute('SELECT * FROM files WHERE type="photo" and album=?', (album,))
        photos = cursor.fetchall()
        while True:
            photo = random.choice(photos)
            if str(photo[0]) in str(watched):
                continue
            else:
                return photo


def get_video_from_album(album, user_id):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        watched = get_info(user_id)[6]

        cursor.execute('SELECT * FROM files WHERE type="video" and album=?', (album,))
        videos = cursor.fetchall()
        while True:
            video = random.choice(videos)
            if str(video[0]) in str(watched):
                continue
            else:
                return video


def delete_album(album_name):
    with sqlite3.connect('data/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM albums WHERE name=?', (album_name,))
        cursor.execute('DELETE FROM files WHERE album=?', (album_name,))
        conn.commit()
