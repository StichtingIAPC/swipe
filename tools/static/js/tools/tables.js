import React from 'react'


export class SwipeTable extends React.Component {
  constructor({children, data, classes}) {
    super({children, data, classes});
    this.columns = children;
    this.data = data;
    this.classes = classes;

    this.RowRenderer = class extends React.Component {
      constructor({row}) {
        this.row = row
      }

      render() {
        const cells = React.Children.map(children,
          (col) => <col.CellRenderer value={col.key(this.row)}/>
        );
        return <tr>{cells}</tr>
      }
    }
  }

  render() {
    const heads = this.columns.map(
      (col) => <col.HeadRenderer/>
    );
    const rows = this.data.map(
      (row) => <this.RowRenderer row={row}/>
    );
    return (
      <table class={this.classes}>
        <thead>
          <tr>
            {heads}
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    );
  }
}

export class Column extends React.Component {
  /**
   * The base class for any columns in the Table. Please extend this class, and override the
   * CellRenderer and HeadRenderer methods when needed.
   */
  constructor({name, key}) {
    super({name, key});
    this.name = name ? name : "Column";
    this.key = key;

    this.HeadRenderer = class extends React.Component {
      render() {
        return <td>{name}</td>
      }
    };

    this.CellRenderer = class extends React.Component {
      render() {
        return <td>{this.props.value}</td>
      }
    };
  }
}
