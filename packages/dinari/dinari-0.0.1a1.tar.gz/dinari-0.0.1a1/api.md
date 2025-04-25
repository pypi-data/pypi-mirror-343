# API

## V2

Types:

```python
from dinari.types.api import V2GetHealthResponse
```

Methods:

- <code title="get /api/v2/_health/">client.api.v2.<a href="./src/dinari/resources/api/v2/v2.py">get_health</a>() -> <a href="./src/dinari/types/api/v2_get_health_response.py">V2GetHealthResponse</a></code>

### MarketData

Types:

```python
from dinari.types.api.v2 import MarketDataGetMarketHoursResponse
```

Methods:

- <code title="get /api/v2/market_data/market_hours/">client.api.v2.market_data.<a href="./src/dinari/resources/api/v2/market_data/market_data.py">get_market_hours</a>() -> <a href="./src/dinari/types/api/v2/market_data_get_market_hours_response.py">MarketDataGetMarketHoursResponse</a></code>

#### Stocks

Types:

```python
from dinari.types.api.v2.market_data import (
    StockListResponse,
    StockRetrieveDividendsResponse,
    StockRetrieveHistoricalPricesResponse,
    StockRetrieveNewsResponse,
    StockRetrieveQuoteResponse,
)
```

Methods:

- <code title="get /api/v2/market_data/stocks/">client.api.v2.market_data.stocks.<a href="./src/dinari/resources/api/v2/market_data/stocks/stocks.py">list</a>(\*\*<a href="src/dinari/types/api/v2/market_data/stock_list_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/market_data/stock_list_response.py">StockListResponse</a></code>
- <code title="get /api/v2/market_data/stocks/{stock_id}/dividends">client.api.v2.market_data.stocks.<a href="./src/dinari/resources/api/v2/market_data/stocks/stocks.py">retrieve_dividends</a>(stock_id) -> <a href="./src/dinari/types/api/v2/market_data/stock_retrieve_dividends_response.py">StockRetrieveDividendsResponse</a></code>
- <code title="get /api/v2/market_data/stocks/{stock_id}/historical_prices/">client.api.v2.market_data.stocks.<a href="./src/dinari/resources/api/v2/market_data/stocks/stocks.py">retrieve_historical_prices</a>(stock_id, \*\*<a href="src/dinari/types/api/v2/market_data/stock_retrieve_historical_prices_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/market_data/stock_retrieve_historical_prices_response.py">StockRetrieveHistoricalPricesResponse</a></code>
- <code title="get /api/v2/market_data/stocks/{stock_id}/news">client.api.v2.market_data.stocks.<a href="./src/dinari/resources/api/v2/market_data/stocks/stocks.py">retrieve_news</a>(stock_id, \*\*<a href="src/dinari/types/api/v2/market_data/stock_retrieve_news_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/market_data/stock_retrieve_news_response.py">StockRetrieveNewsResponse</a></code>
- <code title="get /api/v2/market_data/stocks/{stock_id}/quote">client.api.v2.market_data.stocks.<a href="./src/dinari/resources/api/v2/market_data/stocks/stocks.py">retrieve_quote</a>(stock_id) -> <a href="./src/dinari/types/api/v2/market_data/stock_retrieve_quote_response.py">StockRetrieveQuoteResponse</a></code>

##### Splits

Types:

```python
from dinari.types.api.v2.market_data.stocks import (
    StockSplit,
    SplitRetrieveResponse,
    SplitListResponse,
)
```

Methods:

- <code title="get /api/v2/market_data/stocks/{stock_id}/splits">client.api.v2.market_data.stocks.splits.<a href="./src/dinari/resources/api/v2/market_data/stocks/splits.py">retrieve</a>(stock_id, \*\*<a href="src/dinari/types/api/v2/market_data/stocks/split_retrieve_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/market_data/stocks/split_retrieve_response.py">SplitRetrieveResponse</a></code>
- <code title="get /api/v2/market_data/stocks/splits">client.api.v2.market_data.stocks.splits.<a href="./src/dinari/resources/api/v2/market_data/stocks/splits.py">list</a>(\*\*<a href="src/dinari/types/api/v2/market_data/stocks/split_list_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/market_data/stocks/split_list_response.py">SplitListResponse</a></code>

### Entities

Types:

```python
from dinari.types.api.v2 import Entity, EntityListResponse
```

Methods:

- <code title="post /api/v2/entities/">client.api.v2.entities.<a href="./src/dinari/resources/api/v2/entities/entities.py">create</a>(\*\*<a href="src/dinari/types/api/v2/entity_create_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/entity.py">Entity</a></code>
- <code title="get /api/v2/entities/{entity_id}">client.api.v2.entities.<a href="./src/dinari/resources/api/v2/entities/entities.py">retrieve</a>(entity_id) -> <a href="./src/dinari/types/api/v2/entity.py">Entity</a></code>
- <code title="get /api/v2/entities/">client.api.v2.entities.<a href="./src/dinari/resources/api/v2/entities/entities.py">list</a>() -> <a href="./src/dinari/types/api/v2/entity_list_response.py">EntityListResponse</a></code>
- <code title="get /api/v2/entities/me">client.api.v2.entities.<a href="./src/dinari/resources/api/v2/entities/entities.py">retrieve_current</a>() -> <a href="./src/dinari/types/api/v2/entity.py">Entity</a></code>

#### Accounts

Types:

```python
from dinari.types.api.v2.entities import Account, AccountListResponse
```

Methods:

- <code title="post /api/v2/entities/{entity_id}/accounts">client.api.v2.entities.accounts.<a href="./src/dinari/resources/api/v2/entities/accounts.py">create</a>(entity_id) -> <a href="./src/dinari/types/api/v2/entities/account.py">Account</a></code>
- <code title="get /api/v2/entities/{entity_id}/accounts">client.api.v2.entities.accounts.<a href="./src/dinari/resources/api/v2/entities/accounts.py">list</a>(entity_id, \*\*<a href="src/dinari/types/api/v2/entities/account_list_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/entities/account_list_response.py">AccountListResponse</a></code>

#### KYC

Types:

```python
from dinari.types.api.v2.entities import (
    KYCData,
    KYCDocumentType,
    KYCInfo,
    KYCGetURLResponse,
    KYCUploadDocumentResponse,
)
```

Methods:

- <code title="get /api/v2/entities/{entity_id}/kyc">client.api.v2.entities.kyc.<a href="./src/dinari/resources/api/v2/entities/kyc.py">retrieve</a>(entity_id) -> <a href="./src/dinari/types/api/v2/entities/kyc_info.py">KYCInfo</a></code>
- <code title="get /api/v2/entities/{entity_id}/kyc/url">client.api.v2.entities.kyc.<a href="./src/dinari/resources/api/v2/entities/kyc.py">get_url</a>(entity_id) -> <a href="./src/dinari/types/api/v2/entities/kyc_get_url_response.py">KYCGetURLResponse</a></code>
- <code title="post /api/v2/entities/{entity_id}/kyc">client.api.v2.entities.kyc.<a href="./src/dinari/resources/api/v2/entities/kyc.py">submit</a>(entity_id, \*\*<a href="src/dinari/types/api/v2/entities/kyc_submit_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/entities/kyc_info.py">KYCInfo</a></code>
- <code title="post /api/v2/entities/{entity_id}/kyc/{kyc_id}/document">client.api.v2.entities.kyc.<a href="./src/dinari/resources/api/v2/entities/kyc.py">upload_document</a>(kyc_id, \*, entity_id, \*\*<a href="src/dinari/types/api/v2/entities/kyc_upload_document_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/entities/kyc_upload_document_response.py">KYCUploadDocumentResponse</a></code>

### Accounts

Types:

```python
from dinari.types.api.v2 import (
    AccountRetrieveCashResponse,
    AccountRetrieveDividendPaymentsResponse,
    AccountRetrieveInterestPaymentsResponse,
    AccountRetrievePortfolioResponse,
)
```

Methods:

- <code title="get /api/v2/accounts/{account_id}">client.api.v2.accounts.<a href="./src/dinari/resources/api/v2/accounts/accounts.py">retrieve</a>(account_id) -> <a href="./src/dinari/types/api/v2/entities/account.py">Account</a></code>
- <code title="post /api/v2/accounts/{account_id}/deactivate">client.api.v2.accounts.<a href="./src/dinari/resources/api/v2/accounts/accounts.py">deactivate</a>(account_id) -> <a href="./src/dinari/types/api/v2/entities/account.py">Account</a></code>
- <code title="get /api/v2/accounts/{account_id}/cash">client.api.v2.accounts.<a href="./src/dinari/resources/api/v2/accounts/accounts.py">retrieve_cash</a>(account_id) -> <a href="./src/dinari/types/api/v2/account_retrieve_cash_response.py">AccountRetrieveCashResponse</a></code>
- <code title="get /api/v2/accounts/{account_id}/dividend_payments">client.api.v2.accounts.<a href="./src/dinari/resources/api/v2/accounts/accounts.py">retrieve_dividend_payments</a>(account_id) -> <a href="./src/dinari/types/api/v2/account_retrieve_dividend_payments_response.py">AccountRetrieveDividendPaymentsResponse</a></code>
- <code title="get /api/v2/accounts/{account_id}/interest_payments">client.api.v2.accounts.<a href="./src/dinari/resources/api/v2/accounts/accounts.py">retrieve_interest_payments</a>(account_id) -> <a href="./src/dinari/types/api/v2/account_retrieve_interest_payments_response.py">AccountRetrieveInterestPaymentsResponse</a></code>
- <code title="get /api/v2/accounts/{account_id}/portfolio">client.api.v2.accounts.<a href="./src/dinari/resources/api/v2/accounts/accounts.py">retrieve_portfolio</a>(account_id) -> <a href="./src/dinari/types/api/v2/account_retrieve_portfolio_response.py">AccountRetrievePortfolioResponse</a></code>

#### Wallet

Types:

```python
from dinari.types.api.v2.accounts import Wallet
```

Methods:

- <code title="get /api/v2/accounts/{account_id}/wallet">client.api.v2.accounts.wallet.<a href="./src/dinari/resources/api/v2/accounts/wallet/wallet.py">retrieve</a>(account_id) -> <a href="./src/dinari/types/api/v2/accounts/wallet/wallet.py">Wallet</a></code>

##### External

Types:

```python
from dinari.types.api.v2.accounts.wallet import ExternalGetNonceResponse
```

Methods:

- <code title="post /api/v2/accounts/{account_id}/wallet/external">client.api.v2.accounts.wallet.external.<a href="./src/dinari/resources/api/v2/accounts/wallet/external.py">connect</a>(account_id, \*\*<a href="src/dinari/types/api/v2/accounts/wallet/external_connect_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/accounts/wallet/wallet.py">Wallet</a></code>
- <code title="get /api/v2/accounts/{account_id}/wallet/external/nonce">client.api.v2.accounts.wallet.external.<a href="./src/dinari/resources/api/v2/accounts/wallet/external.py">get_nonce</a>(account_id, \*\*<a href="src/dinari/types/api/v2/accounts/wallet/external_get_nonce_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/accounts/wallet/external_get_nonce_response.py">ExternalGetNonceResponse</a></code>

#### Orders

Types:

```python
from dinari.types.api.v2.accounts import (
    Order,
    OrderListResponse,
    OrderGetEstimatedFeeResponse,
    OrderRetrieveFulfillmentsResponse,
)
```

Methods:

- <code title="get /api/v2/accounts/{account_id}/orders/{order_id}">client.api.v2.accounts.orders.<a href="./src/dinari/resources/api/v2/accounts/orders.py">retrieve</a>(order_id, \*, account_id) -> <a href="./src/dinari/types/api/v2/accounts/order.py">Order</a></code>
- <code title="get /api/v2/accounts/{account_id}/orders">client.api.v2.accounts.orders.<a href="./src/dinari/resources/api/v2/accounts/orders.py">list</a>(account_id) -> <a href="./src/dinari/types/api/v2/accounts/order_list_response.py">OrderListResponse</a></code>
- <code title="post /api/v2/accounts/{account_id}/orders/{order_id}/cancel">client.api.v2.accounts.orders.<a href="./src/dinari/resources/api/v2/accounts/orders.py">cancel</a>(order_id, \*, account_id) -> <a href="./src/dinari/types/api/v2/accounts/order.py">Order</a></code>
- <code title="post /api/v2/accounts/{account_id}/orders/estimated_fee">client.api.v2.accounts.orders.<a href="./src/dinari/resources/api/v2/accounts/orders.py">get_estimated_fee</a>(account_id, \*\*<a href="src/dinari/types/api/v2/accounts/order_get_estimated_fee_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/accounts/order_get_estimated_fee_response.py">OrderGetEstimatedFeeResponse</a></code>
- <code title="get /api/v2/accounts/{account_id}/orders/{order_id}/fulfillments">client.api.v2.accounts.orders.<a href="./src/dinari/resources/api/v2/accounts/orders.py">retrieve_fulfillments</a>(order_id, \*, account_id) -> <a href="./src/dinari/types/api/v2/accounts/order_retrieve_fulfillments_response.py">OrderRetrieveFulfillmentsResponse</a></code>

#### OrderFulfillments

Types:

```python
from dinari.types.api.v2.accounts import OrderFulfillment, OrderFulfillmentQueryResponse
```

Methods:

- <code title="get /api/v2/accounts/{account_id}/order_fulfillments/{fulfillment_id}">client.api.v2.accounts.order_fulfillments.<a href="./src/dinari/resources/api/v2/accounts/order_fulfillments.py">retrieve</a>(fulfillment_id, \*, account_id) -> <a href="./src/dinari/types/api/v2/accounts/order_fulfillment.py">OrderFulfillment</a></code>
- <code title="get /api/v2/accounts/{account_id}/order_fulfillments">client.api.v2.accounts.order_fulfillments.<a href="./src/dinari/resources/api/v2/accounts/order_fulfillments.py">query</a>(account_id) -> <a href="./src/dinari/types/api/v2/accounts/order_fulfillment_query_response.py">OrderFulfillmentQueryResponse</a></code>

#### OrderRequests

Types:

```python
from dinari.types.api.v2.accounts import (
    LimitOrderRequestInput,
    OrderRequest,
    OrderRequestListResponse,
)
```

Methods:

- <code title="get /api/v2/accounts/{account_id}/order_requests/{request_id}">client.api.v2.accounts.order_requests.<a href="./src/dinari/resources/api/v2/accounts/order_requests.py">retrieve</a>(request_id, \*, account_id) -> <a href="./src/dinari/types/api/v2/accounts/order_request.py">OrderRequest</a></code>
- <code title="get /api/v2/accounts/{account_id}/order_requests">client.api.v2.accounts.order_requests.<a href="./src/dinari/resources/api/v2/accounts/order_requests.py">list</a>(account_id) -> <a href="./src/dinari/types/api/v2/accounts/order_request_list_response.py">OrderRequestListResponse</a></code>
- <code title="post /api/v2/accounts/{account_id}/order_requests/limit_buy">client.api.v2.accounts.order_requests.<a href="./src/dinari/resources/api/v2/accounts/order_requests.py">create_limit_buy</a>(account_id, \*\*<a href="src/dinari/types/api/v2/accounts/order_request_create_limit_buy_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/accounts/order_request.py">OrderRequest</a></code>
- <code title="post /api/v2/accounts/{account_id}/order_requests/limit_sell">client.api.v2.accounts.order_requests.<a href="./src/dinari/resources/api/v2/accounts/order_requests.py">create_limit_sell</a>(account_id, \*\*<a href="src/dinari/types/api/v2/accounts/order_request_create_limit_sell_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/accounts/order_request.py">OrderRequest</a></code>
- <code title="post /api/v2/accounts/{account_id}/order_requests/market_buy">client.api.v2.accounts.order_requests.<a href="./src/dinari/resources/api/v2/accounts/order_requests.py">create_market_buy</a>(account_id, \*\*<a href="src/dinari/types/api/v2/accounts/order_request_create_market_buy_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/accounts/order_request.py">OrderRequest</a></code>
- <code title="post /api/v2/accounts/{account_id}/order_requests/market_sell">client.api.v2.accounts.order_requests.<a href="./src/dinari/resources/api/v2/accounts/order_requests.py">create_market_sell</a>(account_id, \*\*<a href="src/dinari/types/api/v2/accounts/order_request_create_market_sell_params.py">params</a>) -> <a href="./src/dinari/types/api/v2/accounts/order_request.py">OrderRequest</a></code>
