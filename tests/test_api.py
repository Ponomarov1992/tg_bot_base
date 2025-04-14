import pytest

from src.api import CRMApi


@pytest.mark.asyncio
async def test_create_client_ok(mocker):
    expected = {'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'phone_number': '+1234567890'}
    mocker.patch('src.api.crm_request', return_value=(True, expected))
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '+1234567890',
        'telegram_data': {'tg_id': 12345, 'username': 'tg-username', 'language_code': 'en'},
    }

    is_success, resp = await CRMApi().create_client(data)

    assert is_success
    assert resp['id'] == 1
    assert resp['first_name'] == data['first_name']
    assert resp['last_name'] == data['last_name']
    assert resp['phone_number'] == data['phone_number']


@pytest.mark.asyncio
async def test_create_client_fail(mocker):
    mocker.patch('src.api.crm_request', return_value=(False, {'error': 'Some error'}))
    data = {'error-data': 'Some data'}

    is_success, resp = await CRMApi().create_client(data)

    assert not is_success
    assert resp == {'error': 'Some error'}


@pytest.mark.asyncio
async def test_create_consultation_ok(mocker):
    expected = {'id': 1, 'client_note': 'Some note', 'client': 1}
    mocker.patch('src.api.crm_request', return_value=(True, expected))
    data = {'client_note': 'Some note', 'client': 1}

    is_success, resp = await CRMApi().create_consultation(data)

    assert is_success
    assert resp['id'] == 1
    assert resp['client_note'] == data['client_note']
    assert resp['client'] == data['client']


@pytest.mark.asyncio
async def test_create_consultation_fail(mocker):
    mocker.patch('src.api.crm_request', return_value=(False, {'error': 'Some error'}))
    data = {'error-data': 'Some data'}

    is_success, resp = await CRMApi().create_consultation(data)

    assert not is_success
    assert resp == {'error': 'Some error'}


@pytest.mark.asyncio
async def test_get_client_by_tg_id_ok(mocker):
    expected = {'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'phone_number': '+1234567890'}
    response = {'count': 1, 'results': [expected]}
    mocker.patch('src.api.crm_request', return_value=(True, response))

    resp = await CRMApi().get_client_by_tg_id(12345)

    assert resp == expected


@pytest.mark.asyncio
async def test_get_client_by_tg_id_fail(mocker):
    response = {'count': 0, 'results': []}
    mocker.patch('src.api.crm_request', return_value=(True, response))

    resp = await CRMApi().get_client_by_tg_id(12345)

    assert resp == {}
