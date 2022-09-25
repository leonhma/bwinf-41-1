const HTMLWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const WasmPackPlugin = require("@wasm-tool/wasm-pack-plugin");
const SveltePreprocess = require("svelte-preprocess");
const path = require("path");

module.exports = (env) => {
  const mode = env.mode || "development";
  const prod = mode === "production";

  return {
    entry: path.resolve(__dirname, "./src/index.ts"),
    mode,
    devtool: prod ? false : "eval-source-map",
    resolve: {
      extensions: [".ts", ".svelte", ".mjs", ".js"],
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          use: "ts-loader",
          exclude: /node_modules/,
        },
        {
          test: /\.(ico)$/,
          type: "asset/resource",
        },
        {
          test: /\.svelte$/,
          use: {
            loader: "svelte-loader",
            options: {
              preprocess: SveltePreprocess(),
              compilerOptions: {
                dev: !prod,
              },
              emitCss: prod,
            },
          },
        },
        {
          test: /\.css$/,
          use: [MiniCssExtractPlugin.loader, "css-loader"],
        },
        {
          // required to prevent errors from Svelte on Webpack 5+
          test: /node_modules\/svelte\/.*\.mjs$/,
          resolve: {
            fullySpecified: false,
          },
        },
        {
          test: /\.m?js$/,
          resolve: {
            fullySpecified: false,
          },
        },
      ],
    },
    experiments: {
      asyncWebAssembly: true,
    },
    output: {
      path: path.resolve(__dirname, "./dist"),
      publicPath: prod ? "/gL5WY3fPt751WfPpougU/" : "/",
      chunkFilename: "[id].chunk.js",
      clean: true,
    },
    plugins: [
      new HTMLWebpackPlugin({ publicPath: prod ? "/gL5WY3fPt751WfPpougU/" : "/" }),
      new MiniCssExtractPlugin(),
      new CopyPlugin({
        patterns: ["public/"],
      }),
      new WasmPackPlugin({
        crateDirectory: path.resolve(__dirname, "."),
      }),
    ],
    ignoreWarnings: [
      /size limit [^]*module\.wasm/, // ignore size warnings for wasm files
    ],
    devServer: {
      hot: true,
      client: {
        logging: "none",
        progress: true,
      },
      watchFiles: [
        "src",
        "cargo.toml",
        "declaration.d.ts",
        "package.json",
        "tsconfig.json",
      ],
    },
  };
};
