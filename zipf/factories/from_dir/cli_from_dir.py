from ...cli.cli import cli

class cli_from_dir(cli):
    def _update(self):
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

    def _print_times(self):
        self._print_frame()
        self._print_label("Remaining zips time", self._statistics.get_remaining_elaboration_time())
        self._print_label("Elapsed time", self._statistics.get_elapsed_time())

    def _print_speeds(self):
        self._print_speed("Zips speed", self._statistics.get_elaboration_speed())
        self._print_speed("Loading speed", self._statistics.get_load_speed())