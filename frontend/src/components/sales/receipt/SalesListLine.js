import React from 'react';
import { connect } from 'react-redux';

import { getArticleNameById, getCount } from '../../../state/assortment/articles/selectors';
import { mutateSalesLineOfArticle } from '../../../state/sales/sales/actions';
import MoneyAmount from '../../money/MoneyAmount';

class SelectorLine extends React.Component {
	render() {
		const { name, stockLine, addArticle } = this.props;

		console.log(stockLine);

		return <tr onClick={evt => addArticle(stockLine, -1, stockLine.count)}>
			<td key="name">{name}</td>
			<td key="count">{stockLine.count}</td>
			<td key="amount"><MoneyAmount money={stockLine.price} /></td>
			<td key="amount"><MoneyAmount
				money={{ ...stockLine.price,
					amount: stockLine.price.amount * stockLine.count }} /></td>
		</tr>;
	}
}

export default connect(
	(state, props) => ({
		count: getCount(state, props.stockLine),
		name: getArticleNameById(state, props.stockLine.article),
	}),
	{
		addArticle: mutateSalesLineOfArticle,
		dispatch: args => args,
	}
)(SelectorLine);
