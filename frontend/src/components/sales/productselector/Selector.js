import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Button, ButtonGroup, Table, FormControl, Label } from 'react-bootstrap';
import { Box } from 'reactjs-admin-lte';
import MoneyAmount from '../../money/MoneyAmount';
import { getArticleById } from '../../../state/assortment/articles/selectors';
import { fetchAllArticles } from '../../../state/assortment/articles/actions';
import LabelList from "../../assortment/LabelList";
import fetchAllLabelTypes from "../../../state/assortment/label-types/actions";

class Selector extends React.Component {
	static propTypes = {
		onArticleAdd: PropTypes.func.isRequired,
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

	constructor(props) {
		super(props);
		this.state = {
			search: '',
		};
	}

	componentWillMount() {
		this.props.fetchAllArticles();
		this.props.fetchAllLabels();
	}

	searchChange = (e) => {
		this.setState({ search: e.target.value });
	};

	render() {
		const labelsOfArticles = this.props.stock.map(s => this.props.article(s.article).labels);
		return <Box>
			<Box.Header>
				<Box.Title>
					Products
				</Box.Title>
				<Box.Tools>
					<FormControl
						type="text"
						placeholder="Search"
						name="search"
						onChange={this.searchChange}
						value={this.state.search}/>
				</Box.Tools>
			</Box.Header>
			<Box.Body>
				<Table responsive striped hover>
					<thead>
						<tr>
							<th>Article</th>
							<th>Amount</th>
							<th>Price</th>
						</tr>
					</thead>
					<tbody>
						{
							this.props.stock.filter(item => this.props.article(item.article).name
								.toLowerCase().includes(this.state.search.toLowerCase()))
								.map(item => (
									<tr key={item.article} onClick={() => this.props.onArticleAdd(item.article, 1)}>
										<td>{this.props.article(item.article).name}<LabelList labels={this.props.article(item.article).labels}/></td>
										<td>{item.count}</td>
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
		fetchAllLabels: fetchAllLabelTypes,
	}
)(Selector);
