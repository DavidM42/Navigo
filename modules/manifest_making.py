import json
import pathlib


def createManifestForIndex(title: str, short_name: str, color: str, background_color: str, description=""):
    data = {
        "name": title,
        "short_name": short_name,
        "description": description,
        "theme_color": color,
        "background_color": background_color,
        "display": "browser",
        "orientation": "portrait",
        "scope": "/",
        "start_url": "/",
        "icons": [
            {
                "src": "/static/icons/pwa/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png"
            },
            {
                "src": "/static/icons/pwa/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png"
            },
            {
                "src": "/static/icons/pwa/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png"
            },
            {
                "src": "/static/icons/pwa/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png"
            },
            {
                "src": "/static/icons/pwa/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png"
            },
            {
                "src": "/static/icons/pwa/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/pwa/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png"
            },
            {
                "src": "/static/icons/pwa/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

    # add .. after absolute path of this file to start with absolute path of project
    absol_project_folder = str(pathlib.Path(
        __file__).parent.absolute()) + '/../'

    base_path = "dist/"
    filename = "manifest.json"

    path = absol_project_folder + base_path + filename
    print("Creating manifest.json for index...")

    # write json file for web manifest
    with open(path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
