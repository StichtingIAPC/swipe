import React from 'react';
import numeral from 'numeral'

/**
 * Created by Matthias on 30/11/2016.
 */

export default class MoneyField extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            format: getFormat(props.currency)
        };
        if (props.value !== "") {
            this.state.stringValue = numeral(props.value).format(this.state.format);
        } else {
            this.state.stringValue = "";
        }
        this.handleChange = this.handleChange.bind(this);
    }


    componentWillReceiveProps(nextProps) {
        if (nextProps.currency !== this.props.currency) {
            this.setState({format: getFormat(nextProps.currency)})
        }
    }


    handleChange(event) {
        const newValue = event.target.value;
        this.setState({stringValue: newValue}, () =>
            this.props.onChange(numeral(newValue).format(this.state.format)))
    }

    render() {
        const { currency, children, value, onChange, ...restProps } = this.props;
        return (
            <div className="input-group">
                <span className="input-group-addon">{currency.symbol}</span>
                <input
                    type="text"
                    className="form-control"
                    value={this.state.stringValue}
                    onChange={this.handleChange}
                    {...restProps}
                />
                {children}
            </div>
        );
    }
}

function getFormat(currency) {
    let format = "0,0";
    if (currency.digits > 0) {
        format = format + "." + "0".repeat(currency.digits)
    }
    return format
}
