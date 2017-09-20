import React from 'react';
import { connect } from 'react-redux';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import { currencies } from '../../actions/money/currencies';
import { registers } from '../../actions/register/registers';
import {
	openRegisterCounts,
	openUpdateAmount,
	openUpdateDenomAmount
} from '../../actions/register/registerCount/openRegisters';
import {
	closedRegisterCounts,
	closedUpdateAmount,
	closedUpdateDenomAmount
} from '../../actions/register/registerCount/closedRegisters';
import RegisterOpenComponent from './RegisterOpenComponent';

const logExceptions = func => (...args) => {
	console.log('called ', func, ...args);
	try {
		return func(...args);
	} catch (e) {
		console.log('caught ', e);
		throw e;
	}
};

class RegisterCount extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	static CurrencyName = ({ currencyName }) => (
		<h2 className="page-header">{currencyName}</h2>
	);

	static CurrencyRegisters = ({
		registers: regs,
		registerCounts,
		Component,
		updateDenomAmount,
		updateAmount,
		currency,
	}) => {
		const regCounts = regs.map(register => [
			register,
			registerCounts.find(count => count.register === register.id),
		]).filter(entry => typeof entry[1] !== 'undefined');

		const briefs = regCounts.filter(([ register ]) => !register.is_cash_register);
		const cash = regCounts.filter(([ register ]) => !!register.is_cash_register);

		return (
			<div className="row">
				<div className="col-md-4">
					{
						briefs.map(([ register, count ]) => (
							<Component
								key={register.id}
								updateDenomAmount={updateDenomAmount}
								updateAmount={updateAmount}
								register={register}
								registerCount={count}
								currency={currency} />
						))
					}
				</div>
				<div className="col-md-8">
					{
						cash.map(([ register, count ]) => (
							<div key={register.id} className="brief-register">
								<Component
									updateDenomAmount={updateDenomAmount}
									updateAmount={updateAmount}
									register={register}
									registerCount={count}
									currency={currency} />
							</div>
						))
					}
				</div>
			</div>
		);
	};

	render() {
		if (!this.props.requirementsLoaded)
			return null;

		const { CountComponent, registers: regs, registerCounts, currencies: currs, updateDenomAmount, updateAmount } = this.props;

		const currencyRegisterMap = regs.reduce((product, register) => ({
			...product,
			[register.currency]: [ ...product[register.currency] || [], register ],
		}), {});

		return (
			<div className="col">
				{
					Object.entries(currencyRegisterMap)
						.reduce(
							(all, [ currency, regis ]) => {
								const curr = currs.find(cur => cur.iso === currency);

								return [
									...all,
									<RegisterCount.CurrencyName
										currencyName={curr.name}
										key={`${currency}:name`} />,
									<RegisterCount.CurrencyRegisters
										key={`${currency}:regs`}
										registers={regis}
										registerCounts={registerCounts}
										Component={CountComponent}
										updateDenomAmount={updateDenomAmount}
										updateAmount={updateAmount}
										currency={curr} />,
								];
							}, [])
				}
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
	}),
	dispatch => ({
		dispatch,
		updateAmount: (...args) => dispatch(closedUpdateAmount(...args)),
		updateDenomAmount:  (...args) => dispatch(closedUpdateDenomAmount(...args)),
		emptyMessage: 'There are no closed registers',
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
	}),
	dispatch => ({
		dispatch,
		updateAmount: (...args) => dispatch(openUpdateAmount(...args)),
		updateDenomAmount: (...args) => dispatch(openUpdateDenomAmount(...args)),
		emptyMessage: 'There are no open registers',
	})
)(RegisterCount);
