from unittest.mock import patch
import requests
import caretrack

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError()

def test_get_weather_advice_hot():
    # Mockando uma resposta da API indicando clima muito quente
    mock_data = {"current_weather": {"temperature": 32.5}}
    
    with patch('requests.get', return_value=MockResponse(mock_data, 200)):
        result = caretrack.get_weather_advice()
        assert result == "hot"

def test_get_weather_advice_cold():
    # Mockando uma resposta da API indicando clima frio
    mock_data = {"current_weather": {"temperature": 10.0}}
    
    with patch('requests.get', return_value=MockResponse(mock_data, 200)):
        result = caretrack.get_weather_advice()
        assert result == "cold"

def test_get_weather_advice_normal():
    # Mockando clima ameno
    mock_data = {"current_weather": {"temperature": 22.0}}
    
    with patch('requests.get', return_value=MockResponse(mock_data, 200)):
        result = caretrack.get_weather_advice()
        assert result == "normal"

def test_get_weather_advice_api_error():
    # Simulando um erro na requisição à API
    with patch('requests.get', side_effect=requests.RequestException("Erro simulado")):
        result = caretrack.get_weather_advice()
        assert result == "error"
