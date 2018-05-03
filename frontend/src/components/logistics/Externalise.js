import React, { Component } from 'react';

import { Route, Switch } from 'react-router-dom';

import ExternaliseList from './externalise/ExternaliseList';
import ExternaliseAdd from './externalise/ExternaliseAdd';
import { Col, Row } from 'react-bootstrap';

export default class Externalise extends Component {


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
