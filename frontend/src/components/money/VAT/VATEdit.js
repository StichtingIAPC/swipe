import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import DatePicker from "react-datepicker";
import { updateVAT, createVAT } from "../../../actions/money/VATs";
import Form from "../../forms/Form";
import { StringField, BoolField } from "../../forms/fields";
import FontAwesome from "../../tools/icons/FontAwesome";

class VATEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
		this.renderVATPeriodRow = this.renderVATPeriodRow.bind(this);
	}

	getResetState(props = this.props) {
		if (props.VAT != null) return { ...props.VAT };
		return { name: '', active: true, vatperiod_set: [] };
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
			this.props.updateVAT(this.state);
		} else {
			this.props.createVAT(this.state);
		}
	}

	renderVATPeriodRow({VATPeriod}) {
		const updateValue = (name, nextValue) => this.setState(state => {
			const nstate = (
				{
					...state,
					vatperiod_set: [
						...state.vatperiod_set
					],
				}
			);
			nstate.vatperiod_set[state.vatperiod_set.findIndex(e => e == VATPeriod)] = {...VATPeriod, [name]: nextValue};
			return nstate;
		});

		const remove = () => this.setState(state => (
			{
				...state,
				vatperiod_set: state.vatperiod_set.filter((el) => el !== VATPeriod),
			}
		));

		if (VATPeriod.id) {
			return (
				<tr>
					<td>{VATPeriod.begin_date}</td>
					<td>
						{
							VATPeriod.end_date ? VATPeriod.end_date : (
								<DatePicker
									minDate={VATPeriod.start_date}
									dateFormat="YYYY-MM-DD"
									onChange={val => updateValue('start_date', val)} />
								)
						}
					</td>
					<td>{VATPeriod.vatrate}</td>
					<td />
				</tr>
			)
		} else {
			return (
				<tr>
					<td>
						<DatePicker
							selected={VATPeriod.begin_date}
							maxDate={VATPeriod.end_date}
							dateFormat="YYYY-MM-DD"
							onChange={val => updateValue('begin_date', val)} />
					</td>
					<td>
						<DatePicker
							selected={VATPeriod.end_date}
							minDate={VATPeriod.begin_date}
							dateFormat="YYYY-MM-DD"
							onChange={val => updateValue('end_date', val)} />
					</td>
					<td>
						<input
							type="number"
							min="0"
							step="0.001"
							value={VATPeriod.vatrate}
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
			)
		}
	}

	render() {
		let index = 0;
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
				returnLink={this.state.id ? `/money/vat/${this.state.id}/` : "/money/"}
				closeLink="/money/"
				title={this.state.id ? this.state.name : "New VAT"}
				onReset={this.reset.bind(this)}
				onSubmit={this.save.bind(this)}
				error={this.props.errorMsg}>
				<StringField name="Name" value={this.state.name} onChange={(evt) => this.setState({name: evt.target.value})} />
				<BoolField name="Active" value={this.state.active} onChange={(evt) => this.setState({active: evt.target.value})} />
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
										(vp) => (
											<this.renderVATPeriodRow key={vp.id || 'new' + index++} VATPeriod={vp} />
										)
									)
								}
							</tbody>
						</table>
					</div>
				</div>
			</Form>
		)
	}
}

export default connect(
	(state, ownProps) => ({
		errorMsg: state.VATs.inputError,
		VAT: (state.VATs.VATs.find((obj) => obj.id == ownProps.params.VATID) || null),
	}),
	dispatch => ({
		updateVAT: (VAT) => dispatch(updateVAT(VAT)),
		createVAT: (VAT) => dispatch(createVAT(VAT)),
	})
)(VATEdit)
