import pkg from './package.json' assert { type: 'json' }

import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import babel from '@rollup/plugin-babel'
import json from '@rollup/plugin-json'

const footer = `
if(typeof window !== 'undefined') {
  window._Dry_VERSION_ = '${pkg.version}'
}`

export default {
  input: './index.js',
  output: [
    {
      file: `./${pkg.main}`,
      format: 'cjs',
      footer,
    },
    {
      file: `./${pkg.module}`,
      format: 'esm',
      footer,
    },
    {
      file: `./${pkg.browser}`,
      format: 'umd',
      name: 'Dry',
      footer,
    },
    {
      file: `./${pkg.iife}`,
      format: 'iife',
      name: 'Dry',
      footer,
    }
  ],
  plugins: [
    json(),
    resolve(),
    babel({ babelHelpers: 'bundled' }),
    commonjs(),
  ],
  external: ["axios"],
}