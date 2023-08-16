import type { Config } from "tailwindcss";
const defaultTheme = require("tailwindcss/defaultTheme");

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    fontFamily: {
      mono: ["AnonPro", ...defaultTheme.fontFamily.mono],
    },
    extend: {
      colors: {
        primary: "rgba(var(--color-primary), 0.8)",
      },
    },
  },
  plugins: [],
};

export default config;
