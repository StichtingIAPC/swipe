'use strict';

const path = require('path');

const APP_DIR = path.resolve(path.join(__dirname, 'frontend', 'src'));
const BUILD_DIR = path.resolve(path.join(__dirname, 'frontend', 'dist'));

module.exports = {
	entry: [
		'babel-polyfill',
		path.join(APP_DIR, 'app.js'),
	],
	output: {
		path: BUILD_DIR,
		publicPath: '/dist/',
		filename: 'bundle.js',
	},
	module: {
		rules: [
			{
				test: /\.jsx?/,
				exclude: /node_modules/,
				loaders: [ 'react-hot-loader/webpack', 'babel-loader' ],
			}, {
				test: /\.scss$/,
				loaders: [ 'style-loader', 'css-loader', 'sass-loader' ],
			}, {
				test: /\.css$/,
				loaders: [ 'style-loader', 'css-loader' ],
			}, {
				test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "url-loader?limit=10000&mimetype=application/font-woff",
			}, {
				test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "file-loader",
			},
			{
				test: /\.(jpg|jpeg|png|gif|svg)$/,
				loader: "file-loader",
			},
		],
	},
	resolve: {
		modules: [ 'node_modules', APP_DIR ],
	},
	//devtool: 'cheap-module-source-map',
	devServer: {
		headers: { "Access-Control-Allow-Origin": "*" },
	},
};