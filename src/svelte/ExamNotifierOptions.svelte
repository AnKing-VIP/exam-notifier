<script lang="ts">
  import PatreonIcon from "./patreon.svg";

  interface AddonData {
    enabled: boolean;
    exam_name: string;
    // unix epoch in seconds
    exam_date: number;
  }

  export let data: Record<string, unknown>;

  let dateInput: HTMLInputElement;
  let addonData: AddonData;
  // exam_date:

  function onDateInputChange(ev: Event) {
    const target = ev.target as HTMLInputElement;
    const epoch_seconds = Math.round(target.valueAsNumber / 1000);
    addonData["exam_date"] = epoch_seconds;

    if (addonData["exam_date"] != epoch_seconds) {
      addonData["exam_date"] = epoch_seconds;
    }
  }

  $: addonData = data["exam_settings"] as AddonData;
  $: if (dateInput) dateInput.valueAsNumber = addonData["exam_date"] * 1000;
</script>

<div>
  <h3>Exam Notifier</h3>
  <div>
    <input
      id="en-exam-enabled"
      type="checkbox"
      bind:checked={addonData["enabled"]}
    />
    <label for="en-exam-enabled">Enable exam notifications for this deck</label>
  </div>
  <div id="en-main-inputs">
    <div class="en-row">
      <label for="en-exam-name">Exam name</label>
      <input
        id="en-exam-name"
        type="text"
        bind:value={addonData["exam_name"]}
      />
    </div>
    <div class="en-row">
      <label for="en-exam-date">Exam date</label>
      <input
        id="en-exam-date"
        type="date"
        bind:this={dateInput}
        on:input={onDateInputChange}
      />
    </div>
  </div>
  <div>
    <p>
      Hi there :) ! Enjoy <b>Exam Notifier</b>? Then please consider supporting
      our work, so we can keep working on projects like this:
    </p>
    <div class="en-buttons">
      <button
        id="en-btn-glutanimate"
        class="btn"
        title="Become a Patron and receive exclusive content by the AnKing team!"
      >
        <span class="en-icon"><PatreonIcon /></span>
        <span>Glutanimate</span>
      </button>
      <button
        id="en-btn-anking"
        class="btn"
        title="Become a Patron and receive exclusive content by the AnKing team!"
      >
        <span class="en-icon"><PatreonIcon /></span>
        <span>AnKing</span>
      </button>
    </div>
    <p>
      Each contribution is greatly appreciated and will help us
      <b>update and improve</b> Exam Notifier as time goes by. Thank you!
    </p>
  </div>
</div>

<style>
  h3 {
    border-bottom: 1px solid #b6b6b6;
  }
  :global(.night-mode) h3 {
    border-bottom: 1px solid #444;
  }
  #en-main-inputs {
    padding: 16px;
    margin-bottom: 24px;
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0.15);
  }
  :global(.night-mode) #en-main-inputs {
    background-color: rgba(255, 255, 255, 0.1);
  }
  #en-main-inputs:global(.disabled) {
    filter: opacity(0.75);
    backdrop-filter: opacity(0.9);
  }
  .en-row {
    margin: 4px 0;
    display: flex;
  }
  .en-row label {
    min-width: 8em;
  }
  .en-row input {
    flex: 0 1 300px;
  }
  .en-buttons {
    max-width: 360px;
    display: flex;
    justify-content: space-between;
    gap: 16px;
    margin: 18px auto;
  }
  .en-buttons > button {
    flex: 1 1;

    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;

    background-color: white;
    border: 1px solid #ced4da;
  }
  :global(.night-mode) .en-buttons > button {
    background-color: #3a3a3a;
    border: 1px solid #777;
  }
  .en-buttons > button:hover {
    backdrop-filter: brightness(0.9);
  }
  :global(.night-mode) .en-buttons > button:hover {
    backdrop-filter: brightness(1.1);
  }
</style>
