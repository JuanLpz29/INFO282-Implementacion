import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'
const path = require("path");

// https://vitejs.dev/config/
export default defineConfig({
    base: path.resolve(__dirname, "./dist/"),
    plugins: [
        vue({
            template: { transformAssetUrls }
        }),

        quasar({
            sassVariables: 'src/quasar-variables.sass'
        })
    ]
});
