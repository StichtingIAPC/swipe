import React from 'react';
import FontAwesome from '../tools/icons/FontAwesome.js';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { startFetchingRegisterOpen } from '../../state/register/actions';

class RegisterOpenIndicator extends React.Component {
	componentWillMount() {
		this.props.getOpenStatus();
	}
	render() {
		return <FontAwesome icon={this.props.open ? 'circle indicator-green' : 'circle-o indicator-red'} />;
	}
}

RegisterOpenIndicator.propTypes = {
	open: PropTypes.bool,
};

export default connect(
	state => ({ open: state.register.open }),
	{ getOpenStatus: startFetchingRegisterOpen },
)(RegisterOpenIndicator);
