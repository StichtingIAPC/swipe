import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import FontAwesome from '../tools/icons/FontAwesome';
import { fetchSupplier, newSupplier } from '../../state/suppliers/actions';
import { getSupplierActiveObject } from "../../state/suppliers/selector";

class SupplierDetail extends React.Component {
	trash(evt) {
		evt.preventDefault();
	}

	componentDidMount() {
		this.props.fetchSupplier(this.props.match.params.supplierID);
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
								<a onClick={::this.trash} className="btn btn-danger btn-sm" title="Delete"><FontAwesome icon="trash" /></a>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{[ 'id', 'name', 'deleted', 'notes', 'search_url' ].map(
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
	state => ({
		supplier: getSupplierActiveObject(state),
	}),
	{
		fetchSupplier,
		newSupplier,
	}
)(SupplierDetail);
