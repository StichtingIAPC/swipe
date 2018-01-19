/* eslint-disable no-undef */
import React from 'react';
import { mount, shallow } from 'enzyme';
import { SelectorLine } from './SelectorLine';
describe('SelectorLine', () => {
	test('', () => {
		const comp = shallow(<SelectorLine
			stockLine={ { count: 4,
				price: { currency: 'EUR',
					amount: 4.9 }} }
			name="Firewire" count={4} addArticle={ () => {
			} } />);
		expect(comp.text()).toEqual('Firewire4<Connect(MoneyAmount) />');
	});
});
