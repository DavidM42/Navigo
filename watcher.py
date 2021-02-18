from typing import List
import os

from build import re_render, absol_path_from_build_script


# edit if other files should be watched
watch_paths = ["templates/", "links.json", "linkIcons/"]


# modified version of Reloader.py in staticjinja 1.0.4
class CustomReloader(object):
    def __init__(self, custom_event_handler_renderer, watch_paths: List[str] = []):
        self.custom_event_handler_renderer = custom_event_handler_renderer

        self.watch_paths: List[str] = []
        for path in watch_paths:
            absol_path = absol_path_from_build_script(path)
            self.watch_paths.append(absol_path)

    def should_handle(self, event_type, filename):
        started_with_watch_path = False
        for path in self.watch_paths:
            if filename.startswith(path):
                started_with_watch_path = True

        return (
            event_type in ("modified", "created")
            and started_with_watch_path
            and os.path.isfile(filename)
        )

    def event_handler(self, event_type, src_path):
        if self.should_handle(event_type, src_path):
            print("{} {}".format(event_type, src_path))
            # self.custom_event_handler_renderer(self.site)
            re_render()
            print("-------------------------------------------")

    def watch(self):
        import easywatch
        easywatch.watch(self.watch_paths, self.event_handler)

reloader = CustomReloader(re_render, watch_paths)
reloader.watch()