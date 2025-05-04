# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

import csv
from typing import (
    List,
    Dict,
    Any
)

# =============== // LIBRARY IMPORT // ===============

from sqlmodel import (
    Session,
    select
)
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException
)

# =============== // MODULE IMPORT // ===============

import modules.db as db
import modules.stock as sm
from dependencies import (
    verify_token,
    get_session
)

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


# =============== // ROUTES // ===============

@router.get(
    "/",
    response_model=List[db.schema.StockRead]
)
def read_stocks(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    stocks: List[db.schema.StockRead] = session.exec(
        select(
            db.schema.Stocks
        ).offset(
            skip
        ).limit(
            limit
        )
    ).all()
    return stocks


@router.get(
    "/{ticker}",
    response_model=db.schema.StockRead
)
def read_stock(
    ticker: str,
    session: Session = Depends(get_session)
):
    stock: db.schema.StockRead = session.exec(
        select(
            db.schema.Stocks
        ).where(
            db.schema.Stocks.ticker == ticker
        )
    ).first()

    if not stock:
        stock_data: Dict = sm.stock(ticker).model_dump()
        if stock_data["price"] is None:
            raise HTTPException(
                status_code=404,
                detail="Stock not found"
            )
        new_stock: db.schema.Stocks = db.schema.Stocks(
            **stock_data | {
                "ticker": ticker
            }
        )
        session.add(new_stock)
        session.commit()
        session.refresh(new_stock)
        return new_stock
    return stock


@router.post(
    "/bulk",
    response_model=Dict[str, Any],
    status_code=201
)
async def upload_stocks_csv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are accepted"
        )

    # Read and decode the file content
    content = await file.read()
    try:
        text_content = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded"
        )

    # Parse CSV content
    reader = csv.reader(text_content.splitlines())
    tickers = [row[0].strip() for row in reader if row and row[0].strip()]

    if not tickers:
        raise HTTPException(
            status_code=400,
            detail="No tickers found in the CSV file"
        )

    # Begin transaction
    added_stocks = []
    failed_tickers = []

    try:
        # Process each ticker
        for ticker in tickers:
            # Check if ticker already exists
            existing_stock = session.exec(
                select(db.schema.Stocks).where(db.schema.Stocks.ticker == ticker)
            ).first()

            if existing_stock:
                continue  # Skip existing tickers

            # Fetch stock data
            stock_data = sm.stock(ticker).model_dump()
            if stock_data["price"] is None:
                failed_tickers.append(ticker)
                continue

            # Create new stock entry
            new_stock = db.schema.Stocks(
                **stock_data | {
                    "ticker": ticker
                }
            )
            session.add(new_stock)
            added_stocks.append(ticker)

        # If any tickers failed, rollback the transaction
        if failed_tickers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid tickers found: {', '.join(failed_tickers)}"
            )

        # Commit the transaction
        session.commit()

        return {
            "status": "success",
            "added_stocks": added_stocks,
            "total_added": len(added_stocks)
        }

    except Exception as e:
        session.rollback()
        raise e
