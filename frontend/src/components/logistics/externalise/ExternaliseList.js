import React, { Component } from 'react';
import MoneyAmount from '../../money/MoneyAmount';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome';
import { connect } from 'react-redux';
import { fetchAllAction as fetchAllExternalisations } from '../../../state/logistics/externalise/actions';
import { Button, ButtonGroup, Table } from 'react-bootstrap';
import { Box } from 'reactjs-admin-lte';

class List extends Component {
	componentWillMount() {
		if (!this.props.populated && !this.props.loading) {
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
							disabled={this.props.loading}>
							<FontAwesome icon={`refresh ${this.props.loading ? 'fa-spin' : ''}`} />
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
		externalises: state.logistics.externalise.externalisations,
		loading: state.logistics.externalise.loading,
		populated: state.logistics.externalise.populated,
	}),
	{ fetchExternalisations: fetchAllExternalisations },
)(List);
