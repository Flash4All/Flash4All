import React, {Component}  from 'react';
import { connect } from 'react-redux';
import tokenActions from '../redux/actions/tokenActions';

let { fetchTokens, addToken } = tokenActions;

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
    }
  }

  addTokens(token) {
    this.props.addToken(token);
    // do something
  }

  componentDidMount() {
    this.props.fetchTokens();
  }

   render() {
     let { tokens } = this.props.token;
     return (
     <section>
        List of Tokens
       {tokens.map((token) => (<div> {token}</div>))}
     </section>
     )
   }
}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
  fetchTokens: () => dispatch(fetchTokens()),
  addToken: (token) => dispatch(addToken(token)),
})

export default connect(mapStateToProps, mapDispatchToProps)(Home);
