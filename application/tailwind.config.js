/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      textColor: {
        icon: "var(--color-icons)",
      },
      backgroundColor: {
        oceans: "var(--bg-oceans)",
        "primary-gray": "var(--bg-primary-gray)",
        "dark-gray": "var(--bg-dark-gray)",
        "lighter-black": "var(--bg-lighter-black)",
        "darker-gray": "var(--bg-darker-gray)",
        "lighter-gray": "var(--bg-lighter-gray)",
        "light-black": "var(--bg-light-black)",
        "second-table": "var(--bg-second-table)",
        "dark-blue": "var(--bg-dark-blue)",
      },
    },
  },
  plugins: [require("daisyui")],
};
