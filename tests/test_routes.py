from httpx import AsyncClient
import pytest


@pytest.mark.asyncio(scope="session")
async def test_get_last_trading_dates_route(client: AsyncClient):
    response = await client.get('/get_last_trading_dates?amount=1')
    assert response.status_code == 200
    assert response.json() == ["2024-04-04"]


@pytest.mark.asyncio(scope="session")
async def test_get_dynamics(client: AsyncClient):
    response = await client.get('/get_dynamics?start=2024-02-28&end=2024-03-26')
    assert response.status_code == 200
    assert response.json() == [
        {
            'oil_id': 'A100',
            'delivery_type_id': 'F',
            'delivery_basis_id': 'ANK',
            'start_date': '2024-02-28',
            'end_date': '2024-03-26'
        },
        {
            'oil_id': 'A100',
            'delivery_type_id': 'F',
            'delivery_basis_id': 'ANK',
            'start_date': '2024-02-28',
            'end_date': '2024-03-26'
        }
    ]


@pytest.mark.asyncio(scope="session")
async def test_get_trading_results(client: AsyncClient):
    response = await client.get('/get_trading_results?limit=1')
    assert response.status_code == 200
    assert response.json() == [
        {
            'oil_id': 'A100',
            'delivery_type_id': 'F',
            'delivery_basis_id': 'ANK'
        }
    ]
