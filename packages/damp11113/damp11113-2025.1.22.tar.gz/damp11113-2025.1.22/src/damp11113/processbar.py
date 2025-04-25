"""
damp11113-library - A Utils library and Easy to use. For more info visit https://github.com/damp11113/damp11113-library/wiki
Copyright (C) 2021-present damp11113 (MIT)

Visit https://github.com/damp11113/damp11113-library

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from shutil import get_terminal_size
from itertools import cycle
import math
import time
from threading import Thread
from time import sleep
from .utils import get_size_unit2, center_string, TextFormatter, insert_string

class Steps:
    steps1 = ['[   ]', '[-  ]', '[-- ]', '[---]', '[ --]', '[  -]']
    steps2 = ['[   ]', '[-  ]', '[ - ]', '[  -]']
    steps3 = ['[   ]', '[-  ]', '[-- ]', '[ --]', '[  -]', '[   ]', '[  -]', '[ --]', '[-- ]', '[-  ]']
    steps4 = ['[   ]', '[-  ]', '[ - ]', '[  -]', '[   ]', '[  -]', '[ - ]', '[-  ]', '[   ]']
    steps5 = ['[   ]', '[  -]', '[ --]', '[---]', '[-- ]', '[-  ]']
    steps6 = ['[   ]', '[  -]', '[ - ]', '[-  ]']
    expand_contract = ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]', '[    ]']
    rotating_dots = ['.    ', '..   ', '...  ', '.... ', '.....', ' ....', '  ...', '   ..', '    .', '     ']
    bouncing_ball = ['o     ', ' o    ', '  o   ', '   o  ', '    o ', '     o', '    o ', '   o  ', '  o   ', ' o    ', 'o     ']
    left_right_dots = ['[    ]', '[.   ]', '[..  ]', '[... ]', '[....]', '[ ...]', '[  ..]', '[   .]', '[    ]']
    expanding_square = ['[ ]', '[■]', '[■■]', '[■■■]', '[■■■■]', '[■■■]', '[■■]', '[■]', '[ ]']
    spinner = ['|', '/', '-', '\\', '|', '/', '-', '\\']
    zigzag = ['/   ', ' /  ', '  / ', '   /', '  / ', ' /  ', '/   ', '\\   ', ' \\  ', '  \\ ', '   \\', '  \\ ', ' \\  ', '\\   ']
    arrows = ['←  ', '←← ', '←←←', '←← ', '←  ', '→  ', '→→ ', '→→→', '→→ ', '→  ']
    snake = ['[>    ]', '[=>   ]', '[==>  ]', '[===> ]', '[====>]', '[ ===>]', '[  ==>]', '[   =>]', '[    >]']
    loading_bar = ['[          ]', '[=         ]', '[==        ]', '[===       ]', '[====      ]', '[=====     ]', '[======    ]', '[=======   ]', '[========  ]', '[========= ]', '[==========]']


class indeterminateStatus:
    def __init__(self, desc="Loading...", end="[ ✔ ]", timeout=0.1, fail='[ ❌ ]', steps=None):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.faill = fail

        self._thread = Thread(target=self._animate, daemon=True)
        if steps is None:
            self.steps = Steps.steps1
        else:
            self.steps = steps
        self.done = False
        self.fail = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{c} {self.desc}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def stopfail(self):
        self.done = True
        self.fail = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.faill}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

# This class is developed in 3 October 2023 at 5:00 PM
class LoadingProgress:
    def __init__(self, total=100, totalbuffer=None, length=50, fill='█', fillbufferbar='█', desc="Loading...", status="", enabuinstatus=True, end="[ ✔ ]", timeout=0.1, fail='[ ❌ ]', steps=None, unit="it", barbackground="-", shortnum=False, buffer=False, shortunitsize=1000, currentshortnum=False, show=True, clearline=True, indeterminate=False, barcolor="red", bufferbarcolor="white", barbackgroundcolor="black", color=False):
        """
        Simple loading progress bar python
        @param total: change all total
        @param desc: change description
        @param status: change progress status
        @param end: change success progress
        @param timeout: change speed
        @param fail: change error stop
        @param steps: change steps animation
        @param unit: change unit
        @param buffer: enable buffer progress (experiment)
        @param show: show progress bar
        @param indeterminate: indeterminate mode
        @param barcolor: change bar color
        @param bufferbarcolor: change buffer bar color
        @param barbackgroundcolor: change background color
        @param color: enable colorful
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.faill = fail
        self.total = total
        self.length = length
        self.fill = fill
        self.enbuinstatus = enabuinstatus
        self.status = status
        self.barbackground = barbackground
        self.unit = unit
        self.shortnum = shortnum
        self.shortunitsize = shortunitsize
        self.currentshortnum = currentshortnum
        self.printed = show
        self.clearline = clearline
        self.indeterminate = indeterminate
        self.barcolor = barcolor
        self.barbackgroundcolor = barbackgroundcolor
        self.enabuffer = buffer
        self.bufferbarcolor = bufferbarcolor
        self.fillbufferbar = fillbufferbar
        self.totalbuffer = totalbuffer
        self.enacolor = color

        self._thread = Thread(target=self._animate, daemon=True)

        if steps is None:
            self.steps = Steps.steps1
        else:
            self.steps = steps

        if self.totalbuffer is None:
            self.totalbuffer = self.total

        self.currentpercent = 0
        self.currentbufferpercent = 0
        self.current = 0
        self.currentbuffer = 0
        self.startime = 0
        self.done = False
        self.fail = False
        self.currentprint = ""

    def start(self):
        self._thread.start()
        self.startime = time.perf_counter()
        return self

    def update(self, i=1):
        self.current += i

    def updatebuffer(self, i=1):
        self.currentbuffer += i

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break

            if not self.indeterminate:
                if self.total != 0 or math.trunc(float(self.currentpercent)) > 100:
                    if self.enabuffer:
                        self.currentpercent = ("{0:.1f}").format(100 * (self.current / float(self.total)))

                        filled_length = int(self.length * self.current // self.total)

                        if self.enacolor:
                            bar = TextFormatter.format_text(self.fill * filled_length, self.barcolor)
                        else:
                            bar = self.fill * filled_length

                        self.currentbufferpercent = ("{0:.1f}").format(
                            100 * (self.currentbuffer / float(self.totalbuffer)))

                        if float(self.currentbufferpercent) >= 100.0:
                            self.currentbufferpercent = 100

                        filled_length_buffer = int(self.length * self.currentbuffer // self.totalbuffer)

                        if filled_length_buffer >= self.length:
                            filled_length_buffer = self.length

                        if self.enacolor:
                            bufferbar = TextFormatter.format_text(self.fillbufferbar * filled_length_buffer,
                                                                  self.bufferbarcolor)
                        else:
                            bufferbar = self.fillbufferbar * filled_length_buffer

                        bar = insert_string(bufferbar, bar)

                        if self.enacolor:
                            bar += TextFormatter.format_text(self.barbackground * (self.length - filled_length_buffer),
                                                            self.barbackgroundcolor)
                        else:
                            bar += self.barbackground * (self.length - filled_length_buffer)
                    else:
                        self.currentpercent = ("{0:.1f}").format(100 * (self.current / float(self.total)))
                        filled_length = int(self.length * self.current // self.total)
                        if self.enacolor:
                            bar = TextFormatter.format_text(self.fill * filled_length, self.barcolor)

                            bar += TextFormatter.format_text(self.barbackground * (self.length - filled_length),
                                                             self.barbackgroundcolor)
                        else:
                            bar = self.fill * filled_length
                            if self.enacolor:
                                bar = TextFormatter.format_text(bar, self.barcolor)
                            bar += self.barbackground * (self.length - filled_length)


                    if self.enbuinstatus:
                        elapsed_time = time.perf_counter() - self.startime
                        speed = self.current / elapsed_time if elapsed_time > 0 else 0
                        remaining = self.total - self.current
                        eta_seconds = remaining / speed if speed > 0 else 0
                        elapsed_formatted = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
                        eta_formatted = time.strftime('%H:%M:%S', time.gmtime(eta_seconds))
                        if self.shortnum:
                            stotal = get_size_unit2(self.total, '', False, self.shortunitsize, False, '')
                            scurrent = get_size_unit2(self.current, '', False, self.shortunitsize, self.currentshortnum, '')
                        else:
                            stotal = self.total
                            scurrent = self.current

                        if math.trunc(float(self.currentpercent)) > 100:
                            elapsed_time = time.perf_counter() - self.startime
                            elapsed_formatted = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))

                            bar = center_string(self.barbackground * self.length, TextFormatter.format_text("Indeterminate", self.barcolor))

                            self.currentprint = f"{c} {self.desc} | --%|{bar}| {scurrent}/{stotal} | {elapsed_formatted} | {get_size_unit2(speed, self.unit, self.shortunitsize)} | {self.status}"

                        else:
                            self.currentprint = f"{c} {self.desc} | {math.trunc(float(self.currentpercent))}%|{bar}| {scurrent}/{stotal} | {elapsed_formatted}<{eta_formatted} | {get_size_unit2(speed, self.unit, self.shortunitsize)} | {self.status}"
                    else:
                        if self.shortnum:
                            stotal = get_size_unit2(self.total, '', False, self.shortunitsize, False, '')
                            scurrent = get_size_unit2(self.current, '', False, self.shortunitsize, self.currentshortnum, '')
                        else:
                            stotal = self.total
                            scurrent = self.current


                        self.currentprint = f"{c} {self.desc} | {math.trunc(float(self.currentpercent))}%|{bar}| {scurrent}/{stotal} | {self.status}"
                else:
                    elapsed_time = time.perf_counter() - self.startime
                    elapsed_formatted = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))

                    bar = center_string(self.barbackground * self.length, TextFormatter.format_text("Indeterminate", self.barcolor))

                    self.currentprint = f"{c} {self.desc} | --%|{bar}| {elapsed_formatted} | {self.status}"
            else:
                elapsed_time = time.perf_counter() - self.startime
                elapsed_formatted = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))

                bar = center_string(self.barbackground * self.length, TextFormatter.format_text("Indeterminate", self.barcolor))

                self.currentprint = f"{c} {self.desc} | --%|{bar}| {elapsed_formatted} | {self.status}"

            if self.printed:
                print(f"\r{self.currentprint}", flush=True, end="")

            sleep(self.timeout)

            if self.printed and self.clearline:
                # This clears the previous printed line
                print("\r" + " " * len(self.currentprint), end="", flush=True)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def stopfail(self):
        self.done = True
        self.fail = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.faill}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()
