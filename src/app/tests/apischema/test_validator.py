from apischema.validator import validate_todo_entry


def test_short_summary_in_todo_entry() -> None:
    data = {
        "summary": "Lo",
        "detail": "",
        "tags": [],
    }

    error = validate_todo_entry(raw_data=data)
    assert error.path == "summary"
    assert "maxLength" in error.validation_schema
    assert "minLength" in error.validation_schema
    assert "type" in error.validation_schema


def test_tags_are_not_array() -> None:
    data = {
        "summary": "Lorem Ipsum",
        "detail": "",
        "tags": "important",
    }

    error = validate_todo_entry(raw_data=data)
    assert error.path == "tags"
    assert "type" in error.validation_schema
