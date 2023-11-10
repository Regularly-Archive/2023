import serve from 'rollup-plugin-serve';
import babel from '@rollup/plugin-babel'

export default {
  input: 'dist/edge-tts.iife.js',
  output: [
    {
      file: 'dist/bundle.js',
      format: 'umd',
      name: 'Dry'
    }
  ],
  plugins: [
    babel({ babelHelpers: 'bundled' }),
    serve({
      contentBase: ['dist'],
      port: 9527
    })
  ]
}