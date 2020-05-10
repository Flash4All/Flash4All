import React, {Component}  from 'react';
import { connect } from 'react-redux';
import tokenActions from '../redux/actions/tokenActions';
import Web3 from 'web3';

let { fetchTokens, addToken, arbitrage }  = tokenActions;

let abi = {};

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      flashEthAmount: 0,
    }
  }

  addTokens(token) {
    this.props.addToken(token);
  }

  getArbitrage = (token) => {
    this.props.arbitrage(token);
  }

  flashEth = () => {
    console.log(this.state.flashEthAmount + 'flash eth clicked');
    window.ethereum.enable().then((accounts) => {
      console.log(accounts[0])
    });
  }

  componentDidMount() {
    if (window.web3 == null) {
      var web3 = new Web3(Web3.givenProvider);
      window.web3 = web3;
    }

    console.log(window.web3);

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
       <hr />
       <hr />
       <div class="input-group i-1">
         <input type="text" onChange={(e) => this.setState({flashEthAmount: e.target.value})} class="form-control" id="input1" placeholder="Amount of ETH" />
         <button onClick={this.flashEth} type="button" id="data_button1" class="btn btn-primary">Flash ETH</button>
       </div>
       <div class="input-group i-2">
         <input type="text" class="form-control" id="input2" placeholder="Amount of DAI" />
         <button type="button" id="data_button2" class="btn btn-primary">Flash DAI</button>
       </div>
       <div class="input-group i-3">
         <input type="text" class="form-control" id="input3" placeholder="Amount of DAI" />
         <button type="button" id="data_button3" class="btn btn-primary">Flash DAI > KNC > ETH (via Kyber)</button>
       </div>
       <div class="input-group i-3">
         <input type="text" class="form-control" id="input4" placeholder="Amount of DAI" />
         <button type="button" id="data_button4" class="btn btn-primary">Flash DAI > KNC > ETH (via Uniswap v2 flash?)</button>
       </div>
       <div class="input-group i-4">
         <input type="text" class="form-control" id="input5_1" placeholder="Amount of DAI" />
         <input type="text" class="form-control" id="input5_2" placeholder="Flashloan amount in DAI" />
         <button type="button" id="data_button5" class="btn btn-primary">Flash DAI > KNC > ETH (via Kyber)</button>
       </div>

       <div class="input-group i-5">
         <input type="text" class="form-control" id="input6" placeholder="Amount of DAI" />
         <button type="button" id="data_button5" class="btn btn-primary">Flash DAI > EOS > DAI (via predefined exchanges x,y)</button>
       </div>
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
