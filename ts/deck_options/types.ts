export interface AuxData {
  exam_settings?: ExamSettingsRaw;
}

export interface ExamSettingsRaw {
  enabled: boolean;
  exam_name: string;
  // unix epoch in seconds
  exam_date?: number;
}

export interface ExamSettings extends ExamSettingsRaw {
  exam_date: number;
}

export function defaultExamSettings(): ExamSettings {
  return {
    enabled: false,
    exam_name: "",
    exam_date: new Date().getUTCSeconds(),
  };
}
