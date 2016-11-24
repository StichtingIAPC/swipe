import React from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';

import { addSupplier } from '../../actions/suppliers';

import Form from '../forms/Form';
import { StringField, BoolField } from '../forms/fields';

import FA from '../tools/FontAwesome';

/**
 * Created by Matthias on 17/11/2016.
 */

let SupplierCreate = class extends React.Component {
	async create(obj) {
		obj.lastModified = new Date();
		await this.props.addSupplier(obj);
		browserHistory.push(`/supplier/${obj.id}/`);
	}

	render() {
		return (
			<Form
				original={{}}
				onSubmit={this.create.bind(this)}
				returnLink={`/supplier/`}
				fields={{
					name: StringField,
					notes: StringField,
					deleted: BoolField,
					searchUrl: StringField,
				}}>

				<h3 className="box-title">Create supplier</h3>
			</Form>
		)
	}
};

SupplierCreate.propTypes = {};

SupplierCreate = connect(
	(state, ownProps) => {
		return {
			...ownProps,
		}
	},
	(dispatch, ownProps) => {
		return {
			...ownProps,
			addSupplier: async (arg) => dispatch(addSupplier(arg)),
		};
	}
)(SupplierCreate);


export {
	SupplierCreate,
}

export default SupplierCreate;
