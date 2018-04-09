import React, { Component } from 'react';

import { Link, Switch, Route } from 'react-router-dom';

import ExternaliseList from './externalise/ExternaliseList';
import ExternaliseAdd from './externalise/ExternaliseAdd';

export default class Externalise extends Component {
	cols = [
		{
			dataField: 'article',
			text: 'Article',
			sort: true,
		},
		{
			dataField: 'memo',
			text: 'Memo',
			sort: false,
		},
		{
			dataField: 'amount',
			text: 'Book value per article',
			sort: false,
		},
		{
			dataField: 'count',
			text: 'Count',
			sort: true,
		},
	];

	render() {
		return (
			<Switch>
				<Route path={`${this.props.match.path}/create`}>
					<div className="row">
						<div className="col-xs-8 col-md-8">
							<ExternaliseList />
						</div>
						<div className="col-xs-4 col-md-4">
							<ExternaliseAdd />
						</div>
					</div>
				</Route>
				<Route path={`${this.props.match.path}`}>
					<ExternaliseList />
				</Route>
			</Switch>
		);
	}
}
