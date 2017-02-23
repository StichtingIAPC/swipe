import React from "react";
import { connect } from "react-redux";
import { connectMixin, fetchStateRequirementsFor } from "../../core/StateRequirements";
import CurrencyList from "./currency/CurrencyList";
import VATList from "./VAT/VATList";
import { currencies } from "../../actions/money/currencies";
import { VATs } from "../../actions/money/VATs";
/**
 * Created by Matthias on 26/11/2016.
 */

class MoneyBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		return (
			<div className="row">
				<div className="col-xs-4 col-md-4">
					<CurrencyList activeID={this.props.currencyID || ''} />
					<VATList activeID={this.props.VATID || ''} />
				</div>
				<div className="col-xs-8 col-md-8">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>
			</div>
		)
	}
}

export default connect(
	connectMixin({ currencies, VATs })
)(MoneyBase);
