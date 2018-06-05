import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Button, ButtonGroup, Table } from 'react-bootstrap';
import { Box } from 'reactjs-admin-lte';
import MoneyAmount from '../../money/MoneyAmount';
import { getArticleById } from '../../../state/assortment/articles/selectors';
import { fetchAllArticles } from '../../../state/assortment/articles/actions';

class Selector extends React.Component {
	static propTypes = {
		onArticleRemove: PropTypes.func.isRequired,
		receipt: PropTypes.arrayOf(PropTypes.shape({
			article: PropTypes.number.isRequired,
			price: PropTypes.shape({
				amount: PropTypes.string.isRequired,
				currency: PropTypes.string.isRequired,
			}).isRequired,
			count: PropTypes.number.isRequired,
		})).isRequired,
		stock: PropTypes.arrayOf(PropTypes.shape({
			article: PropTypes.number.isRequired,
			price: PropTypes.shape({
				amount: PropTypes.string.isRequired,
				currency: PropTypes.string.isRequired,
			}).isRequired,
			count: PropTypes.number.isRequired,
		})).isRequired,
	};

	componentWillMount() {
		this.props.fetchAllArticles();
	}

	render() {
		console.log(this.props.stock);
		return <Box>
			<Box.Header>
				Products
			</Box.Header>
			<Box.Body>
				<Table responsive striped hover>
					<thead>
						<tr>
							<th>Article</th>
							<th>Price</th>
						</tr>
					</thead>
					<tbody>
						{
							this.props.stock.map(item => (
								<tr key={item.article} onClick={() => this.props.onArticleAdd(item.article, 1)}>
									<td>{this.props.article(item.article).name}</td>
									<td><MoneyAmount money={item.price} /></td>
								</tr>
							))
						}
					</tbody>
				</Table>
			</Box.Body>
		</Box>;
	}
}

export default connect(
	state => ({
		article: getArticleById.bind(null, state),
	}),
	{
		fetchAllArticles,
	}
)(Selector);
