import asyncio
import base64
from typing import List
from fastapi import status

from fastapi import APIRouter, UploadFile

from src.web3_transactions.tasks import send_transaction

router = APIRouter(tags=['transaction'], prefix='/transactions')


@router.post('/send', status_code=status.HTTP_200_OK)
async def send_all_transactions(files: List[UploadFile]):
    files_data = [base64.b64encode(file.file.read()).decode() for file in files]
    for file in files_data:
        send_transaction.delay({"file": file})
    return {'msg': 'ok'}
