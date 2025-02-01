<script lang="ts">
   import type { Writable } from "svelte/store";
   import {onMount} from "svelte";

   import {
     type AuxData,
     type ExamSettings,
     defaultExamSettings,
   } from "./types";

   import ExamNotifierOptions from "./ExamNotifierOptions.svelte";

   export let data: Writable<AuxData>;

   let examSettings: ExamSettings = getExamSettings($data);

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
     data.update((d) => {
       d.exam_settings = settings;
       return d;
     });
   }

   $: onExamSettingsChange(examSettings);

   onMount(() => {
     data.subscribe((d) => {
       examSettings = getExamSettings(d);
     });
   });
 </script>
<ExamNotifierOptions bind:examSettings />
