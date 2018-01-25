import React from 'react';
import DatePicker from 'react-datepicker';
import FontAwesome from '../../tools/icons/FontAwesome';
import moment from "moment";

export default class VatPeriodRow extends React.Component {
	setVatPeriodField = (name, value) => this.props.setVatPeriodField(this.props.vatPeriod, name, value);

	setEndDate = val => {
		this.setVatPeriodField('end_date', moment(val).format('YYYY-MM-DD'));
	};

	setBeginDate = val => {
		this.setVatPeriodField('begin_date', moment(val).format('YYYY-MM-DD'));
	};

	setVatRate = ({ target: { value }}) => this.setVatPeriodField('vatrate', value);

	remove = () => this.props.remove(this.props.vatPeriod);

	render() {
		const { vatPeriod } = this.props;

		if (vatPeriod.id) {
			return (
				<tr>
					<td>{ vatPeriod.begin_date }</td>
					<td>
						{
							vatPeriod.end_date ? vatPeriod.end_date : (
								<DatePicker
									minDate={vatPeriod.start_date}
									dateFormat="YYYY-MM-DD"
									onChange={this.setEndDate} />
							)
						}
					</td>
					<td>{ vatPeriod.vatrate }</td>
					<td />
				</tr>
			);
		}
		return (
			<tr>
				<td>
					<DatePicker
						selected={vatPeriod.begin_date ? moment(vatPeriod.begin_date) : ''}
						maxDate={vatPeriod.end_date ? moment(vatPeriod.end_date) : ''}
						dateFormat="YYYY-MM-DD"
						onChange={this.setBeginDate} />
				</td>
				<td>
					<DatePicker
						selected={vatPeriod.end_date ? moment(vatPeriod.end_date) : ''}
						minDate={vatPeriod.begin_date ? moment(vatPeriod.begin_date) : ''}
						dateFormat="YYYY-MM-DD"
						onChange={this.setEndDate} />
				</td>
				<td>
					<input
						type="number"
						min="0"
						step="0.001"
						value={vatPeriod.vatrate}
						onChange={this.setVatRate} />
				</td>
				<td>
					<div className="input-group">
						<div className="btn-group-xs">
							<a className="btn bnt-xs btn-danger" onClick={this.remove}>
								<FontAwesome icon="ban" />
							</a>
						</div>
					</div>
				</td>
			</tr>
		);
	}
}
