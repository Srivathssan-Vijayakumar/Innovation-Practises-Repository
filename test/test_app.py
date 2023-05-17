import pytest
from app import validate_linestring, calculate_offset

def test_validate_linestring():
    valid_input = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    assert validate_linestring(valid_input) == True

    additional_properties = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]], "properties": {"name": "Test Line"}}'
    assert validate_linestring(additional_properties) == True

    invalid_type = '{"type":"Polygon","coordinates":[[[30,10],[40,40],[20,40],[10,20],[30,10]]]}'
    assert validate_linestring(invalid_type) == False

    invalid_longcoordinates = '{"type":"LineString","coordinates":[[200,40.7414944],[-89.45986751186378,95],[-89.45982903706444,40.74168799589157]]}'
    assert validate_linestring(invalid_coordinates) == False

    invalid_latcoordinates = '{"type":"LineString","coordinates":[[-89.4599889,100.7414944],[-89.45986751186378,140.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    assert validate_linestring(invalid_coordinates) == False

    empty_input = ""
    assert validate_linestring(empty_input) == False

    incorrect_json_object = '[{"type":"LineString"},{"coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}]'
    assert validate_linestring(incorrect_json_object) == False

    insufficient_coordinates = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944]]}'
    assert validate_linestring(insufficient_coordinates) == False

    non_numeric_coordinates = '{"type":"LineString","coordinates":[["A", 40.7414944],[-89.45986751186378, "B"]]}'
    assert validate_linestring(non_numeric_coordinates) == False

    extra_dimensions = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944, 100],[-89.45986751186378,40.74164593253394, 100],[-89.45982903706444,40.74168799589157, 100]]}'
    assert validate_linestring(extra_dimensions) == False

    nested_linestring = '{"type":"Feature","geometry":{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}}'
    assert validate_linestring(nested_linestring) == False

    empty_coordinates = '{"type":"LineString","coordinates":[]}'
    assert validate_linestring(empty_coordinates) == False


def test_calculate_offset_zero_buffer():
    linestring = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    buffer_distance = 0

    with pytest.raises(ValueError):
        calculate_offset(linestring, buffer_distance)

def test_calculate_offset_negative_buffer():
    linestring = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    buffer_distance = -1

    with pytest.raises(ValueError):
        calculate_offset(linestring, buffer_distance)

def test_calculate_offset_large_linestring():
    large_linestring = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157],[-89.4597889,40.741444],[-89.45987751186378,40.74184593253394],[-89.45972903706444,40.74178799589157]]}'
    buffer_distance = 5.0
    result = calculate_offset(large_linestring, buffer_distance)
    assert "format_3857" in result and "format_4326" in result


def test_calculate_offset_expected_keys_left_right():
    linestring = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    buffer_distance = 2.2
    result = calculate_offset(linestring, buffer_distance)
    assert "left" in result["format_3857"] and "right" in result["format_3857"]
    assert "left" in result["format_4326"] and "right" in result["format_4326"]


def test_calculate_offset_expected_keys_coordinates():
    linestring = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    buffer_distance = 2.2
    result = calculate_offset(linestring, buffer_distance)
    assert "coordinates" in result["format_3857"]["left"] and "coordinates" in result["format_3857"]["right"]
    assert "coordinates" in result["format_4326"]["left"] and "coordinates" in result["format_4326"]["right"]


def test_calculate_offset_expected_keys_type():
    linestring = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    buffer_distance = 2.2
    result = calculate_offset(linestring, buffer_distance)
    assert "type" in result["format_3857"]["left"] and "type" in result["format_3857"]["right"]
    assert "type" in result["format_4326"]["left"] and "type" in result["format_4326"]["right"]

def test_calculate_offset_small_buffer():
    linestring = '{"type":"LineString","coordinates":[[-89.4599889,40.7414944],[-89.45986751186378,40.74164593253394],[-89.45982903706444,40.74168799589157]]}'
    buffer_distance = 0.001
    result = calculate_offset(linestring, buffer_distance)
    assert result["format_4326"]["left"]["coordinates"] != result["format_4326"]["right"]["coordinates"]
