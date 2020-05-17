pragma solidity ^0.6.6;

interface ERC20 {
    function transfer(address _to, uint _value) external returns (bool success);
    function approve(address _spender, uint _value) external returns (bool success);
}
interface FlashStart {
    function flashLoan(address _receiver, address _reserve, uint256 _amount, bytes calldata _params) external;
}

// Minimalistic Contract to get a FlashLoan from Aave on Ropsten Testnet
// Please fund the contract with ETH or one of the currentcies below before executing.
// Addresses have to be adjusted for mainnet

contract miniFlash {

    //address DAI=0xf80A32A835F79D7787E8a8ee5721D0fEaFd78108;
    //address USDT=0xB404c51BBC10dcBE948077F18a4B8E553D160084;
    //address TUSD=0xa51EE1845C13Cb03FcA998304b00EcC407fc1F92;
    address ETH=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    constructor() public {}

    function startFlash(address startToken) public {
        if(startToken!=ETH) ERC20(startToken).approve(address(this), 200000000);
        FlashStart(0x9E5C7835E4b13368fd628196C4f1c6cEc89673Fa).flashLoan(address(this), startToken, 20000, abi.encode(startToken)); // get from LendingPool 0x9E5C7835E4b13368fd628196C4f1c6cEc89673Fa
    }

    // Receiver for flashLoan as defined by Aave
    function executeOperation(address _reserve, uint256 _amount, uint256 _fee, bytes calldata _params) external {
        address startToken;(startToken)=abi.decode(_params, (address));
        if(startToken!=ETH)
            ERC20(_reserve).transfer(0x4295Ee704716950A4dE7438086d6f0FBC0BA9472, _amount + _fee); // Send to LendingPoolCore 0x4295Ee704716950A4dE7438086d6f0FBC0BA9472
        else
            (0x4295Ee704716950A4dE7438086d6f0FBC0BA9472).transfer(_amount + _fee);
    }

    function giveMeEth() public payable {} // Necessary in order to send ETH to the smart contract
}