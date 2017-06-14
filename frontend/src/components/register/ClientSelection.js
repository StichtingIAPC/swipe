import React from 'react';
import { connect } from 'react-redux';
import AsyncSelectBox from '../base/AsyncSelectBox.js';


export default connect(
	state => ({ client: state.register.client })
)(class ClientSelection extends React.Component {
	constructor() {
		super();
		this.state = { query: '' };
	}

	search(query) {
		// TODO: fire request to Redux saga to actually do a search for clients
		this.setState({ query });
	}

	render() {
		return <div>
			<AsyncSelectBox
				placeholder="Jaap de Steen"
				query={this.state.query}
				onSearch={query => this.search(query)} />
		</div>;
	}
});
