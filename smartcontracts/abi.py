ABI = [
    {
        "inputs": [],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
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
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "github_hash",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "email_address_hash",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct SBT.PersonalDataHashed",
                "name": "_soulData",
                "type": "tuple"
            }
        ],
        "name": "claim",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_soul_id",
                "type": "uint256"
            }
        ],
        "name": "Claim",
        "type": "event"
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
            }
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_soul_id",
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
                "name": "_soul_id",
                "type": "uint256"
            }
        ],
        "name": "MintAchievement",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_new_address",
                "type": "address"
            }
        ],
        "name": "setAchevementsContractAddress",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "_new_address",
                "type": "address"
            }
        ],
        "name": "SetAchevementsContractAddress",
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
                        "internalType": "uint256",
                        "name": "soul_id",
                        "type": "uint256"
                    },
                    {
                        "components": [
                            {
                                "internalType": "bytes32",
                                "name": "github_hash",
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
        "name": "getUserId",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
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
        "inputs": [],
        "name": "kAchevementsContract",
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
        "inputs": [],
        "name": "verifyDataCorrectness",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "github_hash",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "email_address_hash",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct SBT.PersonalDataHashed",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# [1, 0x41c9288b78090946db0fd6d32D8cB1fEfe18134B, 0x41c9288b78090946db0fd6d32D8cB1fEfe18134B, 'False','url']


ABI3 = [
    {
        "inputs": [],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
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
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "github_hash",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "email_address_hash",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct SBT.PersonalDataHashed",
                "name": "_soulData",
                "type": "tuple"
            }
        ],
        "name": "claim",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_soul_id",
                "type": "uint256"
            }
        ],
        "name": "Claim",
        "type": "event"
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
            }
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_soul_id",
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
                "name": "_soul_id",
                "type": "uint256"
            }
        ],
        "name": "MintAchievement",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_new_address",
                "type": "address"
            }
        ],
        "name": "setAchevementsContractAddress",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "_new_address",
                "type": "address"
            }
        ],
        "name": "SetAchevementsContractAddress",
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
                        "internalType": "uint256",
                        "name": "soul_id",
                        "type": "uint256"
                    },
                    {
                        "components": [
                            {
                                "internalType": "bytes32",
                                "name": "github_hash",
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
        "name": "getUserId",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
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
        "inputs": [],
        "name": "kAchevementsContract",
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
        "inputs": [],
        "name": "verifyDataCorrectness",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "github_hash",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "email_address_hash",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct SBT.PersonalDataHashed",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

achivement_ABI = [
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
            },
            {
                "internalType": "bool",
                "name": "_newStatus",
                "type": "bool"
            }
        ],
        "name": "changeAchievementVerification",
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
                        "name": "issuer",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "owner",
                        "type": "uint256"
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
                        "name": "issuer",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "owner",
                        "type": "uint256"
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
    }
]
