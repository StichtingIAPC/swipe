import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import FontAwesome from '../tools/icons/FontAwesome';

class SupplierDetail extends React.Component {
	static propTypes = {
		params: PropTypes.shape({
			supplierID: PropTypes.string.isRequired,
		}).isRequired,
	};

	trash(evt) {
		evt.preventDefault();
	}

	render() {
		if (!this.props.supplier) {
			return null;
		}


		const { supplier } = this.props;

		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Supplier: {supplier.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to="/supplier/" className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>
								<Link to={`/supplier/${supplier.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
								<Link onClick={::this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{[ 'id', 'name', 'deleted', 'notes', 'searchUrl' ].map(
							key => (
								<div key={key}>
									<dt>{key}</dt>
									<dd>{String(supplier[key])}</dd>
								</div>
							)
						)}
					</dl>
				</div>
			</div>
		);
	}
}

export default connect(
	(state, ownProps) => ({
		...ownProps,
		supplier: state.suppliers.suppliers.filter(s => +s.id === parseInt(ownProps.params.supplierID || '-1', 10))[0],
	})
)(SupplierDetail);
