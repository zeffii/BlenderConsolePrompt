# import bpy
import re
from urllib.request import urlopen


def peek_builder_org(search_target):
    base_url = 'https://builder.blender.org/download/'
    print('reading from', base_url)
    d = urlopen(base_url)
    d = d.read().decode('utf8')
    d = d.split('\n')

    # #print(d)

    # #rpath = r'C:\Users\dealga\Desktop\panz.html'
    # #with open(rpath) as f:
    # #    d = f.readlines()

    hrefs = []
    pattern = 'href=\"(.*)\"\>'

    for line in d:
        if ('href=' in line):
            if all([(target in line) for target in search_target]):
                full_line = line.strip()
                match = re.search(pattern, full_line)
                href_str = match.group(1)
                hrefs.append(href_str)

    return hrefs if hrefs else None

# if True:
#     f = peek_builder_org(['win32', '>ble'])
#     print(f
