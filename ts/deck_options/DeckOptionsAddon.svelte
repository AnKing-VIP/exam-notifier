<script lang="ts">
  import {
    type AuxData,
    type ExamSettings,
    defaultExamSettings,
  } from "./types";

  import ExamNotifierOptions from "./ExamNotifierOptions.svelte";

  export let data: AuxData;

  let examSettings: ExamSettings;

  function getExamSettings(auxData: AuxData): ExamSettings {
    if (auxData.exam_settings === undefined) {
      auxData.exam_settings = defaultExamSettings();
    }
    let settings = auxData.exam_settings;
    const now = Date.now() / 1000;

    if (settings.exam_date === undefined || settings.exam_date < now) {
      settings.exam_date = now;
    }

    return settings as ExamSettings;
  }

  function onExamSettingsChange(settings: ExamSettings) {
    // if data was already updated this tick, update isn't re-triggered.
    // So there is no infinite loop.
    data = data;
  }

  $: examSettings = getExamSettings(data);
  $: onExamSettingsChange(examSettings);
</script>

<ExamNotifierOptions bind:examSettings />
