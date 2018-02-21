import React from 'react';
import { connect } from 'react-redux';

import { createvat, updatevat, fetchvat, setvatField } from '../../../../state/money/vats/actions.js';
import Form from '../../../forms/Form';
import { BoolField, StringField } from '../../../forms/fields';
import FontAwesome from '../../../tools/icons/FontAwesome';
import { resetvat } from '../../../../state/money/vats/actions';
import VatPeriodRow from '../../../money/VAT/VatPeriodRow';

class VATEdit extends React.Component {
	componentWillMount() {
		this.reset();
	}

	reset() {
		if (this.props.match.params.vatId) {
			this.props.fetchvat(this.props.match.params.vatId);
		} else {
			this.props.resetvat();
		}
	}

	setName = ({ target: { value }}) => this.props.setvatField('name', value);
	setActive = () => this.props.setvatField('active', !this.props.vat.active);

	componentWillReceiveProps({ match, fetchvat: fetch, resetvat: reset }) {
		if (this.props.match.params.vatId !== match.params.vatId) {
			if (typeof match.params.vatId === 'undefined') {
				reset();
			} else {
				fetch(match.params.vatId);
			}
		}
	}

	save = evt => {
		evt.preventDefault();
		const { vat } = this.props;

		if (vat.id === null) {
			this.props.createvat(vat);
		} else {
			this.props.updatevat(vat);
		}
	};

	updateVatPeriod = (period, field, value) => this.props.setvatField(
		'vatperiod_set',
		this.props.vat.vatperiod_set.map(vatperiod => {
			if (vatperiod === period) {
				return {
					...vatperiod,
					[field]: value,
				};
			}
			return vatperiod;
		})
	);

	removeVatPeriod = period => this.props.setvatField('vatperiod_set', this.props.vat.vatperiod_set.filter(p => p !== period));

	addVatPeriod = () => this.props.setvatField(
		'vatperiod_set',
		this.props.vat.vatperiod_set.concat([{
			begin_date: null,
			end_date: null,
			vatrate: 1,
		}])
	);

	render() {
		const { vat } = this.props;

		return (
			<Form
				returnLink={vat.id ? `/money/vat/${vat.id}/` : '/money/'}
				closeLink="/money/"
				title={vat.id ? vat.name : 'New VAT'}
				onReset={this.reset}
				onSubmit={this.save}
				error={this.props.errorMsg}>
				<StringField
					name="Name" value={vat.name}
					onChange={this.setName} />
				<BoolField
					name="Active" value={vat.active}
					onChange={this.setActive} />
				<div className="form-group">
					<label className="col-sm-3 control-label">VAT periods</label>
					<div className="col-sm-9">
						<table className="table table-striped">
							<thead>
								<tr>
									<th className="col-xs-4">Start date</th>
									<th className="col-xs-4">End date</th>
									<th className="col-xs-3">Rate (* factor)</th>
									<th className="col-xs-1">
										<div className="btn-group-xs">
											<a onClick={this.addVatPeriod} className="btn btn-">
												<FontAwesome icon="plus" />
											</a>
										</div>
									</th>
								</tr>
							</thead>
							<tbody>
								{
									vat.vatperiod_set.map(
										(vp, i) => (
											<VatPeriodRow
												key={vp.id || `new${i}`}
												vatPeriod={vp}
												delete={this.removeVatPeriod}
												setVatPeriodField={this.updateVatPeriod} />
										)
									)
								}
							</tbody>
						</table>
					</div>
				</div>
			</Form>
		);
	}
}

export default connect(
	state => ({
		errorMsg: state.money.vats.error,
		vat: state.money.vats.activeObject,
	}),
	{
		setvatField,
		resetvat,
		updatevat,
		createvat,
		fetchvat,
	}
)(VATEdit);
