import React, { PropTypes } from 'react'
import { Link, browserHistory } from 'react-router'
import { connect } from 'react-redux';

import FA from '../tools/FontAwesome'
/**
 * Created by Matthias on 17/11/2016.
 */

let SupplierDetail = class extends React.Component {
	trash(evt) {
		evt.preventDefault();
	}

	render() {
		if (!this.props.supplier) {
			browserHistory.push(`/supplier/`);
			return null;
		}

		const supplier = this.props.supplier;
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Supplier: {supplier.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to={`/supplier/${supplier.id}/edit`} className="btn btn-default btn-sm" title="Edit"><FA icon="edit" /></Link>
								<Link onClick={this.trash.bind(this)} className="btn btn-danger btn-sm" title="Delete"><FA icon="trash" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{['id', 'name', 'deleted', 'notes', 'searchUrl'].map(
							(key) => (
								<div key={key}>
									<dt>{key}</dt>
									<dd>{String(supplier[key])}</dd>
								</div>
							)
						)}
					</dl>
				</div>
			</div>
		)
	}
};

SupplierDetail.propTypes = {
	params: PropTypes.shape({
		supplierID: PropTypes.string.isRequired,
	}).isRequired,
};

SupplierDetail = connect(
	(state, ownProps) => {
		return {
			...ownProps,
			supplier: Object.values(state.suppliers.objects).find((obj) => obj.id == Number(ownProps.params.supplierID)),
		}
	})(SupplierDetail);


export {
	SupplierDetail,
}

export default SupplierDetail;
