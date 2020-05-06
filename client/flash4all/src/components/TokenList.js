import React, { Component } from 'react';
import { connect } from 'react-redux'

class TokenList extends Component {
  render() {
    return <h1>List of Tokens</h1>;
  }
}

const mapStateToProps = (state) => {
  return {
  }
}

const mapDispatchToProps = {  }

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(TokenList)

