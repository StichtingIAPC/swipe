import { getActiveRegisters } from '../registers/selectors';

export const getActivePaymentTypes = state => {
	const activeRegisters = getActiveRegisters(state);

	return state.register.paymentTypes.paymentTypes
		.filter(paymentType => activeRegisters.find(register => register.payment_type === paymentType.id));
};
