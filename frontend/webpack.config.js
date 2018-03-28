'use strict';

const path = require('path');
const webpack = require('webpack');

const APP_DIR = path.resolve(path.join(__dirname, 'src'));
const BUILD_DIR = path.resolve(path.join(__dirname, 'public', 'dist'));

let replacements = {};

try {
	// eslint-disable-next-line global-require
	replacements = require(path.resolve(path.join(APP_DIR, 'config.local')));
} catch (e) { console.log('No config.local.js found, continueing on without changing any settings')}

const defaults = {
	'__BACKEND_URL__': '`//${window.location.hostname}:8000`',
	'process.env': {
		NODE_ENV: JSON.stringify('develop'),
	},
};


module.exports = {
	entry: [
		path.join(APP_DIR, 'app.js'),
	],
	output: {
		path: BUILD_DIR,
		publicPath: '/dist/',
		filename: 'bundle.js',
	},
	devtool: 'inline-source-map',
	module: {
		rules: [
			{
				test: /\.jsx?/,
				exclude: /node_modules/,
				loaders: [ 'babel-loader' ],
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
	plugins: [
		new webpack.DefinePlugin(Object.assign({}, defaults, replacements)),
	],
	resolve: {
		modules: [ 'node_modules' ],
	},
	devServer: {
		headers: { "Access-Control-Allow-Origin": "*" },
		contentBase: './public/',
	},
};
