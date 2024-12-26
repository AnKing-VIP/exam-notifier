import { mount } from "svelte";
import { get } from "svelte/store";

import DeckOptionsAddon from "./DeckOptionsAddon.svelte";

$deckOptions.then((deckOptions) => {
    deckOptions.addHtmlAddon("", () => {});
    setTimeout(() => {
        let target = null;
        for (const h1 of document.querySelectorAll("h1")) {
            if (h1.textContent === "Add-ons") {
                target = h1.parentElement;
                break;
            }
        }
        mount(DeckOptionsAddon, {
            target: target,
            props: { data: get(deckOptions.auxData()) },
        });
    }, 100);
});
