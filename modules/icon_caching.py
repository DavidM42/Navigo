from PIL import Image
import requests
from io import BytesIO
from urllib.parse import urlparse
import favicon
from base64 import b64encode
import pathlib

import os

class InvalidIconValueException(Exception):
    """Exception raised for when unreachable icon paths are found.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def cacheDownloadAndRelinkImages(data, dist_path: str):
    iconsDownloadedUrls = []
    for index, link in enumerate(data["links"]):
        # parse icon name with and without extensions
        try:
            icon_url = link["iconUrl"]
        except KeyError as e:
            icon_url = None
            # use library to find iconUrl if none given
            icons = favicon.get(link["href"])
            for icon in icons:
                # else have horde problem
                # gets first valid so best quality favicon
                if ".php?url=" not in icon.url:
                    icon_url = icon.url
                    break
            
            # found no valid iconUrl 
            if not icon_url: 
                print("Found no favicon for " + link["href"])
                print(icons)
                continue

        # could also use new webp or other next gen formats
        # but webP not supported in safari
        # thanks to https://stackoverflow.com/a/27253809
        icon_name_new_extension = b64encode(icon_url.encode()).decode() + '.png'
        webLink = 'static/' + icon_name_new_extension

        # create dist folder if new and construct path
        if not os.path.exists(dist_path):
            os.makedirs(dist_path)
        path = dist_path + icon_name_new_extension

        # add .. after absolute path of this file to start with absolute path of project
        absol_project_folder = str(pathlib.Path(__file__).parent.absolute()) + '/../'

        # get and cache iconImages or relink if existing
        if icon_url in iconsDownloadedUrls:
            data["links"][index]["iconUrl"] = webLink
        else:
            img = None
            if icon_url.startswith("http://") or icon_url.startswith("https://"):
                response = requests.get(icon_url)
                try:
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                    print("Cached " + icon_url + "...")
                except:
                    raise InvalidIconValueException("\"" + icon_url + "\" could not be retrieved. Check and correct this url")
            else:
                try:
                    img = Image.open(absol_project_folder + icon_url)
                    print("Resized " + icon_url + "...")
                except:
                    raise InvalidIconValueException(path + " could not be locally retrieved. Check that this file exists and the path is correct")

            if img is not None:
                # resize to 150px width and height
                # if this is changed also change max-widht in main.css
                basewidth = 150
                # would be to calculate height via aspect ratio
                # wpercent = (basewidth/float(img.size[0]))
                # hsize = int((float(img.size[1])*float(wpercent)))
                # img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                img = img.resize((basewidth,basewidth), Image.ANTIALIAS)

                # convert to rgba for png file, save and relink
                img.convert('RGBA')
                img.save(path)
                data["links"][index]["iconUrl"] = webLink
                iconsDownloadedUrls.append(icon_url)
    return data