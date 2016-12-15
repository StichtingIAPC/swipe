import React, {PropTypes} from "react";
import {connect} from "react-redux";
import {updateSupplier} from "../../actions/suppliers";
import Form from "../forms/Form";
import {StringField} from "../forms/fields";

/**
 * Created by Matthias on 17/11/2016.
 */

class SupplierEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			supplier: this.props.supplier,
			workingCopy: {...this.props.supplier},
		}
	}

	update(evt) {
		evt.preventDefault();
		const obj = this.state.workingCopy;
		obj.lastModified = new Date();
		this.props.updateSupplier(obj);
	}

	reset(evt) {
		evt.preventDefault();
		this.setState({workingCopy: {...this.state.supplier}});
	}

	componentWillReceiveProps(nextProps) {
		if (this.state.supplier != nextProps.supplier) {
			this.setState({
				supplier: nextProps.supplier,
				workingCopy: {
					name: "",
					notes: "",
					searchUrl: "",
					...nextProps.supplier,
				},
			})
		}
	}

	render() {
		if (!this.props.supplier) {
			return null;
		}

		const updateValue = (key) =>
			(evt) => this.setState({workingCopy: {
				...this.state.workingCopy,
				[key]: evt.target.value,
			}});

		const supplier = this.state.workingCopy;
		return (
			<Form
				title={`Edit ${supplier.name}`}
				onSubmit={this.update.bind(this)}
				onReset={this.reset.bind(this)}
				returnLink={`/supplier/${supplier.id}/`}>
				<StringField onChange={updateValue('name')} name="Name" value={supplier.name} />
				<StringField onChange={updateValue('notes')} name="Notes" value={supplier.notes} />
				<StringField onChange={updateValue('searchUrl')} name="Search url" value={supplier.searchUrl} />
			</Form>
		)
	}
}

SupplierEdit.propTypes = {
	params: PropTypes.shape({
		supplierID: PropTypes.string.isRequired,
	}).isRequired,
	supplier: PropTypes.shape({
		name: PropTypes.string.isRequired,
		notes: PropTypes.string,
		searchUrl: PropTypes.string,
	}),
};

export default connect(
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
