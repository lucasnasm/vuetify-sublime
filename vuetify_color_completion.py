import sublime_plugin
import sublime
from .completions import color_classes


class VuetifyCompletions(sublime_plugin.EventListener):
    """
    Provide tag completions for Vuetify elements and v-{component} attributes
    """

    def __init__(self):
        self.color_class_completions = [
            ("%s \tColor class - Vuetify" % s, s) for s in color_classes]

    def on_query_completions(self, view, prefix, locations):

        if view.match_selector(locations[0], "text.html string.quoted"):

            # Cursor is inside a quoted attribute
            # Now check if we are inside the class attribute

            # max search size
            LIMIT = 250

            # place search cursor one word back
            cursor = locations[0] - len(prefix) - 1

            # dont start with negative value
            start = max(0, cursor - LIMIT - len(prefix))

            # get part of buffer
            line = view.substr(sublime.Region(start, cursor))

            # split attributes
            parts = line.split('=')

            # is the last typed attribute a color attribute?
            if len(parts) > 1 and parts[-2].strip().endswith("color"):
                return self.color_class_completions
            else:
                return []
        elif view.match_selector(locations[0], "text.html meta.tag - text.html punctuation.definition.tag.begin"):

            # Cursor is in a tag, but not inside an attribute, i.e. <div {here}>
            # This one is easy, just return completions for the v-* attributes
            return self.attributes_completions

        else:

            return []
