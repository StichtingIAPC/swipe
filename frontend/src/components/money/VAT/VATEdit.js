import React from 'react';
import { connect } from 'react-redux';
import DatePicker from 'react-datepicker';
import { createvat, updatevat } from '../../../state/money/vats/actions.js';
import Form from '../../forms/Form';
import { BoolField, StringField } from '../../forms/fields';
import FontAwesome from '../../tools/icons/FontAwesome';
import { fetchvat } from '../../../state/money/vats/actions';

class VATEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
		this.renderVATPeriodRow = ::this.renderVATPeriodRow;
	}

	componentWillMount() {
		this.props.fetchvat(this.props.match.params.vatId);
	}

	getResetState(props = this.props) {
		if (props.vat !== null) {
			return { ...props.vat };
		}
		return {
			name: '',
			active: true,
			vatperiod_set: [],
		};
	}

	reset() {
		this.setState(this.getResetState());
	}

	componentWillReceiveProps(props) {
		this.setState(this.getResetState(props));
	}

	save(evt) {
		evt.preventDefault();
		if (this.state.id) {
			this.props.updatevat(this.state);
		} else {
			this.props.createvat(this.state);
		}
	}

	renderVATPeriodRow = ({ vatPeriod }) => {
		const updateValue = (name, nextValue) => this.setState(state => {
			const nstate =
				{
					...state,
					vatperiod_set: [
						...state.vatperiod_set,
					],
				}

			;
			nstate.vatperiod_set[state.vatperiod_set.findIndex(e => e === vatPeriod)] = {
				...vatPeriod,
				[name]: nextValue,
			};
			return nstate;
		});

		const remove = () => this.setState(state => (
			{
				...state,
				vatperiod_set: state.vatperiod_set.filter(el => el !== vatPeriod),
			}
		));

		if (vatPeriod.id) {
			return (
				<tr>
					<td>{vatPeriod.begin_date}</td>
					<td>
						{
							vatPeriod.end_date ? vatPeriod.end_date : (
								<DatePicker
									minDate={vatPeriod.start_date}
									dateFormat="YYYY-MM-DD"
									onChange={val => updateValue('end_date', val)} />
							)
						}
					</td>
					<td>{vatPeriod.vatrate}</td>
					<td />
				</tr>
			);
		}
		return (
			<tr>
				<td>
					<DatePicker
						selected={vatPeriod.begin_date}
						maxDate={vatPeriod.end_date}
						dateFormat="YYYY-MM-DD"
						onChange={val => updateValue('begin_date', val)} />
				</td>
				<td>
					<DatePicker
						selected={vatPeriod.end_date}
						minDate={vatPeriod.begin_date}
						dateFormat="YYYY-MM-DD"
						onChange={val => updateValue('end_date', val)} />
				</td>
				<td>
					<input
						type="number"
						min="0"
						step="0.001"
						value={vatPeriod.vatrate}
						onChange={evt => updateValue('vatrate', evt.target.value)} />
				</td>
				<td>
					<div className="input-group">
						<div className="btn-group-xs">
							<a className="btn bnt-xs btn-danger" onClick={() => remove()}>
								<FontAwesome icon="ban" />
							</a>
						</div>
					</div>
				</td>
			</tr>
		);
	}

	render() {
		const addVATPeriod = () => this.setState(state => ({
			...state,
			vatperiod_set: [
				...state.vatperiod_set,
				{
					begin_date: '',
					end_date: '',
					vatrate: 1,
				},
			],
		}));

		return (
			<Form
				returnLink={this.state.id ? `/money/vat/${this.state.id}/` : '/money/'}
				closeLink="/money/"
				title={this.state.id ? this.state.name : 'New VAT'}
				onReset={::this.reset}
				onSubmit={::this.save}
				error={this.props.errorMsg}>
				<StringField
					name="Name" value={this.state.name}
					onChange={evt => this.setState({ name: evt.target.value })} />
				<BoolField
					name="Active" value={this.state.active}
					onChange={() => this.setState(({ active }) => ({ active: !active }))} />
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
											<a onClick={addVATPeriod} className="btn btn-">
												<FontAwesome icon="plus" />
											</a>
										</div>
									</th>
								</tr>
							</thead>
							<tbody>
								{
									this.state.vatperiod_set.map(
										(vp, i) => (
											<this.renderVATPeriodRow key={vp.id || `new${i}`} vatPeriod={vp} />
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
		updatevat,
		createvat,
		fetchvat,
	}
)(VATEdit);
