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
interface aaveLinks {
    function getLendingPool() external view returns (address); // ILendingPoolAddressesProvider
    function getLendingPoolCore() external view returns (address payable); // ILendingPoolAddressesProvider
    function addressesProvider () external view returns ( address ); // ILendingPool
    function flashLoan(address _receiver, address _reserve, uint256 _amount, bytes calldata _params) external; // ILendingPool
}

contract flashTurnaround {

    address ETH=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    address aaveAddr=0x1c8756FD2B28e9426CDBDcC7E3c4d64fa9A54728; // get addresses from Aave Addresses Provider

    constructor () public payable {}

    function turnaround(address[] memory tokenPath, string[] memory exchangePath, uint injectedAmount, uint tradeAmount) public {
        require(tradeAmount>0 && tradeAmount>=injectedAmount); // amounts should be >0
        require(tokenPath[0]==tokenPath[tokenPath.length]); // first and last token must be the same
        ERC20 baseToken=ERC20(tokenPath[0]);

        // injectedAmount : Amount to be sent to the smart contract to perform trades
        if(injectedAmount>0) baseToken.transferFrom(msg.sender, address(this), injectedAmount);
        if(tokenPath[0]!=ETH) baseToken.approve(address(this), tradeAmount);

        // Encode input parameters
        bytes memory params = abi.encode(tokenPath, exchangePath, injectedAmount, tradeAmount);

        // tradeAmount : Wanted amount to perform the trade.
        if(tradeAmount>injectedAmount) // If tradeAmount is higher, than a flashloan will fill the gap
            aaveLinks(aaveLinks(aaveAddr).getLendingPool()).flashLoan(address(this), tokenPath[0], tradeAmount - injectedAmount, params);
        else
            performSwaps(params, 0);
    }

    // Receiver for Aave flash loan
    function executeOperation(address _reserve, uint256 _amount, uint256 _fee, bytes calldata _params) external {
        performSwaps(_params, _fee);

        // Return flash loan
        address corePool = aaveLinks(aaveAddr).getLendingPoolCore();
        if(_reserve!=ETH)
            ERC20(_reserve).transfer(corePool, _amount + _fee);
        else
            payable(corePool).transfer(_amount + _fee);
    }

    function performSwaps(bytes memory params, uint fee) private {
        address[] memory tokenPath; string[] memory exchangePath; uint injectedAmount; uint tradeAmount;
        (tokenPath, exchangePath, injectedAmount, tradeAmount) = abi.decode(params, (address[], string[], uint, uint));

        ERC20 targetToken; // changes along the tokenPath
        for (uint i=0; i<tokenPath.length-1; i++) {
            ERC20 fromToken=ERC20(tokenPath[i]);
            targetToken=ERC20(tokenPath[i+1]);
            if (hashi(exchangePath[i])==hashi("kyberswap")) tradeAmount = kyberSwap(fromToken, targetToken, tradeAmount);
            if (hashi(exchangePath[i])==hashi("uniswap")) tradeAmount = uniswapV2(fromToken, targetToken, tradeAmount);
        }

        // Return remaining Tokens to sender
        if(address(targetToken)!=ETH) targetToken.transfer(msg.sender, tradeAmount-fee);
        else msg.sender.transfer(tradeAmount-fee);
    }

    function kyberSwap(ERC20 fromToken, ERC20 targetToken, uint amount) private returns (uint exchangedAmount) {
        address kyberSC=0x818E6FECD516Ecc3849DAf6845e3EC868087B755;
        SimpleNetworkInterface k = SimpleNetworkInterface(kyberSC);
        fromToken.approve(kyberSC, amount);
        return k.swapTokenToToken(fromToken, amount, targetToken, 0);
    }
    
    function uniswapV2(ERC20 fromToken, ERC20 targetToken, uint amount) private returns (uint exchangedAmount) {
    //    address uniswapSC=0xf164fC0Ec4E93095b804a4795bBe1e041497b92a;
    //    IUniswapV2Router01 u = IUniswapV2Router01(uniswapSC);
    //    fromToken.approve(uniswapSC, amount);
    //    return u.swapExactTokensForTokens(amount,0,[address(this),address(this),address(this)],address(this),0)[1];
    }

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
