#!/usr/bin/python


class ShellColor(object):
    """
    Colors strings based on XML-esque lookup or color name for display in bash.
    """
    def __init__(self):
        colorcodes = dict(BLACK=0, RED=1, GREEN=2, YELLOW=3, BLUE=4, MAGENTA=5, CYAN=6, WHITE=7)
        levels = dict(
            WARNING=colorcodes['YELLOW'],
            INFO=colorcodes['WHITE'],
            DEBUG=colorcodes['BLUE'],
            CRITICAL=colorcodes['RED'],
            ERROR=colorcodes['RED']
        )
        self.colorcodes = dict(list(colorcodes.items()) + list(levels.items()))
        self.strcodes = {
            '<black>': 'BLACK', '<red>': 'RED', '<green>': 'GREEN', '<yellow>': 'YELLOW', '<blue>': 'BLUE',
            '<magenta>': 'MAGENTA', '<cyan>': 'CYAN', '<white>': 'WHITE', '<warning>': 'WARNING', '<info>': 'INFO',
            '<debug>': 'DEBUG', '<critical>': 'CRITICAL', '<error>': 'ERROR', '<bold>': 'BOLD', '<reset>': 'RESET'
        }

    def _color_code(self, code):
        RESET_SEQ = "\033[0m"
        COLOR_SEQ = "\033[1;%dm"
        BOLD_SEQ = "\033[1m"
        out = ''
        if code in self.strcodes:
            if code == '<reset>':
                return RESET_SEQ
            if code == '<bold>':
                out += BOLD_SEQ
            else:
                out += COLOR_SEQ % (30 + self.colorcodes[self.strcodes[code]])
        elif code in self.colorcodes:
            if code == 'RESET':
                return RESET_SEQ
            if code == 'BOLD':
                out += BOLD_SEQ
            else:
                out += COLOR_SEQ % (30 + self.colorcodes[code])
        else:
            return RESET_SEQ
        return out

    def coded_colorize(self, message):
        for code in self.strcodes:
            message = message.replace(code, self._color_code(code))
        message += self._color_code('RESET')
        return message

    def colorize(self, message, color):
        message = self._color_code(color) + message
        message += self._color_code('RESET')
        return message

if __name__ == '__main__':
    print """
             This is meant to be an imported class.
             Usage:
               c = ShellColor()
               print c.coded_colorize('<yellow><bold>message <green>and more')
               OR
               print c.colorize('green message', 'GREEN')
          """