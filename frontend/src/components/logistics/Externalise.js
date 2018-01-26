import React, { Component } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import { connect } from 'react-redux';

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
		return <BootstrapTable
			keyField="id"
			columns={this.cols}
			data={this.props.externalises} />;
	}
}

export default connect(
	state => ({ externalises: state.logistics.externalise.externalisations }),
	{ fetchExternalisations: fetchAllExternalisations }
)(Externalise);
