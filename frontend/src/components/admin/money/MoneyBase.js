import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import CurrencyList from './currency/CurrencyList';
import AccountingGroupList from './accountingGroup/AccountingGroupList';
import VATList from './VAT/VATList';
import { currencies } from '../../../state/money/currencies/actions.js';
import { vats } from '../../../state/money/vats/actions.js';
import { accountingGroups } from '../../../state/money/accounting-groups/actions.js';
import CurrencyEdit from './currency/CurrencyEdit';
import CurrencyDetail from './currency/CurrencyDetail';
import VATEdit from './VAT/VATEdit';
import VATDetail from './VAT/VATDetail';
import AccountingGroupEdit from './accountingGroup/AccountingGroupEdit';
import AccountingGroupDetail from './accountingGroup/AccountingGroupDetail';

/**
 * Created by Matthias on 26/11/2016.
 */

export class MoneyBase extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { match } = this.props;
		console.log(this.props.availableRequirements);

		return (
			<div className="row">
				<div className="col-xs-4 col-md-4">
					<CurrencyList activeID={this.props.currencyID || ''} />
					<AccountingGroupList activeID={this.props.accGrpID || ''} />
					<VATList activeID={this.props.VATID || ''} />
				</div>
				<div className="col-xs-8 col-md-8">
					{
						this.props.requirementsLoaded ? (
							<Switch>
								<Route path={`${match.path}/currency/create`} component={CurrencyEdit} />
								<Route path={`${match.path}/currency/:currencyID/edit`} component={CurrencyEdit} />
								<Route path={`${match.path}/currency/:currencyID`} component={CurrencyDetail} />
								<Route path={`${match.path}/vat/create`} component={VATEdit} />
								<Route path={`${match.path}/vat/:vatId/edit`} component={VATEdit} />
								<Route path={`${match.path}/vat/:vatId`} component={VATDetail} />
								<Route path={`${match.path}/accountinggroup/create`} component={AccountingGroupEdit} />
								<Route path={`${match.path}/accountinggroup/:accountingGroupId/edit`} component={AccountingGroupEdit} />
								<Route path={`${match.path}/accountinggroup/:accountingGroupId/`} component={AccountingGroupDetail} />
							</Switch>
						) : null
					}
				</div>
			</div>
		);
	}
}

export default connect(
	connectMixin({
		money: {
			currencies,
			accountingGroups,
			vats,
		},
	})
)(MoneyBase);
