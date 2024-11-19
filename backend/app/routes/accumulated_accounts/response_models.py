accumulated_accounts_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "GetAccountListSuccess": {
                        "summary": "Example of a successful response for getting accounts",
                        "value": {
                            "data": [
                                {
                                    "id": 1,
                                    "owner_id": 123,
                                    "amount": 1000.0,
                                    "currency": "USD",
                                    "created_at": "2024-11-12 15:30:00",
                                    "users": {
                                        "owner": {
                                            "name": "Андрей",
                                            "lastname": "Кузнецова"
                                        },
                                        "invited_users": [
                                            {
                                                "name": "Анна",
                                                "lastname": "Иванова",
                                                "role": "просмотр",
                                                "status": "ожидает подтверждения"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "id": 2,
                                    "owner_id": 123,
                                    "amount": 500.0,
                                    "currency": "EUR",
                                    "created_at": "2024-11-13 12:20:00",
                                    "users": {
                                        "owner": {
                                            "name": "Андрей",
                                            "lastname": "Кузнецова"
                                        },
                                        "invited_users": [
                                            {
                                                "name": "Анна",
                                                "lastname": "Иванова",
                                                "role": "просмотр",
                                                "status": "ожидает подтверждения"
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    "CreateAccountSuccess": {
                        "summary": "Example of a successful account creation",
                        "value": {
                            "id": 1,
                            "owner_id": 123,
                            "amount": 1000.0,
                            "currency": "USD",
                            "created_at": "2024-11-12 15:30:00",
                            "users": {
                                "owner": {
                                    "name": "Андрей",
                                    "lastname": "Кузнецова"
                                },
                                "invited_users": [
                                    {
                                        "name": "Анна",
                                        "lastname": "Иванова",
                                        "role": "просмотр",
                                        "status": "ожидает подтверждения"
                                    }
                                ]
                            }
                        }
                    },
                    "DepositSuccess": {
                        "summary": "Example of a successful deposit",
                        "value": {
                            "message": "Funds deposited successfully",
                            "new_balance": 1500.0
                        }
                    },
                    "WithdrawSuccess": {
                        "summary": "Example of a successful withdrawal",
                        "value": {
                            "message": "Funds withdrawn successfully",
                            "new_balance": 500.0
                        }
                    },
                    "InviteUserSuccess": {
                        "summary": "Example of a successful user invitation",
                        "value": {
                            "message": "User invited successfully"
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "InsufficientFunds": {
                        "summary": "Example of an insufficient funds error during withdrawal",
                        "value": {
                            "detail": "Insufficient funds"
                        }
                    },
                    "IntegrityError": {
                        "summary": "Example of a database integrity error during account creation",
                        "value": {
                            "detail": "Failed to create account due to integrity error"
                        }
                    }
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "examples": {
                    "NoPermission": {
                        "summary": "Example of a permission error",
                        "value": {
                            "detail": "No permission to access this account"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "examples": {
                    "UserNotFound": {
                        "summary": "Example of a not found error for an invited user",
                        "value": {
                            "detail": "User to invite not found"
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "examples": {
                    "Unauthorized": {
                        "summary": "Example of an unauthorized error",
                        "value": {
                            "detail": "Unauthorized"
                        }
                    }
                }
            }
        }
    }
}

accumulated_account_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "GetAccountListSuccess": {
                        "summary": "Example of a successful response for getting accounts",
                        "value": {
                            "data": {
                                "id": 1,
                                "owner_id": 123,
                                "amount": 1000.0,
                                "currency": "USD",
                                "created_at": "2024-11-12 15:30:00"
                            }
                        }
                    },
                    "CreateAccountSuccess": {
                        "summary": "Example of a successful account creation",
                        "value": {
                            "id": 1,
                            "owner_id": 123,
                            "amount": 1000.0,
                            "currency": "USD",
                            "created_at": "2024-11-12 15:30:00"
                        }
                    },
                    "DepositSuccess": {
                        "summary": "Example of a successful deposit",
                        "value": {
                            "message": "Funds deposited successfully",
                            "new_balance": 1500.0
                        }
                    },
                    "WithdrawSuccess": {
                        "summary": "Example of a successful withdrawal",
                        "value": {
                            "message": "Funds withdrawn successfully",
                            "new_balance": 500.0
                        }
                    },
                    "InviteUserSuccess": {
                        "summary": "Example of a successful user invitation",
                        "value": {
                            "message": "User invited successfully"
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "InsufficientFunds": {
                        "summary": "Example of an insufficient funds error during withdrawal",
                        "value": {
                            "detail": "Insufficient funds"
                        }
                    },
                    "IntegrityError": {
                        "summary": "Example of a database integrity error during account creation",
                        "value": {
                            "detail": "Failed to create account due to integrity error"
                        }
                    }
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "examples": {
                    "NoPermission": {
                        "summary": "Example of a permission error",
                        "value": {
                            "detail": "No permission to access this account"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "examples": {
                    "UserNotFound": {
                        "summary": "Example of a not found error for an invited user",
                        "value": {
                            "detail": "User to invite not found"
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "examples": {
                    "Unauthorized": {
                        "summary": "Example of an unauthorized error",
                        "value": {
                            "detail": "Unauthorized"
                        }
                    }
                }
            }
        }
    }
}
