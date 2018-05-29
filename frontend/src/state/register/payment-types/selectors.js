export const getPaymentTypeIdForString = (state, name) => (state.register.paymentTypes.paymentTypes.filter((x) => (x.name === name))[0] || {}).id;
