'use strict';

const path = require('path');
const webpack = require('webpack');

const APP_DIR = path.resolve(path.join(__dirname, 'frontend/src'));
const BUILD_DIR = path.resolve(path.join(__dirname, 'frontend/dist'));

module.exports = {
	entry: path.join(APP_DIR, 'app.js'),
	output: {
		path: BUILD_DIR,
		publicPath: '/dist/',
		filename: 'bundle.js',
	},
	module : {
		loaders : [
			{
				test : /\.jsx?/,
				exclude: /node_modules/,
				loaders: [ 'react-hot', 'babel' ]
			}, {
				test: /\.scss$/,
				loaders: [ 'style', 'css', 'sass' ],
			},
		],
	},
};