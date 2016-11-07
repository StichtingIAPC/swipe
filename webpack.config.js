'use strict';

const path = require('path');
const webpack = require('webpack');

const APP_DIR = path.resolve(path.join(__dirname, 'frontend', 'src'));
const BUILD_DIR = path.resolve(path.join(__dirname, 'frontend', 'dist'));

// we place our resources in the {app}/static folder,
// {app} is specified here such that it can be found by webpack and imported.
const apps = [
	'article',
	'assortment',
	'frontend',
	'money',
	'register',
	'tools',
	'www',
];

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
			}, {
				test: /\.css$/,
				loaders: [ 'style', 'css' ],
			}, {
				test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "url-loader?limit=10000&mimetype=application/font-woff"
			}, {
				test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "file-loader"
			},
			{
				test: /\.(jpg|jpeg|png|gif|svg)$/,
				loader: "file-loader"
			},
		],
	},
	resolve: {
		root: [].concat(
			apps.map(
				app => path.join(__dirname, app, 'static')
			)
		),
	},
	sassLoader: {
		includePaths: apps.map(
			app => path.join(__dirname, app, 'static')
		)
	},
	devtool: 'cheap-module-source-map',
};
