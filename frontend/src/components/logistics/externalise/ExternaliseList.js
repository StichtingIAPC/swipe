import React, { Component } from 'react';
import MoneyAmount from '../../money/MoneyAmount';
import { Link } from 'react-router-dom';
import FontAwesome from '../../tools/icons/FontAwesome';
import { connect } from 'react-redux';
import { fetchAllAction as fetchAllExternalisations } from '../../../state/logistics/externalise/actions';
import {
	getExternalisationData,
	getExternalisationLoading,
	getExternalisationPopulated
} from "../../../state/logistics/externalise/selectors";

class List extends Component {
	componentWillMount() {
		if (!this.props.isPopulated && !this.props.isLoading) {
			this.props.fetchExternalisations();
		}
	}

	render() {
		return <div className="box">
			<div className="box-header">
				<div className="box-title">
					Externalisations
				</div>
				<div className="box-tools">
					<div className="btn-group">
						<a
							className={`btn btn-sm btn-default ${this.props.isLoading ? 'disabled' : ''}`}
							title="Refresh"
							onClick={this.props.fetchExternalisations}>
							<FontAwesome icon={`refresh ${this.props.isLoading ? 'fa-spin' : ''}`} />
						</a>
						<Link
							className="btn btn-default btn-sm"
							to="/logistics/externalise/create/"
							title="Create new register">
							<FontAwesome icon="plus" />
						</Link>
					</div>
				</div>
			</div>
			<div className="box-body">
				<table className="table">
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
									<td>{ extl.article.name }</td>
									<td>{ extl.memo }</td>
									<td><MoneyAmount money={extl.amount} /></td>
									<td>{ extl.count }</td>
								</tr>
							))
						}
					</tbody>
				</table>
			</div>
		</div>;
	}
}

export default connect(
	state => ({
		externalises: getExternalisationData(state),
		isLoading: getExternalisationLoading(state),
		isPopulated: getExternalisationPopulated(state),
	}),
	{ fetchExternalisations: fetchAllExternalisations }
)(List);
