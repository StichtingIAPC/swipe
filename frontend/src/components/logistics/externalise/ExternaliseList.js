import React, { Component } from 'react';
import MoneyAmount from '../../money/MoneyAmount';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome';
import { connect } from 'react-redux';
import { fetchAllExternalizesStart as fetchAllExternalisations } from '../../../state/logistics/externalise/actions';
import {
	getExternalisationData,
	getExternalisationLoading,
	getExternalisationPopulated
} from "../../../state/logistics/externalise/selectors";
import { Button, ButtonGroup, Table } from 'react-bootstrap';
import { Box } from 'reactjs-admin-lte';

class List extends Component {
	componentWillMount() {
		if (!this.props.isPopulated && !this.props.isLoading) {
			this.props.fetchExternalisations();
		}
	}

	render() {
		// eslint-disable-next-line react/style-prop-object
		return <Box style="primary">
			<Box.Header>
				<Box.Title>
					Externalisations
				</Box.Title>
				<Box.Tools>
					<ButtonGroup>
						<Button
							bsSize="small"
							title="Refresh"
							onClick={this.props.fetchExternalisations}
							disabled={this.props.isLoading}>
							<FontAwesome icon={`refresh ${this.props.isLoading ? 'fa-spin' : ''}`} />
						</Button>
						<Link
							className="btn btn-default btn-sm"
							to="/logistics/externalise/create/"
							title="Create new externalisation">
							<FontAwesome icon="plus" />
						</Link>
					</ButtonGroup>
				</Box.Tools>
			</Box.Header>
			<Box.Body>
				<Table responsive striped hover>
					<thead>
						<tr>
							<th>Article</th>
							<th>Memo</th>
							<th>Book price</th>
							<th>Count</th>
						</tr>
					</thead>
					<tbody>
						{
							this.props.externalises.map(extl => (
								<tr key={extl.article.id + extl.memo}>
									<td>{extl.article.name}</td>
									<td>{extl.memo}</td>
									<td><MoneyAmount money={extl.amount} /></td>
									<td>{extl.count}</td>
								</tr>
							))
						}
					</tbody>
				</Table>
			</Box.Body>
		</Box>;
	}
}

export default connect(
	state => ({
		externalises: getExternalisationData(state),
		isLoading: getExternalisationLoading(state),
		isPopulated: getExternalisationPopulated(state),
	}),
	{ fetchExternalisations: fetchAllExternalisations },
)(List);
