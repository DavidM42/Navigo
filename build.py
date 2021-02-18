# -*- coding: utf-8 -*-

from staticjinja import Site
import json
from shutil import rmtree
import warnings
import logging
import pathlib

# own modules
from modules.icon_caching import cacheDownloadAndRelinkImages
from modules.manifest_making import createManifestForIndex

def absol_path_from_build_script(path: str):
    # add leading slash if necessary
    if not path.startswith("/"):
        path = "/" + path
    return str(pathlib.Path(__file__).parent.absolute()) + path

def render_index_page():
    # homepage site to copy static files
    # and link to all subjects
    print("===> Rendering Index page...")

    with open(absol_path_from_build_script('links.json'), encoding='utf-8') as json_file:
        data = json.load(json_file)

        # download all linked images and chang links to them to use cached local ones
        dist_static_path = absol_path_from_build_script('dist/static/')
        data = cacheDownloadAndRelinkImages(data, dist_static_path)

        with warnings.catch_warnings():
            # ignore this deprecation warning for now
            warnings.filterwarnings("ignore", message="staticpaths are deprecated. Use Make instead.")
            
            # decrease logging to warning
            loggy = logging.getLogger(__name__)
            loggy.setLevel(logging.WARNING)

            made_site = Site.make_site(
                outpath = absol_path_from_build_script("dist/"),
                searchpath = absol_path_from_build_script("templates/"),
                staticpaths = ["static/"],
                env_globals = data,
                logger=loggy
            )
            made_site.render()

        description = None
        if "description" in data:
            description = data["description"]

        # TODO catch missing values and throw good exception
        # remind to check spelling
        createManifestForIndex(data["title"], data["short_name"], data["color"], data["background_color"], description)

def re_render():
    try:
        # clear dist folder and does not ignore errors
        rmtree(absol_path_from_build_script('dist/'), False)
    except Exception as e:
        print("Dist folder did not exist so did not have to be deleted")
    render_index_page()

if __name__ == "__main__":
    re_render()