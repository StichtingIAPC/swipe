import React from "react";

/**
 * Created by Matthias on 30/11/2016.
 */

export default function MoneyInput({currency, value, onChange, children, ...restProps}) {
	return (
		<div className="input-group">
			<span className="input-group-addon">{currency.symbol}</span>
			<input className="form-control" value={Number(value).toFixed(currency.digits)} step={10 ** (-currency.digits)} onChange={onChange} {...restProps} />
			{children}
		</div>
	);
}
