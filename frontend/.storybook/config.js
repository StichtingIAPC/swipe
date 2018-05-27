import React from 'react';
import styled from 'styled-components';
import { configure, addDecorator } from '@storybook/react';

import Theme from 'components/theme';

const Wrapper = styled.div`
	padding: 1em;
`;

const ThemeDecorator = story => (
	<Theme>
		<Wrapper>{story()}</Wrapper>
	</Theme>
);

addDecorator(ThemeDecorator);

const req = require.context('../src/components', true, /\.story\.js$/);

function loadStories() {
	req.keys().forEach(filename => req(filename));
}

configure(loadStories, module);
