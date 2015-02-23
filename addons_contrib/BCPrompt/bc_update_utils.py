# import bpy
import re
from urllib.request import urlopen

'''
design considerations

from past experience this should not totally flatten the existing install,
rather it it should copy the content (minus folders..2.7x etc) into a
new archive. So in the event of 'catastrophic' failure I can revert.

Further caution taken with regards to any symlinked folders which may exist.
For me inside addons and addons_contrib i have several such folders which
link to local git repository of addons in development.

I think the process should be
- locate download zip (After narrow down)
- start external python thread
- tell it where the current .exe is
- close blender
- zip all files in the executable folder
- read whitelist of addons to remove from the download zip before copy
in my case
    - addons/sverchok
    - addons_contrib/BioBlender
    - addons_contrib/tinyCAD
    - addons_contrib/BCPrompt
    - any more?
- remove all whitelisted folders from the download.zip
- unpack download.zip into correct place
- start blender
- end longrunning python thread

'''


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
