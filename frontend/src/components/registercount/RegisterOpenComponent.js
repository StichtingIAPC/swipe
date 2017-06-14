import React from 'react';
import PropTypes from 'prop-types';
import DenominationCount from './DenominationCount';

export default class RegisterOpenComponent extends React.Component {
	static propTypes = {
		updateAmount: PropTypes.func.isRequired,
		updateDenomAmount: PropTypes.func.isRequired,
		register: PropTypes.object.isRequired,
		registerCount: PropTypes.object.isRequired,
		currency: PropTypes.object.isRequired,
	};

	constructor(props) {
		super(props);
		this.state = {
			selected: false,
		};
	}

	render() {
		const { register, registerCount, currency } = this.props;

		return (
			<div className="box">
				<div className="box-header">
					<h3 className="box-title">{register.name}</h3>
				</div>
				<div className="box-body">
					<div className="input-group">
						<span className="input-group-addon">
							<input type="checkbox" checked={this.state.selected} onChange={() => this.setState(({ selected }) => ({ selected: !selected }))} />
						</span>
						<span className="input-group-addon">{currency.symbol}</span>
						<input
							className="form-control"
							type="number"
							min={0}
							disabled={!this.state.selected || register.is_cash_register}
							value={registerCount.amount} />
					</div>
					{
						register.is_cash_register ? currency.denomination_set.map(
							denom => <DenominationCount disabled={!this.state.selected} key={denom.amount} currency={currency} registerCount={registerCount} amount={denom.amount} />
						) : null
					}
				</div>
			</div>
		);
	}
}

