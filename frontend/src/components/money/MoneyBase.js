import React from "react";
import {connect} from "react-redux";
import {connectMixin, fetchStateRequirementsFor} from "../../core/StateRequirements";
import CurrencyList from "./currency/CurrencyList";
import {currencies} from "../../actions/money/currencies";

/**
 * Created by Matthias on 26/11/2016.
 */

let MoneyBase = class extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		return (
			<div className="row">
				<div className="col-xs-6 col-md-6">
					<CurrencyList activeID={this.props.currencyID || ''} />
				</div>
				<div className="col-xs-6 col-md-6">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>
			</div>
		)
	}
};

MoneyBase = connect(
	connectMixin({ currencies })
)(MoneyBase);

export default MoneyBase
