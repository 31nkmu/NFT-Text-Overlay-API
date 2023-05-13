import json

import ipfsapi
from web3 import Web3

from src.config import ALCHEMY_KEY, PRIVATE_KEY

OWNER = '0x9f2DDe75CeCE586D7d42C340930afB5cC53Eb1cA'
CONTRACT_ADDRESS = '0xE3Af4f8C59c9bdC2B39522dee81f638964cCe841'
PROVIDER_URL = 'https://data-seed-prebsc-1-s1.binance.org:8545/'
with open('abi.json') as f:
    ABI = json.load(f)


def add_file_to_ipfs(file) -> str:
    """Отправляем файл file в ipfs"""
    from io import BytesIO
    bytes_stream = BytesIO(file)

    # Клиент ipfs должен быть запущен на сервере
    api = ipfsapi.Client(host='http://127.0.0.1', port=5001)  # подключение к ipfs
    CID = api.add(bytes_stream)['Hash']
    ipfs_link = "https://ipfs.io/ipfs/" + CID
    return ipfs_link


def send_transaction(file):
    """Отправляем транзакцию в блокчейн"""
    web3 = Web3(Web3.HTTPProvider(PROVIDER_URL))  # подключение к узлу
    contract = web3.eth.contract(CONTRACT_ADDRESS, abi=ABI)  # инициализация контракта
    nonce = web3.eth.get_transaction_count(OWNER)  # количество транзакций пользователя
    dict_transaction = {
        'chainId': web3.eth.chain_id,
        'from': OWNER,
        'value': 0,
        'gasPrice': round(web3.eth.gas_price * 1.1),
        'nonce': nonce,
    }
    ipfs_link = add_file_to_ipfs(file)
    transaction = contract.functions.mint(OWNER, 1, 1, ipfs_link).build_transaction(
        dict_transaction)  # создаем транзакцию
    signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)  # подписываем транзакцию
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()  # отправляем транзакцию
    link_transaction = f'https://testnet.bscscan.com/tx/{txn_hash}'
    print(link_transaction)
    print('******************************************88')
    return link_transaction
