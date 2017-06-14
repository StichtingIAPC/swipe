import React from "react";
import { connect } from "react-redux";
import { connectMixin, fetchStateRequirementsFor } from "../../core/stateRequirements";
import { currencies } from "../../actions/money/currencies";
import { registers } from "../../actions/register/registers";
import { openRegisterCounts } from "../../actions/register/registerCount/openRegisters";
import { closedRegisterCounts } from "../../actions/register/registerCount/closedRegisters";
import RegisterOpenComponent from "./RegisterOpenComponent";

class RegisterCount extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		if (!this.props.requirementsLoaded)
			return null;

		const { CountComponent, registers: regs, registerCounts, currencies: currs } = this.props;

		const regCounts = regs.map(register => [ register, registerCounts.find(count => count.register === register.id) ])
			.filter(entry => typeof entry[1] !== 'undefined');

		const briefRegs = regCounts.filter(entry => !entry[0].is_cash_register);
		const cashRegs = regCounts.filter(entry => !!entry[0].is_cash_register);

		return (
			<div className="row">
				<div className="col-md-3">
					{
						briefRegs.map(([ register, count ]) => (
							<CountComponent key={register.id} register={register} registerCount={count} currency={currs.find(curr => curr.iso === register.currency)} />
						))
					}
				</div>
				<div className="col-md-9 brief-register-container">
					{
						cashRegs.map(([ register, count ]) => (
							<div key={register.id} className="brief-register">
								<CountComponent register={register} registerCount={count} currency={currs.find(curr => curr.iso === register.currency)} />
							</div>
						))
					}
				</div>
			</div>
		);
	}
}

export const OpenRegisterCount = connect(
	state => ({
		...connectMixin({
			closedRegisterCounts,
			registers,
			currencies,
		}, state),
		registers: state.registers.registers,
		registerCounts: state.closedRegisterCounts.closedRegisterCounts,
		currencies: state.currencies.currencies,
		CountComponent: RegisterOpenComponent,
	})
)(RegisterCount);

export const CloseRegisterCount = connect(
	state => ({
		...connectMixin({
			openRegisterCounts,
			registers,
			currencies,
		}, state),
		registers: state.registers.registers,
		registerCounts: state.openRegisterCounts.openRegisterCounts,
		currencies: state.currencies.currencies,
		CountComponent: RegisterOpenComponent,
	})
)(RegisterCount);
