def test_set_is_valid(
    is_valid0,
    is_valid1,
    question_cls,
    tag_name,
    valid_class="is-valid",
    invalid_class="is-invalid",
):
    question = question_cls()
    question.set_is_valid(is_valid0)
    question.set_is_valid(is_valid1)
    classes = question.html_settings[tag_name]["class"]

    if is_valid1 is None:
        assert valid_class not in classes
        assert invalid_class not in classes
    elif is_valid1:
        assert valid_class in classes
        assert invalid_class not in classes
    else:
        # is_valid is False
        assert valid_class not in classes
        assert invalid_class in classes
