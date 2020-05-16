pragma solidity ^0.6.6;
pragma experimental ABIEncoderV2;

interface ERC20 {
    function totalSupply() external view returns (uint supply);
    function balanceOf(address _owner) external view returns (uint balance);
    function transfer(address _to, uint _value) external returns (bool success);
    function transferFrom(address _from, address _to, uint _value) external returns (bool success);
    function approve(address _spender, uint _value) external returns (bool success);
    function allowance(address _owner, address _spender) external view returns (uint remaining);
    function decimals() external view returns(uint digits);
    event Approval(address indexed _owner, address indexed _spender, uint _value);
}

interface SimpleNetworkInterface { //Kyber on Ropsten 0x818E6FECD516Ecc3849DAf6845e3EC868087B755
    function swapTokenToToken(ERC20 src, uint srcAmount, ERC20 dest, uint minConversionRate) external returns(uint);
    function swapEtherToToken(ERC20 token, uint minConversionRate) external payable returns(uint);
    function swapTokenToEther(ERC20 token, uint srcAmount, uint minConversionRate) external returns(uint);
}

interface IUniswapV2Router01 { //Uniswap V2 on Ropsten 0xf164fC0Ec4E93095b804a4795bBe1e041497b92a
    function swapExactTokensForTokens(uint amountIn,uint amountOutMin,address[] calldata path,address to,uint deadline) external returns (uint[] memory amounts);
    function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline) external payable returns (uint[] memory amounts);
    function swapExactTokensForETH(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);
}

import 'https://github.com/aave/flashloan-box/blob/master/contracts/aave/ILendingPoolAddressesProvider.sol';
import 'https://github.com/aave/flashloan-box/blob/master/contracts/aave/ILendingPool.sol';
import 'https://github.com/aave/flashloan-box/blob/master/contracts/aave/FlashLoanReceiverBase.sol';

//import 'https://github.com/aave/aave-protocol/blob/master/contracts/configuration/LendingPoolAddressesProvider.sol';
//import 'https://github.com/aave/aave-protocol/blob/master/contracts/lendingpool/LendingPool.sol';
//import 'https://github.com/aave/aave-protocol/blob/master/contracts/flashloan/base/FlashLoanReceiverBase.sol';

contract flashTurnaround is FlashLoanReceiverBase {

    constructor () public payable {}

    function turnaround(address[] memory tokenPath, string[] memory exchangePath, uint128 injectedAmount, uint128 requestedAmount) public {
        ERC20 baseToken=ERC20(tokenPath[0]);
        ERC20 targetToken; // changes along the tokenPath

        // injectedAmount : Amount to be sent to the smart contract for exchange
        if (injectedAmount>0) baseToken.transferFrom(msg.sender, address(this), injectedAmount);
        baseToken.approve(address(this), injectedAmount);
        
        // requestedAmount : Wanted amount to perform the trade. If requestedAmount is higher, than a flashloan will fill the gap
        // tbd
        if(requestedAmount>injectedAmount) getAaveFlashLoan(tokenPath[0], requestedAmount - injectedAmount);
        uint amount=requestedAmount;
        
        

        bytes memory params = abi.encode(tokenPath, exchangePath, injectedAmount, requestedAmouunt);
        ILendingPool lendingPool = ILendingPool(addressesProvider.getLendingPool());
        lendingPool.flashLoan(address(this), baseToken, amount, params);


        // Exchange Tokens along the tokenPath
        targetToken.transfer(msg.sender, amount);
       
    }

    function getAaveFlashLoan(address token, uint amount) external {
        ILendingPool lendingPool = ILendingPool(addressesProvider.getLendingPool());
        lendingPool.flashLoan(address(this), token, amount, '');
        //address aaveLPAddressesProvider=0x1c8756FD2B28e9426CDBDcC7E3c4d64fa9A54728;
        //LendingPoolAddressesProvider loanProvider = LendingPoolAddressesProvider(aaveLPAddressesProvider);
        // dai address
        //LendingPool lendingPool = LendingPool(loanProvider.getLendingPool());
        //receive
        //lendingPool.flashLoan(address(this), token address, amount, '');
    }
    
    // Receiver for flashLoan
    function executeOperation(address _reserve, uint256 _amount, uint256 _fee, bytes calldata _params) external {
        (_tokenPath, _exchangePath, _injectedAmount _requestedAmount) = abi.decode(data, (address[], string[], uint128, uint128));
        require(_amount <= getBalanceInternal(address(this), _reserve), "Invalid balance, was the flashLoan successful?");
        
        for (uint i=0; i<tokenPath.length-1; i++) {
            ERC20 fromToken=ERC20(tokenPath[i]);
            targetToken=ERC20(tokenPath[i+1]);
            if (hashi(exchangePath[i])==hashi("kyberswap")) amount = kyberSwap(fromToken, targetToken, amount);
        }

        uint totalDebt = _amount.add(_fee);
        transferFundsBackToPoolInternal(_reserve, totalDebt);
    }

    function kyberSwap(ERC20 fromToken, ERC20 targetToken, uint amount) private returns (uint exchangedAmount) {
        address kyberSC=0x818E6FECD516Ecc3849DAf6845e3EC868087B755;
        SimpleNetworkInterface k = SimpleNetworkInterface(kyberSC);
        fromToken.approve(kyberSC, amount);
        return k.swapTokenToToken(fromToken, amount, targetToken, 0);
    }
    
    //function uniswapV2(ERC20 fromToken, ERC20 targetToken, uint amount) private returns (uint exchangedAmount) {
    //    address uniswapSC=0xf164fC0Ec4E93095b804a4795bBe1e041497b92a;
    //    IUniswapV2Router01 u = IUniswapV2Router01(uniswapSC);
    //    fromToken.approve(uniswapSC, amount);
    //    return u.swapExactTokensForTokens(amount,0,[address(this),address(this),address(this)],address(this),0)[1];
    //}
    function hashi(string memory text) private pure returns (bytes32 hash) {
        return keccak256(abi.encodePacked(text));
    }

    function giveMeEth() public payable {

    }

    function getBalance() public pure returns (uint256) { //view
        return 823;
        //address(this).balance;
    }

    function withdraw() public {
        msg.sender.transfer(address(this).balance);
    }
}
