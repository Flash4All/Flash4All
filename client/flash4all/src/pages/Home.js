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
      triArbKyberAmount: {}
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
      var contractABI=[{"inputs":[],"stateMutability":"payable","type":"constructor"},{"stateMutability":"payable","type":"fallback"},{"inputs":[{"internalType":"address","name":"_reserve","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint256","name":"_fee","type":"uint256"},{"internalType":"bytes","name":"_params","type":"bytes"}],"name":"executeOperation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"giveMeEth","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"fromAddr","type":"address"},{"internalType":"address","name":"targetAddr","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"kyberSwap","outputs":[{"internalType":"uint256","name":"exchangedAmount","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address[]","name":"tokenPath","type":"address[]"},{"internalType":"string[]","name":"exchangePath","type":"string[]"},{"internalType":"uint256","name":"injectedAmount","type":"uint256"},{"internalType":"uint256","name":"tradeAmount","type":"uint256"}],"name":"turnaround","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"fromAddr","type":"address"},{"internalType":"address","name":"targetAddr","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"uniswapv1","outputs":[{"internalType":"uint256","name":"exchangedAmount","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}];
      var contractAddress="0x9c8039Db04e769c42C773e8843DF7103d120F7De";
      var web3 = new Web3(Web3.givenProvider);

      // Various addresses for sample transaction on Ropsten testnet
      // DAI on Ropsten Oasis 0x31f42841c2db5173425b5223809cf3a38fede360
      // DAI on Ropsten Kyber 0xad6d458402f60fd3bd25163575031acdce07538d
      // DAI on Ropsten AAve  0xf80a32a835f79d7787e8a8ee5721d0feafd78108 or 0xb5e5d0f8c0cba267cd3d7035d6adc8eba7df7cdd
      var DAI="0xad6d458402f60fd3bd25163575031acdce07538d";
      var KNC="0x7b2810576aa1cce68f2b118cef1f36467c648f92";
      var EOS="0xd5b4218b950a53ff07985e2d88346925c335eae7";
      var WETH="0xc778417e063141139fce010982780140aa0cd5ab";
      var ETH="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE";
      var tokenABI=[{"constant": false,"inputs": [{"name": "_spender", "type": "address"}, {"name": "_value","type": "uint256"}],"name": "approve","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"}];
      var web3Infura = new Web3(Web3.givenProvider || "https://ropsten.infura.io/v3/"); // Infura-ID to be provided
      var tokenContract = new web3Infura.eth.Contract(tokenABI, DAI, {from: accounts[0]});
      
      var smartContract = new web3Infura.eth.Contract(contractABI, contractAddress, {from: accounts[0], gas:21000000, gasPrice:2000000000});
      console.log(smartContract);

      // Exchange parameters - to be adjusted as required
      var tokenPath=[DAI,EOS,ETH];
      var exchangePath=["kyberswap","kyberswap"];
      var initialAmount='800000000000000000'; // from the user's wallet
      var totalAmount='800000000000000000'; // if totel amount is higher, flashloan will be used

      if (tokenPath[0]!=ETH) {
        tokenContract.methods
          .approve(contractAddress,initialAmount).send(() => smartContract.methods
          .turnaround(tokenPath,exchangePath,initialAmount,totalAmount).send({from:accounts[0],gasLimit:7700000}));
      } else
        smartContract.methods
          .turnaround(tokenPath,exchangePath,initialAmount,totalAmount).send({from:accounts[0],gasLimit:7700000,value:initialAmount});
    });
  }

  componentDidMount() {
    if (window.web3 == null) {
      var web3 = new Web3(Web3.givenProvider);
      window.web3 = web3;
    }

    this.props.fetchTokens();
    this.props.arbitrage('ETH');
  }

  render() {
    let { tokens, trades } = this.props.token;
    return (
      <section>
        <p>Available Flash-Mates (click to activate)</p>
        <button style={workingPart}>DAI</button>
        {tokens.map((token) => (<button onClick={this.getArbitrage.bind(null, token)}> {token}</button>))}
        <br/>
        <br/>
        <br/>
        <center>
          <table>
            <tbody>
              <tr>
                <td>

                </td>
              </tr>
            </tbody>
          </table>
          <hr/>
          <table>
            <tbody>
              <tr>
                <td><b>Trading Opportunities</b></td>
                <td><b>Choose your volume</b></td>
              </tr>
              {trades && trades.map((trade, i) => {
              let t = trade[0].split(',');
              return (<tr>
                <td><gain>{trade[1].toString().substr(0, 7)}% </gain> {t[0]} - {t[3]} > {t[1]} - {t[4]} > {t[2]} {t[5]}</td>
                <td>
                  <p>
                    0$<input type="range" value={this.state.triArbKyberAmount[i]} onChange={(e) => this.setState({triArbKyberAmount: {i: e.target.value}})} />100$ <button type="button" onClick={this.triArbKyber}>Execute trade</button>
                    <table><tr>40 {t[3]} from wallet</tr><tr>50 {t[3]} in Flash Loan</tr></table>
                  </p>
                </td>
              </tr>)
              })}
            </tbody>
          </table>
        </center>
        <hr />
        <hr />
        <div class="input-group i-1">
          <input type="text" onChange={(e) => this.setState({flashEthAmount: e.target.value})} class="form-control" id="input1" placeholder="Amount of ETH" />
          <button onClick={this.flashEth} type="button" id="data_button1" class="btn btn-primary">Log account address</button>
        </div>
        <div class="input-group i-3" style={workingPart}>
          <input type="text" onChange={(e) => this.setState({triArbKyberAmount: e.target.value})} class="form-control" id="input3" placeholder="Amount of DAI" />
          <button onClick={this.triArbKyber} type="button" id="data_button3" class="btn btn-primary">Flash DAI > KNC > EOS (via Kyber)</button>
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
