module.exports = {
    root: true,
    plugins: ["jest"],
    env: {
        node: true,
        "jest/globals": true,
    },
    extends: [
        "eslint:recommended",
        "plugin:vue/essential",
        "prettier",
        "plugin:jest/all",
    ],
    parserOptions: {
        parser: "babel-eslint",
    },
};
