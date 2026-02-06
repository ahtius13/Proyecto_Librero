from src.persistence.json_functions import JsonFunctions

def test_json_inicia_vacio(tmp_path):
    file = tmp_path / "test.json"
    repo = JsonFunctions(file)

    assert repo.get_all() == []

def test_guardar_y_leer_datos(tmp_path):
    file = tmp_path / "test.json"
    repo = JsonFunctions(file)

    data = [{"a": 1}, {"b": 2}]
    repo.save_all(data)

    assert repo.get_all() == data

def test_sobrescribe_contenido(tmp_path):
    file = tmp_path / "test.json"
    repo = JsonFunctions(file)

    repo.save_all([{"a": 1}])
    repo.save_all([{"b": 2}])

    assert repo.get_all() == [{"b": 2}]