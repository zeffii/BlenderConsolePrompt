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
- remove all whitelisted folders from the download.zip
- unpack download.zip into correct place
- start blender
- end longrunning python thread

'''


def get_whitelist():
    # this whitelist allows users to prevent an overwrite of certain files
    # or folders inside
    folders = {
        "addons": [
            "/Flow",
            "/sverchok"
        ],
        "addons_contrib": [
            "/mesh_tinyCAD",
            "/BioBlender",
            "/BCPrompt"
        ],
        "addons_extern": [

        ]
    }
    return dict(items=folders)


def peek_builder_org(search_target):
    base_url = 'https://builder.blender.org/download/'
    print('reading from', base_url)
    d = urlopen(base_url)
    d = d.read().decode('utf8')
    d = d.split('\n')

    hrefs = []
    pattern = 'href=\"(.*)\"\>'

    if len(search_target) == 1:
        '''
        this allows user to type:  -up win32
        by adding >ble, the result will only be blender master, not a branch.
        '''
        search_target.append('>ble')

    for line in d:
        if ('href=' in line):
            if all([(target in line) for target in search_target]):
                full_line = line.strip()
                match = re.search(pattern, full_line)
                href_str = match.group(1)
                hrefs.append(base_url + href_str)

    return hrefs

# if True:
#     f = peek_builder_org(['win32', '>ble'])
#     print(f)


def process_zip(url):
    wl = get_whitelist()
    print(url)

    for k, v in wl['items'].items():
        for f in v:
            print(k + f)

    pass
