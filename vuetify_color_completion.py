import sublime_plugin
import sublime

# The following 2 lines can be generated with "grunt sublime" in the main bootstrap code
bootstrap_classes = ["red", "pink", "purple", "deep-purple", "indigo", "blue", "light-blue", "cyan", "teal", "green", "light-green", "lime", "yellow", "amber", "orange", "deep-orange", "brown", "blue-grey", "grey","black","white","transparent","red lighten-5","red lighten-4","red lighten-3","red lighten-2","red lighten-1","red darken-1","red darken-2","red darken-3","red darken-4","red accent-1","red accent-2","red accent-3","red accent-4","pink lighten-5","pink lighten-4","pink lighten-3","pink lighten-2","pink lighten-1","pink darken-1","pink darken-2","pink darken-3","pink darken-4","pink accent-1","pink accent-2","pink accent-3","pink accent-4","purple lighten-5","purple lighten-4","purple lighten-3","purple lighten-2","purple lighten-1","purple darken-1","purple darken-2","purple darken-3","purple darken-4","purple accent-1","purple accent-2","purple accent-3","purple accent-4","deep-purple lighten-5","deep-purple lighten-4","deep-purple lighten-3","deep-purple lighten-2","deep-purple lighten-1","deep-purple darken-1","deep-purple darken-2","deep-purple darken-3","deep-purple darken-4","deep-purple accent-1","deep-purple accent-2","deep-purple accent-3","deep-purple accent-4","indigo lighten-5","indigo lighten-4","indigo lighten-3","indigo lighten-2","indigo lighten-1","indigo darken-1","indigo darken-2","indigo darken-3","indigo darken-4","indigo accent-1","indigo accent-2","indigo accent-3","indigo accent-4","blue lighten-5","blue lighten-4","blue lighten-3","blue lighten-2","blue lighten-1","blue darken-1","blue darken-2","blue darken-3","blue darken-4","blue accent-1","blue accent-2","blue accent-3","blue accent-4","light-blue lighten-5","light-blue lighten-4","light-blue lighten-3","light-blue lighten-2","light-blue lighten-1","light-blue darken-1","light-blue darken-2","light-blue darken-3","light-blue darken-4","light-blue accent-1","light-blue accent-2","light-blue accent-3","light-blue accent-4","cyan lighten-5","cyan lighten-4","cyan lighten-3","cyan lighten-2","cyan lighten-1","cyan darken-1","cyan darken-2","cyan darken-3","cyan darken-4","cyan accent-1","cyan accent-2","cyan accent-3","cyan accent-4","teal lighten-5","teal lighten-4","teal lighten-3","teal lighten-2","teal lighten-1","teal darken-1","teal darken-2","teal darken-3","teal darken-4","teal accent-1","teal accent-2","teal accent-3","teal accent-4","green lighten-5","green lighten-4","green lighten-3","green lighten-2","green lighten-1","green darken-1","green darken-2","green darken-3","green darken-4","green accent-1","green accent-2","green accent-3","green accent-4","light-green lighten-5","light-green lighten-4","light-green lighten-3","light-green lighten-2","light-green lighten-1","light-green darken-1","light-green darken-2","light-green darken-3","light-green darken-4","light-green accent-1","light-green accent-2","light-green accent-3","light-green accent-4","lime lighten-5","lime lighten-4","lime lighten-3","lime lighten-2","lime lighten-1","lime darken-1","lime darken-2","lime darken-3","lime darken-4","lime accent-1","lime accent-2","lime accent-3","lime accent-4","yellow lighten-5","yellow lighten-4","yellow lighten-3","yellow lighten-2","yellow lighten-1","yellow darken-1","yellow darken-2","yellow darken-3","yellow darken-4","yellow accent-1","yellow accent-2","yellow accent-3","yellow accent-4","amber lighten-5","amber lighten-4","amber lighten-3","amber lighten-2","amber lighten-1","amber darken-1","amber darken-2","amber darken-3","amber darken-4","amber accent-1","amber accent-2","amber accent-3","amber accent-4","orange lighten-5","orange lighten-4","orange lighten-3","orange lighten-2","orange lighten-1","orange darken-1","orange darken-2","orange darken-3","orange darken-4","orange accent-1","orange accent-2","orange accent-3","orange accent-4","deep-orange lighten-5","deep-orange lighten-4","deep-orange lighten-3","deep-orange lighten-2","deep-orange lighten-1","deep-orange darken-1","deep-orange darken-2","deep-orange darken-3","deep-orange darken-4","deep-orange accent-1","deep-orange accent-2","deep-orange accent-3","deep-orange accent-4","brown lighten-5","brown lighten-4","brown lighten-3","brown lighten-2","brown lighten-1","brown darken-1","brown darken-2","brown darken-3","brown darken-4","blue-grey lighten-5","blue-grey lighten-4","blue-grey lighten-3","blue-grey lighten-2","blue-grey lighten-1","blue-grey darken-1","blue-grey darken-2","blue-grey darken-3","blue-grey darken-4","grey lighten-5","grey lighten-4","grey lighten-3","grey lighten-2","grey lighten-1","grey darken-1","grey darken-2","grey darken-3","grey darken-4","lighten-5","lighten-4","lighten-3","lighten-2","lighten-1","darken-1","darken-2","darken-3","darken-4","accent-1","accent-2","accent-3","accent-4"]



class BootstrapCompletions(sublime_plugin.EventListener):
    """
    Provide tag completions for Bootstrap elements and data-uk attributes
    """
    def __init__(self):

        self.class_completions = [("%s \tColor class - Vuetify" % s, s) for s in bootstrap_classes]

    def on_query_completions(self, view, prefix, locations):

        if view.match_selector(locations[0], "text.html string.quoted"):

            # Cursor is inside a quoted attribute
            # Now check if we are inside the class attribute

            # max search size
            LIMIT  = 250

            # place search cursor one word back
            cursor = locations[0] - len(prefix) - 1

            # dont start with negative value
            start  = max(0, cursor - LIMIT - len(prefix))

            # get part of buffer
            line   = view.substr(sublime.Region(start, cursor))

            # split attributes
            parts  = line.split('=')

            # is the last typed attribute a class attribute?
            if len(parts) > 1 and parts[-2].strip().endswith("color"):
                return self.class_completions
            else:
                return []
        elif view.match_selector(locations[0], "text.html meta.tag - text.html punctuation.definition.tag.begin"):

            # Cursor is in a tag, but not inside an attribute, i.e. <div {here}>
            # This one is easy, just return completions for the data-uk-* attributes
            return self.data_completions

        else:

            return []




  