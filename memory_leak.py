from zipf.factories import ZipfFromDir
# from pympler import tracker

#text_factory = ZipfFromText()
dir_factory = ZipfFromDir(use_cli=True)

# text = """Se io fossi fuoco, brucerei il mondo;
# se io fossi vento scatenerei la tempesta su di esso;
# se io fossi acqua, lo sommergerei;
# se io fossi Dio, lo farei sprofondare in un abisso;

# se io fossi Papa, allora sì che sarei allegro,
# poiché metterei nei guai tutti i cristiani;
# se io fossi imperatore, sai cosa farei?
# Taglierei la testa di netto a tutti.

# Se io fossi morte andrei da mio padre,
# se io fossi vita mi allontanerei da lui:
# allo stesso modo mi comporterei con mia madre.

# Se io fossi Cecco, come sono e sono sempre stato,
# prenderei per me le donne giovani e avvenenti,
# e lascerei agli altri quelle vecchie e brutte"""

path = "/Users/lucacappelletti/Documents/zipf_datasets/for_datasets/non_recipes/"

# tr = tracker.SummaryTracker()
# tr.print_diff()
dir_factory.run(path)
# tr.print_diff()
