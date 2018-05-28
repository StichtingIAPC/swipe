import React from 'react';
import { storiesOf } from '@storybook/react';

import * as icons from '../index';

const story = storiesOf('Icon', module);

Object.keys(icons).forEach(icon =>
	story.add(icon, () => React.createElement(icons[icon]), { width: 20 }),
);
