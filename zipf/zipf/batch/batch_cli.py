from ..cli import cli

class batch_cli(cli):
    def _update(self):
        self._statistics.step_speeds()

        self._print(self._statistics.get_phase()+"§")
        total_files = self._statistics.get_total_files()

        batches = self._statistics.get_batches()

        if sum(batches.values()):
            self._print_frame()

        for key, value in batches.items():
            if value != 0:
                self._print_fraction(key, value, total_files)

        self._print_speeds()
        self._print_times()

    def _print_times(self):
        self._print_frame()
        self._print_label("Remaining zips time", self._statistics.get_remaining_elaboration_time())
        self._print_label("Elapsed time", self._statistics.get_elapsed_time())

    def _print_speeds(self):
        self._print_speed("Zips", self._statistics.get_elaboration_speed())
