module.exports = {
  parser: '@typescript-eslint/parser',
  extends: ['next/core-web-vitals', 'plugin:@typescript-eslint/recommended'],
  ignorePatterns: ['next-env.d.ts', '.next/**', 'node_modules/**', 'postcss.config.js'],
  rules: {
    '@next/next/no-html-link-for-pages': 'off',
  },
};
