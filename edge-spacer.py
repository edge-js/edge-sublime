import sublime
import sublime_plugin

# Handles the general {{ }} and {{{ }}}
class EdgeSpacerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # insert any closing brackets like sublime normally does
        self.view.run_command(
            'insert_snippet', {"contents": "{${0:$SELECTION}}"})

        for sel in self.view.sel():

            # if we're not selecting text
            if (sel.empty()):
                last = sel.end()
                lastChar = self.view.substr(last - 1)
                charBeforeLast = self.view.substr(last - 2)
                charBeforeThat = self.view.substr(last - 3)
                charAfter = self.view.substr(last + 1)

                # did we type two curly braces?
                if(lastChar == '{' and charBeforeLast == '{'):
                    # If this is something like {{{}  }}
                    if(charBeforeThat == '{'):
                        endOfLine = self.view.find_by_class(
                            last, True, sublime.CLASS_LINE_END)
                        lineStr = self.view.substr(
                            sublime.Region(last, endOfLine))
                        # since we automatically add a curly bracket, we need
                        # to check beyond this
                        firstCurly = lineStr.find('}')
                        nextCurly = lineStr.find('}', firstCurly + 1)

                        # check to see if we're adding brackets to an existing
                        # set, fix if needed
                        if (nextCurly != -1):
                            self.view.erase(
                                edit, sublime.Region(last, last + 1))
                            self.view.insert(
                                edit, last + (nextCurly - firstCurly), '}')

                    else:
                        # If we're typing this in the middle of some quotes,
                        # add an additional end curly brace, since sublime
                        # doesn't auto-close braces inside quotes all the time
                        if (charBeforeThat == '"' and charAfter == '"'):
                            self.view.insert(edit, last + 1, '}')

                        self.addSpaces(edit, last)

                # triple {{{ }}}
                elif(lastChar == '{' and
                        charBeforeLast == ' ' and
                        charBeforeThat == '{'):
                    # erase previous space
                    self.view.erase(edit, sublime.Region(last - 1, last - 2))

                    # erase latter space
                    self.view.erase(edit, sublime.Region(last, last + 1))

                    # add two spaces and center
                    self.addSpaces(edit, last - 1)
            # We are selecting text, so mind the selection
            else:
                start = sel.begin()
                end = sel.end()
                charBeforeStart = self.view.substr(start - 1)
                charBeforeThat = self.view.substr(start - 2)
                charEvenBeforeThat = self.view.substr(start - 3)
                charAfterEnd = self.view.substr(end)
                charAfterThat = self.view.substr(end + 1)
                charEvenAfterThat = self.view.substr(end + 2)

                # Double {{ }}
                if (charBeforeThat == '{' and charBeforeStart == '{' and
                        charAfterEnd == '}' and charAfterThat == '}'):
                    # put a space on either side of the selection
                    self.view.insert(edit, start, ' ')
                    self.view.insert(edit, end + 1, ' ')

                # more than double, like {{{ }}}
                elif(charEvenBeforeThat == '{' and
                        charBeforeThat == ' ' and
                        charBeforeStart == '{' and
                        charAfterEnd == '}' and
                        charAfterThat == ' ' and
                        charEvenAfterThat == '}'):
                    # erase previous space
                    self.view.erase(edit, sublime.Region(start - 1, start - 2))

                    # erase latter space
                    self.view.erase(edit, sublime.Region(end, end + 1))

                    # rewrap the selection
                    self.view.insert(edit, start - 1, ' ')
                    self.view.insert(edit, end, ' ')

    def addSpaces(self, edit, pos):
        # subtract current region from selection so we don't end up with
        # two selections in some cases
        self.view.sel().subtract(sublime.Region(pos, pos))

        # add 2 spaces
        self.view.insert(edit, pos, '  ')

        # move cursor to middle
        middle = pos + 1

        self.view.sel().add(sublime.Region(middle, middle))
