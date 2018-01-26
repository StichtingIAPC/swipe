import React, { Component } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import FontAwesome from '../tools/icons/FontAwesome';

import { fetchAll as fetchAllExternalisations } from '../../state/logistics/externalise/actions';

class Externalise extends Component {
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
			text: 'Amount',
			sort: true,
		},
		{
			dataField: 'count',
			text: 'Count',
			sort: true,
		},
	];

	componentWillMount() {
		this.props.fetchExternalisations();
	}

	render() {
		return (
			<div className="row">
				<div className="col-md-1">
					<div className="box">
						<div className="box-header">
							<div className="box-title">
								Externalisations
							</div>
							<div className="box-tools">
								<div className="btn-group">
									<a
										className={`btn btn-sm btn-default ${this.props.loading ? 'disabled' : ''}`}
										title="Refresh"
										onClick={this.props.fetchExternalisations}>
										<FontAwesome icon={`refresh ${this.props.loading ? 'fa-spin' : ''}`} />
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
							<BootstrapTable
								keyField="id"
								columns={this.cols}
								data={this.props.externalises} />
						</div>
					</div>
				</div>
			</div>
		);
	}
}

export default connect(
	state => ({
		externalises: state.logistics.externalise.externalisations,
		loading: state.logistics.externalise.loading,
	}),
	{ fetchExternalisations: fetchAllExternalisations }
)(Externalise);
