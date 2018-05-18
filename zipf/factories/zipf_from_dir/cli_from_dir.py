from ...cli import Cli


class CliFromDir(Cli):
    def _update(self):
        self._statistic.step_speeds()

        self._print(self._statistic.get_phase()+"§")
        total_files = self._statistic.get_total_files()
        zipfs_files = self._statistic.get_zipfs()
        empty_files = self._statistic.get_empty_files()
        empty_lists = self._statistic.get_empty_lists()

        if zipfs_files + empty_files + empty_lists:
            self._print_frame()

        if zipfs_files != 0:
            self._print_fraction("Zipfs", zipfs_files, total_files)
        if empty_files != 0:
            self._print_fraction("Empty files", empty_files, total_files)
        if empty_lists != 0:
            self._print_fraction("Empty word lists", empty_lists, total_files)

        self._print_speeds()
        self._print_times()

    def _print_times(self):
        self._print_frame()
        self._print_label("Remaining zips time",
                          self._statistic.get_remaining_elaboration_time())
        self._print_label("Elapsed time", self._statistic.get_elapsed_time())

    def _print_speeds(self):
        self._print_speed("Zips", self._statistic.get_elaboration_speed())
