const path = require('path');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const RemoveEmptyScriptsPlugin = require('webpack-remove-empty-scripts');
const autoprefixer = require('autoprefixer');

module.exports = {
  entry: {
    main: './src/index.ts',
    styles: '/src/styles.scss',
  },
  output: {
    filename: '[name].[contenthash].js',
    publicPath: '/static/dist/',
    path: path.resolve(__dirname, '..', 'penne', 'static', 'dist'),
    clean: true,
    library: {
      name: 'penne',
      type: 'var',
    },
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [autoprefixer],
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
            },
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new WebpackManifestPlugin(),
    new CleanWebpackPlugin(),
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css',
    }),
    new RemoveEmptyScriptsPlugin(),
    new CssMinimizerPlugin(),
  ],
  devtool: 'source-map',
};
