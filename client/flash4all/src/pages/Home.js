import React, {Component}  from 'react';
import { connect } from 'react-redux';
import tokenActions from '../redux/actions/tokenActions';

let { fetchTokens, addToken, arbitrage }  = tokenActions;

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
    }
  }

  addTokens(token) {
    this.props.addToken(token);
  }

  getArbitrage = (token) => {
    this.props.arbitrage(token);
  }

  componentDidMount() {
    this.props.fetchTokens();
    this.props.arbitrage('ETH');
  }

   render() {
     let { tokens, trades } = this.props.token;
     return (
     <section>
        List of Tokens
       {tokens.map((token) => (<div onClick={this.getArbitrage.bind(null, token)}> {token}</div>))}
       <br/>
       <br/>
       <br/>

       {trades.map((trade) => (<div> {JSON.stringify(trade)}</div>))}
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
  arbitrage: (token) => dispatch(arbitrage(token)),
})

export default connect(mapStateToProps, mapDispatchToProps)(Home);
