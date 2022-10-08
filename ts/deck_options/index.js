import DeckOptionsAddon from "./DeckOptionsAddon.svelte";

$deckOptions.then((deckOptions) => {
  deckOptions.addSvelteAddon({ component: DeckOptionsAddon });
});
