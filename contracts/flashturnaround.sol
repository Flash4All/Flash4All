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


contract flashTurnaround {

    constructor () public payable {}

    function turnaround(address[] memory tokenPath, string[] memory exchangePath, uint128 injectedAmount, uint128 requestedAmount) public {
        ERC20 baseToken=ERC20(tokenPath[0]);
        ERC20 targetToken; // changes along the tokenPath

        // injectedAmount : Amount to be sent to the smart contract for exchange
        if (injectedAmount>0) baseToken.transferFrom(msg.sender, address(this), injectedAmount);
        baseToken.approve(address(this), injectedAmount);
        
        // requestedAmount : Wanted amount to perform the trade. If requestedAmount is higher, than a flashloan will fill the gap
        // tbd
        requestedAmount=injectedAmount;
        
        uint amount=requestedAmount;
        
        // Exchange Tokens along the tokenPath
        for (uint i=0; i<tokenPath.length-1; i++) {
            ERC20 fromToken=ERC20(tokenPath[i]);
            targetToken=ERC20(tokenPath[i+1]);
            if (hashi(exchangePath[i])==hashi("kyberswap")) amount = kyberSwap(fromToken, targetToken, amount);
        }

        targetToken.transfer(msg.sender, amount);
       
    }

    function kyberSwap(ERC20 fromToken, ERC20 targetToken, uint amount) private returns (uint exchangedAmount) {
        address kyberSC=0x818E6FECD516Ecc3849DAf6845e3EC868087B755;
        SimpleNetworkInterface k = SimpleNetworkInterface(kyberSC);
        fromToken.approve(kyberSC, amount);
        return k.swapTokenToToken(fromToken, amount, targetToken, 0);
    }
    
    function uniswapV2() {
        address uniswapSC="0xf164fC0Ec4E93095b804a4795bBe1e041497b92a";
        
    }
    function hashi(string memory text) private pure returns (bytes32 hash) {
        return keccak256(abi.encodePacked(text));
    }

    function giveMeEth() public payable {

    }

    function getBalance() public pure returns (uint256) { //view
        return 823;
        //address(this).balance; just for verification
    }

    //function withdraw() public {
    //    msg.sender.transfer(address(this).balance);
    //}
}
