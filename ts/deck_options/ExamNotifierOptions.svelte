<script lang="ts">
  import PatreonIcon from "./patreon.svg";
  import {
    type AuxData,
    type ExamSettings,
    defaultExamSettings,
  } from "./types";

  export let data: AuxData;

  let dateInput: HTMLInputElement;
  let examSettings: ExamSettings;

  function dateIsValid(epochSeconds: number) {
    return epochSeconds >= Date.now();
  }

  function onDateInputChange(ev: Event) {
    const target = ev.target as HTMLInputElement;
    const epoch_seconds = Math.round(target.valueAsNumber / 1000);
    examSettings["exam_date"] = epoch_seconds;

    if (examSettings.exam_date != epoch_seconds) {
      examSettings.exam_date = epoch_seconds;
    }
  }

  function openLink(key: string) {
    pycmd(`exam_notifier:deck_options:open_link:${key}`);
  }

  function getExamSettings(auxData: AuxData): ExamSettings {
    if (auxData.exam_settings === undefined) {
      auxData.exam_settings = defaultExamSettings();
    }
    let settings = auxData.exam_settings;

    if (settings.exam_date == undefined || !dateIsValid(settings.exam_date)) {
      settings.exam_date = Math.round(Date.now() / 1000);
    }
    return settings as ExamSettings;
  }

  $: examSettings = getExamSettings(data);
  $: if (dateInput) dateInput.valueAsNumber = examSettings.exam_date * 1000;
</script>

<div>
  <h3>Exam Notifier</h3>
  <div>
    <input
      id="en-exam-enabled"
      type="checkbox"
      bind:checked={examSettings["enabled"]}
    />
    <label for="en-exam-enabled">Enable exam notifications for this deck</label>
  </div>
  <div id="en-main-inputs" class:disabled={!examSettings["enabled"]}>
    <div class="en-row">
      <label for="en-exam-name">Exam name</label>
      <input
        id="en-exam-name"
        type="text"
        disabled={!examSettings["enabled"]}
        bind:value={examSettings["exam_name"]}
      />
    </div>
    <div class="en-row">
      <label for="en-exam-date">Exam date</label>
      <input
        id="en-exam-date"
        type="date"
        bind:this={dateInput}
        disabled={!examSettings["enabled"]}
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
        on:click={() => openLink("glutanimate")}
      >
        <span class="en-icon"><PatreonIcon /></span>
        <span>Glutanimate</span>
      </button>
      <button
        id="en-btn-anking"
        class="btn"
        title="Become a Patron and receive exclusive content by the AnKing team!"
        on:click={() => openLink("anking")}
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
  .en-buttons button {
    flex: 1 1;

    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  button {
    background-color: white;
    border: 1px solid #ced4da;
  }
  :global(.night-mode) button {
    background-color: #3a3a3a;
    border: 1px solid #777;
  }
  button:hover {
    background-color: #f5f5f5;
  }
  :global(.night-mode) button:hover {
    background-color: #525252;
  }
</style>
