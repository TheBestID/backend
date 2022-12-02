ABI_ACH = [
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
                "name": "achievement_id",
                "type": "uint256"
            }
        ],
        "name": "Accept",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "achievement_id",
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
                "internalType": "uint256",
                "name": "achievement_id",
                "type": "uint256"
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
                "name": "achievement_id",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "newOwners",
                "type": "uint256[]"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "newAchievementIds",
                "type": "uint256[]"
            }
        ],
        "name": "Split",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "achievement_id",
                "type": "uint256"
            }
        ],
        "name": "Update",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "achievement_id",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "balance_send",
                "type": "uint256"
            }
        ],
        "name": "Verify",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_achievementId",
                "type": "uint256"
            }
        ],
        "name": "acceptAchievement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_achievementId",
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
                "name": "_achievementId",
                "type": "uint256"
            }
        ],
        "name": "getAchievementInfo",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "achievement_id",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "achievement_type",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "issuer",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "owner",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "is_accepted",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "verifier",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "is_verified",
                        "type": "bool"
                    },
                    {
                        "internalType": "string",
                        "name": "data_address",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "balance",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct SBT_achievement.Achievement",
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
                "name": "_issuer",
                "type": "address"
            }
        ],
        "name": "getAchievementsOfIssuer",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "getAchievementsOfOwner",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "kSBTContract",
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
                        "internalType": "uint256",
                        "name": "achievement_id",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "achievement_type",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "issuer",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "owner",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "is_accepted",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "verifier",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "is_verified",
                        "type": "bool"
                    },
                    {
                        "internalType": "string",
                        "name": "data_address",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "balance",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct SBT_achievement.Achievement",
                "name": "_achievementData",
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
                "internalType": "uint256",
                "name": "_achievementId",
                "type": "uint256"
            }
        ],
        "name": "replenishAchievementBalance",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_new_address",
                "type": "address"
            }
        ],
        "name": "setSBTContractAddress",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_achievementId",
                "type": "uint256"
            },
            {
                "internalType": "uint256[]",
                "name": "_newOwners",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256[]",
                "name": "_newAchievementIds",
                "type": "uint256[]"
            }
        ],
        "name": "splitAchievement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_achievementId",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_newOwner",
                "type": "address"
            }
        ],
        "name": "updateOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_achievementId",
                "type": "uint256"
            }
        ],
        "name": "verifyAchievement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
