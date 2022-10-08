/// <reference types="svelte" />

declare module "*.svg" {
  const content: any;
  export default content;
}

declare function pycmd(cmd: string);
