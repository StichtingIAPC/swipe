import React from 'react';
import styled, { css } from 'styled-components';
import { rem, darken } from 'polished';
import { theme } from 'components/theme';

const spacing = amount => rem(theme.spacing * amount);

const Base = styled.button`
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border-width: 1px;
	border-style: solid;
	border-color: transparent;
	border-radius: ${props => '3px'};
	height: ${spacing(8)};
	min-width: ${spacing(8)};
	font-size: 1em;
	font-family: ${props => props.theme.font.heading};
	background: ${props => props.theme.color.primary.regular};
	color: ${props => props.theme.color.white};
	padding: ${'0 2.7em'};
	transition: 0.3s;
	outline: 0;

	&:focus,
	&:hover {
		background: ${props => props.theme.color.primary.medium};
		box-shadow: 0px 3px 0 0 rgba(0, 0, 0, 0.1);
	}
	&:active {
		background: ${props => props.theme.color.primary.dark};
	}
`;

const large = css`
	height: ${spacing(12)};
	min-width: ${spacing(12)};
`;

const positive = css`
	background: ${props => props.theme.color.positive.regular};
	color: ${props => props.theme.color.white};

	&:focus,
	&:hover {
		background: ${props => props.theme.color.positive.medium};
	}
	&:active {
		background: ${props => props.theme.color.positive.dark};
	}
`;

const negative = css`
	background: ${props => props.theme.color.negative.regular};
	color: ${props => props.theme.color.white};

	&:focus,
	&:hover {
		background: ${props => props.theme.color.negative.medium};
	}
	&:active {
		background: ${props => props.theme.color.negative.dark};
	}
`;

const square = css`
	padding: 0;
`;

const Button = styled(Base)`
	${props => props.positive && positive};
	${props => props.negative && negative};
	${props => props.large && large};
	${props => props.square && square};
`;

export default Button;
