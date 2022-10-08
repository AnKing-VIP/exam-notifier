const { build } = require("esbuild");
const sveltePreprocess = require("svelte-preprocess");
const sveltePlugin = require("esbuild-svelte");

const production = process.env.NODE_ENV === "production";
const development = process.env.NODE_ENV === "development";

const watch = development
  ? {
      onRebuild(error) {
        console.timeLog;

        if (error) {
          console.error(
            new Date(),
            "esbuild: build failed:",
            error.getMessage()
          );
        } else {
          console.log(new Date(), "esbuild: build succeeded");
        }
      },
    }
  : false;

/**
 * This should point to all entry points for JS add-ons.
 */
const entryPoints = ["ts/deck_options/index.js"];

/**
 * Esbuild build options
 * See https://esbuild.github.io/api/#build-api for more
 */
const options = {
  entryPoints,
  outfile: "./src/exam_notifier/web/deck_options.js",
  format: "iife",
  target: "es6",
  bundle: true,
  treeShaking: production,
  sourcemap: !production,
  minify: production,
  pure: production ? ["console.log", "console.time", "console.timeEnd"] : [],
  watch,
  external: ["svelte"],
  plugins: [
    sveltePlugin({
      compilerOptions: { css: true },
      preprocess: sveltePreprocess(),
      include: /\.(?:svelte)|(?:svg)$/,
    }),
  ],
};

build(options).catch((err) => {
  console.error(err);
  process.exit(1);
});

if (watch) {
  console.log("Watching for changes...");
}
