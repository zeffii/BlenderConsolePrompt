import bpy


def search_blenderscripting(input_string):
    try:
        import webbrowser
        search_string = 'http://blenderscripting.blogspot.com/search?q={}'
        webbrowser.open(search_string.format(input_string))
    except:
        print('unable to locate blenderscripting.blogspot.com')


def search_bpydocs(input_string):
    try:
        from urllib.request import urlopen
        d = urlopen('http://www.blender.org/documentation/250PythonDoc')
        d = d.read()
        s_path = str(d).split("/")[2]

        import webbrowser
        s_head = 'http://www.blender.org/documentation/'
        s_slug = '/search.html?q='
        s_tail = '&check_keywords=yes&area=default'
        s_term = input_string
        webbrowser.open(''.join([s_head, s_path, s_slug, s_term, s_tail]))
    except:
        print('unable to browse docs online')


def search_pydocs(input_string):
    try:
        import webbrowser
        search_head = 'http://docs.python.org/py3k/search.html?q='
        search_tail = '&check_keywords=yes&area=default'
        search_term = input_string
        webbrowser.open(''.join([search_head, search_term, search_tail]))
    except:
        print('unable to browse docs online')


def search_stack(input_string, mode):
    try:
        import webbrowser
        if mode == 1:
            # <string>?se
            base_url = 'http://blender.stackexchange.com'
        else:
            # <string>??se
            base_url = 'http://stackoverflow.com'

        search_string = base_url + '/search?q={}'
        input_string = input_string.replace(' ', '+')
        webbrowser.open(search_string.format(input_string))

        print('doing mode:', mode)
    except:
        print('unable to locate stachoverflow')


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
