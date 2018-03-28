import createSagaMiddleware from 'redux-saga';
import { routerMiddleware } from 'react-router-redux';
import rootReducer from './reducer';
import { applyMiddleware, compose, createStore } from 'redux';
import createBrowserHistory from 'history/createBrowserHistory';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const sagaMiddleware = createSagaMiddleware();

const history = createBrowserHistory();

const routingMiddleware = routerMiddleware(history);

const store = createStore(
	rootReducer,
	{},
	composeEnhancers(applyMiddleware(routingMiddleware, sagaMiddleware))
);

export { sagaMiddleware, history };
export default store;
