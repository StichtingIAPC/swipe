import React from "react";

/**
 * Created by Matthias on 30/11/2016.
 */
function valueToString(value, currency){
	if (!Number( value.replace(".", "")))
		return value;
	var value = value.replace(".", "")
	return (Number(value)/100).toFixed(currency.digits)
}
export default function MoneyInput({currency, value, onChange, children, ...restProps}) {
	return (
		<div className="input-group">
			<span className="input-group-addon">{currency.symbol}</span>
			<input className="form-control" value={valueToString(value, currency)} onChange={onChange} {...restProps} />
			{children}
		</div>
	);
}
