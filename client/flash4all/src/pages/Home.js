import React, {Component}  from 'react';
import { connect } from 'react-redux';
import tokenActions from '../redux/actions/tokenActions';
import Web3 from 'web3';

let { fetchTokens, addToken, arbitrage }  = tokenActions;

let abi = {};

const workingPart = {backgroundColor: 'powderblue'};

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

  triArbKyber = () => {
    console.log(this.state.triArbKyberAmount + 'starting Kyber exchange process');
    
    window.ethereum.enable().then((accounts) => {
      console.log(accounts[0]);
      var contractABI=[{"inputs":[],"stateMutability":"payable","type":"constructor"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"giveMeEth","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address[]","name":"tokenPath","type":"address[]"},{"internalType":"string[]","name":"exchangePath","type":"string[]"},{"internalType":"uint128","name":"injectedAmount","type":"uint128"},{"internalType":"uint128","name":"requestedAmount","type":"uint128"}],"name":"turnaround","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}];
      var contractAddress="0x7c2Cad2f43E960203f5eACb424F520aCBF5d8cc4";
      var web3 = new Web3(Web3.givenProvider);
      // DAI on Ropsten Oasis 0x31f42841c2db5173425b5223809cf3a38fede360
      // DAI on Ropsten Kyber 0xad6d458402f60fd3bd25163575031acdce07538d
      var DAI="0xad6d458402f60fd3bd25163575031acdce07538d";
      var KNC="0x7b2810576aa1cce68f2b118cef1f36467c648f92";
      var EOS="0xd5b4218b950a53ff07985e2d88346925c335eae7";
      var tokenABI=[{"constant": false,"inputs": [{"name": "_spender", "type": "address"}, {"name": "_value","type": "uint256"}],"name": "approve","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"}];
      var web3Infura = new Web3(Web3.givenProvider || "https://ropsten.infura.io/v3/");
      var tokenContract = new web3Infura.eth.Contract(tokenABI, DAI, {from: accounts[0]});
      
      var smartContract = new web3Infura.eth.Contract(contractABI, contractAddress, {from: accounts[0], gas:21000000, gasPrice:200});
      console.log(smartContract);
      
      tokenContract.methods
        .approve(contractAddress, '100000000000000000000').send(() => smartContract.methods
        .turnaround([DAI, KNC, EOS],["kyberswap","kyberswap"], '1000000000000000000','0').send({from:accounts[0],gasLimit:1700000}))
  
      
      //Send eth to smart contract
      //web3.eth.sendTransaction({from: '0xF9BeF45E5b554A6aA4202f576a5A501d58822006',to: contractAddress,data: web3.eth.abi.encodeFunctionSignature('giveMeEth()'),value: 10000000000000000});   
      //myContract.methods.getBalance().call({from: accounts[0]},(e,r) => {console.log(r);});
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
       <div class="input-group i-3" style={workingPart}>
       <input type="text" onChange={(e) => this.setState({triArbKyberAmount: e.target.value})} class="form-control" id="input3" placeholder="Amount of DAI" />
         <button onClick={this.triArbKyber} type="button" id="data_button3" class="btn btn-primary">Flash DAI > KNC > EOS (via Kyber)</button>
       </div>
       <div class="input-group i-4">
         <input type="text" class="form-control" id="input4" placeholder="Amount of DAI" />
         <button type="button" id="data_button4" class="btn btn-primary">Flash DAI > KNC > ETH (via Uniswap v2 flash?)</button>
       </div>
       <div class="input-group i-5">
         <input type="text" class="form-control" id="input5_1" placeholder="Amount of DAI" />
         <input type="text" class="form-control" id="input5_2" placeholder="Flashloan amount in DAI" />
         <button type="button" id="data_button5" class="btn btn-primary">Flash DAI > KNC > ETH (via Kyber)</button>
       </div>

       <div class="input-group i-6">
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
