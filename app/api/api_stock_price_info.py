from fastapi import APIRouter, Depends
from app.schemas.stock_price_data import StockPriceInputData, StockPriceOutputData
from app.services.price_data_retrieval import PriceDataRetriever
# from app.load.load_retriever import get_retriever

router = APIRouter()


@router.post("/stockPriceData", response_model=StockPriceOutputData, status_code=200)
async def get_stock_price_data(
        input_data: StockPriceInputData,
        price_retriever_service: PriceDataRetriever = Depends()
):
    return await price_retriever_service.retrieve(input_data)

