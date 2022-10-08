import ExamNotifierOptions from "./ExamNotifierOptions.svelte";

$deckOptions.then((deckOptions) => {
  deckOptions.addSvelteAddon({ component: ExamNotifierOptions });
});
