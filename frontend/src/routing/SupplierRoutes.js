import React from 'react';
import { Route } from 'react-router';

import SupplierBase from '../components/supplier/SupplierBase';
import SupplierEdit from '../components/supplier/SupplierEdit';
import SupplierDetail from '../components/supplier/SupplierDetail';
import SupplierCreate from '../components/supplier/SupplierCreate';

/**
 * Created by Matthias on 17/11/2016.
 */

export default (
	<Route path="" component={SupplierBase}>
		<Route path="supplier/create/" component={SupplierCreate} />
		<Route path="supplier/:supplierID/edit" component={SupplierEdit} />
		<Route path="supplier/:supplierID/" component={SupplierDetail} />
		<Route path="supplier/" />
	</Route>
)
