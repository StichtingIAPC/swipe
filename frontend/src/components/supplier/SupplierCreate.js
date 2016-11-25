import React from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';

import { createSupplier } from '../../actions/suppliers';

import Form from '../forms/Form';
import { StringField, BoolField } from '../forms/fields';

import FA from '../tools/FontAwesome';

/**
 * Created by Matthias on 17/11/2016.
 */

let SupplierCreate = class extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			workingCopy: {
				name: '',
				notes: '',
				searchUrl: '',
			},
		}
	}

	reset(evt) {
		evt.preventDefault();
		this.state = {
			workingCopy: {
				name: '',
				notes: '',
				searchUrl: '',
			},
		}
	}

	async create(evt) {
		evt.preventDefault();
		const obj = this.state.workingCopy;
		obj.lastModified = new Date();
		await this.props.addSupplier(obj);
		browserHistory.push(`/supplier/${obj.id}/`);
	}

	render() {
		const updateValue = (key) =>
			(evt) => this.setState({workingCopy: {
				...this.state.workingCopy,
				[key]: evt.target.value,
			}});

		return (
			<Form
				title="Create supplier"
				onSubmit={this.create.bind(this)}
				onReset={this.reset.bind(this)}
				returnLink={`/supplier/`}>
				<StringField onChange={updateValue('name')} name="Name" />
				<StringField onChange={updateValue('notes')} name="Notes" />
				<StringField onChange={updateValue('searchUrl')} name="Search Url" />
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
			addSupplier: async (arg) => dispatch(createSupplier(arg)),
		};
	}
)(SupplierCreate);


export {
	SupplierCreate,
}

export default SupplierCreate;
