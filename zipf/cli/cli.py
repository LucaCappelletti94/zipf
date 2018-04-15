from __future__ import division
import sys
import curses
import time
from datetime import datetime, timedelta
from multiprocessing import Process
import traceback
import json

class cli:
    def __init__(self, statistics):
        self._statistics = statistics
        self._i=0
        self._max_len = 0
        self._outputs = {}

    def _cli(self):
        self._statistics.set_start_time()
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        try:
            while True:
                time.sleep(0.1)
                if self._statistics.is_done():
                	break
                self._clear()

                self._statistics.step_speeds()

                self._print(self._statistics.get_phase()+"§")
                total_files = self._statistics.get_total_files()
                loaded_files = self._statistics.get_files()
                if total_files != 0:
	                self._print_frame()
	                self._print_fraction("Loaded files",loaded_files, total_files)
	                self._print_fraction("Zipfs",self._statistics.get_zipfs(), loaded_files)
                self._print_speeds()
                self._print_times()

                processes = self._statistics.get_running_processes().items()

                if len(processes)>0:
                    self._print_frame()
                    for name, number in processes:
                        self._print_label("Process %s"%name, number)

                self._print_all()

        except Exception as e:
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            raise

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _print_times(self):
        self._print_frame()
        self._print_label("Remaining zips time", self._statistics.get_remaining_elaboration_time())
        self._print_label("Elapsed time", self._statistics.get_elapsed_time())

    def _print_speeds(self):
    	self._print_speed("Zips speed", self._statistics.get_elaboration_speed())
    	self._print_speed("Loading speed", self._statistics.get_load_speed())

    def _print_speed(self, label, value):
        if value != 0:
            self._print_label("%s speed"%label, "%s url/s"%round(value, 2))

    def _print_fraction(self, label, v1, v2):
        if v2 != 0:
            perc = str(round(v1/v2*100, 1))+"%"

            self._print_label(label, "%s/%s %s"%(
                v1,
                v2,
                perc
            ))

    def _print_frame(self, pos=None):
        self._print("$$$", pos)

    def _print_label(self, label, value, pos=None):
        self._print("%s: § %s"%(label, value), pos)

    def _print(self, value, pos=None):
        if pos == None:
            pos = self._i

        value = "| "+value+" |"

        self._max_len = max(self._max_len, len(value))

        self._outputs.update({
            pos: value
        })
        self._i+=1

    def _print_all(self):
        self._print_frame(0)
        self._print_frame(self._i-1)
        for k, v in self._outputs.items():
            if "| $$$ |" == v:
                v = "| "+("-"*(self._max_len-5))+" |"
            elif "§" in v:
                a, b = v.split("§")
                padding = " "*(self._max_len-len(v))
                v = a+padding+b
            self._stdscr.addstr(k, 0, v)

        self._stdscr.refresh()

    def _clear(self):
        for i in range(self._i):
            self._stdscr.addstr(i, 0, " "*self._max_len)

        self._stdscr.refresh()
        self._i = 1
        self._max_len = 0
        self._outputs = {}

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
