ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_soul_id_to_burn",
                "type": "uint256"
            }
        ],
        "name": "Burn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "_soul",
                "type": "address"
            }
        ],
        "name": "Mint",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_soul_id_to_update",
                "type": "uint256"
            }
        ],
        "name": "Update",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_soul_id_to_burn",
                "type": "uint256"
            }
        ],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_soul_id",
                "type": "uint256"
            }
        ],
        "name": "getOwner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_soul",
                "type": "address"
            }
        ],
        "name": "getSoul",
        "outputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "bytes32",
                                "name": "url_hash",
                                "type": "bytes32"
                            },
                            {
                                "internalType": "bytes32",
                                "name": "github_url_hash",
                                "type": "bytes32"
                            },
                            {
                                "internalType": "bytes32",
                                "name": "email_address_hash",
                                "type": "bytes32"
                            }
                        ],
                        "internalType": "struct SBT.PersonalDataHashed",
                        "name": "hashedData",
                        "type": "tuple"
                    }
                ],
                "internalType": "struct SBT.Soul",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_soul",
                "type": "address"
            }
        ],
        "name": "hasSoul",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_soul_address",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_soul_id",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "url",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "github_url",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "email_address",
                        "type": "string"
                    }
                ],
                "internalType": "struct SBT.PersonalData",
                "name": "_soulData",
                "type": "tuple"
            }
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "operator",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "url_hash",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "github_url_hash",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "email_address_hash",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct SBT.PersonalDataHashed",
                "name": "_newSoulData",
                "type": "tuple"
            }
        ],
        "name": "update",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "url",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "github_url",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "email_address",
                        "type": "string"
                    }
                ],
                "internalType": "struct SBT.PersonalData",
                "name": "_dataToVerify",
                "type": "tuple"
            }
        ],
        "name": "verifyDataCorrectness",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]