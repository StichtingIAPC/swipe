import React, { Component } from 'react';

import { Route, Switch } from 'react-router-dom';

import ExternaliseList from './externalise/ExternaliseList';
import ExternaliseAdd from './externalise/ExternaliseAdd';
import { Col, Row } from 'react-bootstrap';

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
					<Row>
						<Col xs={8} md={8}>
							<ExternaliseList />
						</Col>
						<Col xs={4} md={4}>
							<ExternaliseAdd />
						</Col>
					</Row>
				</Route>
				<Route path={`${this.props.match.path}`}>
					<ExternaliseList />
				</Route>
			</Switch>
		);
	}
}
