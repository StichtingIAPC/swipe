import React from 'react';
import { connect } from 'react-redux';
import { createSupplier, updateSupplier } from '../../state/suppliers/actions.js';
import Card from '../base/Card';
import Form from '../forms/Form';
import { StringField } from '../forms/fields';
import { fetchSupplier, newSupplier, setSupplierField } from '../../state/suppliers/actions';
import { Button, ButtonToolbar, ControlLabel, FormControl, FormGroup, HelpBlock } from 'react-bootstrap';
import { getSupplierActiveObject, getSupplierValidations } from '../../state/suppliers/selector';
import { hasError } from '../../tools/validations/validators';

class SupplierEdit extends React.Component {
	componentWillMount() {
		if (this.props.match.params.supplierID) {
			this.props.fetchSupplier(this.props.match.params.supplierID);
		} else {
			this.props.newSupplier();
		}
	}

	componentWillReceiveProps({ match }) {
		if (this.props.match.params.supplierID !== match.params.supplierID) {
			if (Number.isNaN(+match.params.supplierID)) {
				this.props.newSupplier();
			} else {
				this.props.fetchSupplier(match.params.supplierID);
			}
		}
	}

	submit = evt => {
		evt.preventDefault();
		console.log(this.props.supplier.id);
		if (this.props.supplier.id === null) {
			this.props.createSupplier(this.props.supplier);
		} else {
			this.props.updateSupplier(this.props.supplier);
		}
	};

	reset = () => {
		if (this.props.supplier.id === null) {
			this.props.newSupplier();
		} else {
			this.props.fetchSupplier(this.props.supplier.id);
		}
	};

	setName = ({ target: { value }}) => this.props.setSupplierField('name', value);
	setNotes = ({ target: { value }}) => this.props.setSupplierField('notes', value);
	setSearch_url = ({ target: { value }}) => this.props.setSupplierField('search_url', value);

	render() {
		const { supplier } = this.props;
		const NEW = supplier.id === null;

		const validation_name = this.props.validations ? this.props.validations['name'] : {};
		const nameValidation = validation_name ? validation_name.text : '';
		const nameErrorType = validation_name ? validation_name.type : 'success';

		const validation_memo = this.props.validations ? this.props.validations['notes'] : {};
		const memoValidation = validation_memo ? validation_memo.text : '';
		const memoErrorType = validation_memo ? validation_memo.type : 'success';

		const validation_url = this.props.validations ? this.props.validations['search_url'] : {};
		const urlValidation = validation_url ? validation_url.text : '';
		const urlErrorType = validation_url ? validation_url.type : 'success';

		return (
			<Form
				title={`${NEW ? 'Add' : 'Edit'} supplier`}
				onSubmit={this.submit}
				onReset={this.reset}
				error={this.props.errorMsg}
				returnLink={NEW ? '/supplier/' : `/supplier/${supplier.id}`}
				closeLink="/supplier/">
				<form>


					<FormGroup
						controlId="formBasicText"
						validationState={nameErrorType}>
						<ControlLabel>Name</ControlLabel>
						<FormControl
							type="text"
							value={supplier.name}
							placeholder="Enter Supplier name"
							onChange={this.setName} />
						<FormControl.Feedback />
						<HelpBlock>{nameValidation}</HelpBlock>
					</FormGroup>
					<FormGroup
						controlId="formBasicText"
						validationState={memoErrorType}>
						<ControlLabel>Memo</ControlLabel>
						<FormControl
							type="text"
							value={supplier.notes}
							placeholder="Enter Memo"
							onChange={this.setNotes} />
						<FormControl.Feedback />
						<HelpBlock>{memoValidation}</HelpBlock>
					</FormGroup>
					<FormGroup
						controlId="formBasicText"
						validationState={urlErrorType}>
						<ControlLabel>Url</ControlLabel>
						<FormControl
							type="text"
							value={supplier.search_url}
							placeholder="Search Url"
							onChange={this.setSearch_url} />
						<FormControl.Feedback />
						<HelpBlock>{urlValidation}</HelpBlock>
					</FormGroup>
					<ButtonToolbar>
						<Button
							bsStyle="success"
							onClick={this.submit}
							disabled={hasError(this.props.validations)}>Save</Button>
					</ButtonToolbar>
				</form>
			</Card>
		);
	}
}

const mapStateToProps = state => ({
	supplier: getSupplierActiveObject(state),
	validations: getSupplierValidations(state),
});

export default connect(
	mapStateToProps,
	{
		fetchSupplier,
		newSupplier,
		createSupplier,
		updateSupplier,
		setSupplierField,
	}
)(SupplierEdit);
