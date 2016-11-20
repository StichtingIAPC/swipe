import React, { PropTypes } from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';

import { updateSupplier } from '../../actions/suppliers';

import Form from '../forms/Form';
import { StringField, BoolField } from '../forms/fields';

/**
 * Created by Matthias on 17/11/2016.
 */

let SupplierEdit = class extends React.Component {
	update(obj) {
		obj.lastModified = new Date();
		this.props.updateSupplier(obj);
		browserHistory.push(`/supplier/${obj.id}/`);
	}

	render() {
		if (!this.props.supplier) {
			browserHistory.push(`/supplier/`);
			return null;
		}

		const supplier = this.props.supplier;
		return (
			<Form
				original={supplier}
				onSubmit={this.update.bind(this)}
				returnLink={`/supplier/${supplier.id}/`}
				fields={{
					name: StringField,
					notes: StringField,
					deleted: BoolField,
					searchUrl: StringField,
				}}>

				<h3 className="box-title">Edit Supplier {supplier.name}</h3>
			</Form>
		)
	}
};

SupplierEdit.propTypes = {
	params: PropTypes.shape({
		supplierID: PropTypes.string.isRequired,
	}).isRequired,
};

SupplierEdit = connect(
	(state, ownProps) => {
		return {
			...ownProps,
			supplier: Object.values(state.suppliers.objects).find((obj) => obj.id == Number(ownProps.params.supplierID)),
		}
	},
	(dispatch, ownProps) => {
		return {
			...ownProps,
			updateSupplier: (supplier) => dispatch(updateSupplier(supplier)),
		}
	}
)(SupplierEdit);

export {
	SupplierEdit,
}
export default SupplierEdit;
