import React from 'react';
import { Route } from 'react-router';
import MoneyBase from '../components/admin/money/MoneyBase';
import CurrencyCreate from '../components/admin/money/currency/CurrencyCreate';
import CurrencyEdit from '../components/admin/money/currency/CurrencyEdit';
import CurrencyDetail from '../components/admin/money/currency/CurrencyDetail';

/**
 * Created by Matthias on 26/11/2016.
 */

export default (
	<Route path="" component={MoneyBase}>
		<Route path="money/currency/">
			<Route path="create/" component={CurrencyCreate} />
			<Route path=":currencyID/edit/" component={CurrencyEdit} />
			<Route path=":currencyID/" component={CurrencyDetail} />
		</Route>
		<Route path="money/" />
	</Route>
);
