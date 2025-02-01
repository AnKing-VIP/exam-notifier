import * as fs from "fs";
import { env } from "process";

import * as esbuild from "esbuild";
import { sveltePreprocess } from "svelte-preprocess";
import sveltePlugin from "esbuild-svelte";

for (const dir of ["../dist", "../dist/web"]) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir);
    }
}


const production = env.NODE_ENV === "production";
const watch = env.WATCH === "true";


const entryPoints = ["ts/deck_options/index.js"];

const options = {
    entryPoints,
    outfile: "./src/exam_notifier/web/deck_options.js",
    format: "iife",
    target: ["es6", "chrome77"],
    bundle: true,
    minify: production,
    treeShaking: production,
    sourcemap: !production,
    pure: production ? ["console.log", "console.time", "console.timeEnd"] : [],
    plugins: [
      sveltePlugin({
        compilerOptions: { css: 'injected'},
        preprocess: sveltePreprocess(),
      }),
    ],
    loader: { ".svg": "text" },
};

const context = await esbuild.context(options);

if (watch) {
    console.log("Watching for changes...");
    await context.watch();
}
else {
    await context.rebuild();
    context.dispose();
}
