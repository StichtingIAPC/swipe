import React from 'react';
import {mount, shallow} from 'enzyme';
import {Totals} from './Totals';
describe('Totals', () => {
	test('', () => {
		const comp = shallow(<Totals total={ {currency: 'EUR', amount: 4.9} }/>);
		expect(comp.text()).toEqual('TOTAL<Connect(MoneyAmount) />');
		console.log(comp.children());
	});
});
