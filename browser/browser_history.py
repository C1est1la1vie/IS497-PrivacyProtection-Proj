import os
import sqlite3
import sys

def get_username() -> str:
    """
    Get username based on their local computers
    """
    user_platformcode = url_init()
    platform_code = user_platformcode
    cwd_path = os.getcwd()
    cwd_path_list = []
    # if it is a macOS
    if platform_code == 1:
        cwd_path_list = cwd_path.split('/')
    # if it is a windows
    elif platform_code == 2:
        cwd_path_list = cwd_path.split('\\')
    # if it is a linux
    else:
        cwd_path_list = cwd_path.split('/')
    return cwd_path_list[2]

def url_init():
    # platform_table maps the name of user's OS to a platform code
    platform_table = {
        'linux': 0,
        'linux2': 0,
        'darwin': 1,
        'cygwin': 2,
        'win32': 2,
    }

    # it supports Linux, MacOS, and Windows platforms.
    try:
        user_platformcode = platform_table[sys.platform]
    except KeyError:
        class NotAvailableOS(Exception):
            pass

        raise NotAvailableOS("It does not support your OS.")
    return user_platformcode

def get_database_paths() -> dict:
    """
    Get paths to the database of browsers and store them in a dictionary.
    It returns a dictionary: its key is the name of browser in str and its value is the path to database in str.
    """
    user_platformcode = url_init()
    platform_code = user_platformcode
    browser_path_dict = dict()
    # if it is a macOS
    if platform_code == 1:
        cwd_path = os.getcwd()
        cwd_path_list = cwd_path.split('/')
        # it creates string paths to broswer databases
        abs_safari_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Safari', 'History.db')
        abs_chrome_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'Google/Chrome/Default', 'History')
        abs_firefox_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'Firefox/Profiles')
        # check whether the databases exist
        if os.path.exists(abs_safari_path):
            browser_path_dict['safari'] = abs_safari_path
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            # it looks for a directory that ends '.default'
            for f in firefox_dir_list:
                if f.find('.default') > 0:
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
            # check whether the firefox database exists
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path
    # if it is a windows
    if platform_code == 2:
        homepath = os.path.expanduser("~")
        abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
        abs_firefox_path = os.path.join(homepath, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        # it creates string paths to broswer databases
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            for f in firefox_dir_list:
                if f.find('.default') > 0:
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path
    # if it is a linux and it has only a firefox
    if platform_code == 0:
        cwd_path = os.getcwd()
        cwd_path_list = cwd_path.split('/')
        # it creates string paths to broswer databases
        abs_firefox_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], '.mozilla', 'firefox')
        # check whether the path exists
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            # it looks for a directory that ends '.default'
            for f in firefox_dir_list:
                if f.find('.default') > 0:
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
            # check whether the firefox database exists
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path
    return browser_path_dict

def get_browserhistory() -> dict:
    # browserhistory is a dictionary that stores the query results based on the name of browsers.
    browserhistory = {}
    # call get_database_paths() to get database paths.
    paths2databases = get_database_paths()
    for browser, path in paths2databases.items():
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            _SQL = ''
            # SQL command for browsers' database table
            if browser == 'chrome':
                _SQL = """SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') 
                                    AS last_visit_time FROM urls ORDER BY last_visit_time DESC"""
            elif browser == 'firefox':
                _SQL = """SELECT url, title, datetime((visit_date/1000000), 'unixepoch', 'localtime') AS visit_date 
                                    FROM moz_places INNER JOIN moz_historyvisits on moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC"""
            elif browser == 'safari':
                _SQL = """SELECT url, title, datetime(visit_time + 978307200, 'unixepoch', 'localtime') 
                                    FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item ORDER BY visit_time DESC"""
            else:
                pass
            # query_result will store the result of query
            query_result = []
            try:
                cursor.execute(_SQL)
                query_result = cursor.fetchall()
            except sqlite3.OperationalError:
                print('* Notification * ')
                print('Please Completely Close ' + browser.upper() + ' Window')
            except Exception as err:
                print(err)
            # close cursor and connector
            cursor.close()
            conn.close()
            # put the query result based on the name of browsers.
            browserhistory[browser] = query_result

        except sqlite3.OperationalError:
            print('* ' + browser.upper() + ' Database Permission Denied.')

    return browserhistory

def del_browserhistory(choice):
    # browserhistory is a dictionary that stores the query results based on the name of browsers.
    # call get_database_paths() to get database paths.
    paths2databases = get_database_paths()
    for browser, path in paths2databases.items():
        if browser == choice:
            try:
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                _SQL = ''
                # SQL command for browsers' database table
                if browser == 'chrome':
                    _SQL = """DELETE FROM urls"""
                elif browser == 'firefox':
                    _SQL = """DELETE FROM moz_places"""
                elif browser == 'safari':
                    _SQL = """DELETE FROM history_visits"""
                else:
                    pass
                try:
                    cursor.execute(_SQL)
                    conn.commit()
                except sqlite3.OperationalError:
                    print('* Notification * ')
                    print('Please Completely Close ' + browser.upper() + ' Window')
                except Exception as err:
                    print(err)
                # close cursor and connector
                cursor.close()
                conn.close()

            # put the query result based on the name of browsers.
            except sqlite3.OperationalError:
                print('* ' + browser.upper() + ' Database Permission Denied.')

def del_key_record(choice,target):
    # browserhistory is a dictionary that stores the query results based on the name of browsers.
    # call get_database_paths() to get database paths.
    paths2databases = get_database_paths()

    for browser, path in paths2databases.items():
        if browser == choice:
            try:
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                _SQL = ''
                # SQL command for browsers' database table
                if browser == 'chrome':
                    _SQL = """DELETE FROM urls where title=""" + "'"+target+"'"
                elif browser == 'firefox':
                    _SQL = """DELETE FROM moz_places where title=""" + "'"+target+"'"
                elif browser == 'safari':
                    _SQL = """DELETE FROM history_visits where title=""" + "'"+target+"'"
                else:
                    pass
                try:
                    cursor.execute(_SQL)
                    conn.commit()
                except sqlite3.OperationalError:
                    print('* Notification * ')
                    print('Please Completely Close ' + browser.upper() + ' Window')

                except Exception as err:
                    print(err)
                # close cursor and connector
                cursor.close()
                conn.close()
            # put the query result based on the name of browsers.
            except sqlite3.OperationalError:
                print('* ' + browser.upper() + ' Database Permission Denied.')


