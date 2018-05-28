import React from 'react';
import styled, { css } from 'styled-components';
import { rem, transparentize } from 'polished';

import { theme } from 'components/theme';

const spacing = amount => rem(theme.spacing * amount);

const Container = styled.span`
	position: relative;
	display: flex;
	width: 100%;
`;

const Base = styled.input`
	width: 100%;
	border-width: 1px;
	border-style: solid;
	border-color: ${props => props.theme.color.secondary.regular};
	border-radius: ${props => rem(props.theme.radius[1])};
	padding: ${spacing(2)} 1em;
	font-size: 1em;
	outline: 0;
	transition: 0.3s;

	&:hover,
	&:focus {
		border-color: ${props => props.theme.color.primary.medium};
	}

	&:focus {
		box-shadow: inset 0 0 0 3px
			${props => transparentize(0.85, props.theme.color.primary.regular)};
	}
`;

const success = css`
	border-color: ${props => props.theme.color.positive.regular} !important;

	&:focus {
		box-shadow: inset 0 0 0 3px
			${props => transparentize(0.85, props.theme.color.positive.regular)};
	}
`;

const error = css`
	border-color: ${props => props.theme.color.negative.regular} !important;

	&:focus {
		box-shadow: inset 0 0 0 3px
			${props => transparentize(0.85, props.theme.color.negative.regular)};
	}
`;

const Input = styled(Base)`
	${props => props.success && success};
	${props => props.error && error};
`;

export default props => (
	<Container>
		<Input {...props} />
	</Container>
);
