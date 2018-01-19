import React from 'react';
import {mount, shallow} from 'enzyme';
import {MoneyAmount} from './MoneyAmount';
describe('MoneyAmount', () => {
	test('Tests that money is represented somewhat correctly' , () => {
		const comp = shallow(<MoneyAmount currencies={ { currencies: [ { iso: 'EUR', symbol: '€'} ] } } money={ { currency: 'EUR', amount: 14 } } />);
  		expect(comp.text()).toEqual('€ 14');
	});

	test('Test that when no currency information exists, the \'wrong\' symbol is used' , () => {
		const comp = shallow(<MoneyAmount currencies={ { currencies: [ ] } } money={ { currency: 'EUR', amount: 14 } } />);
  		expect(comp.text()).toEqual('¬ 14');
	});
});