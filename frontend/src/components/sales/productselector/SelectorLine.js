import React from 'react';
import { connect } from 'react-redux';

import {getArticleNameById, getCount } from '../../../state/assortment/articles/selectors';
import { addToSalesListAction } from '../../../state/sales/sales/actions';
import MoneyAmount from '../../money/MoneyAmount';

export class SelectorLine extends React.Component {

	render() {
		const { count, name, stockLine, addArticle } = this.props;

		if (!stockLine)
			return null;
		return <tr onClick={(evt) => addArticle(stockLine, 1, stockLine.count)}>
			<td key='name'>{name}</td>
			<td key='count'>{count}</td>
			<td key='amount'><MoneyAmount money={stockLine.price}/></td>
		</tr>;
	}
}

export default connect(
	(state, props) => ({
		count: getCount(state, props.stockLine),
		name: getArticleNameById(state, props.stockLine.article),
	}),
	{
		addArticle: addToSalesListAction,
		dispatch: args => args,
	}
)(SelectorLine);
