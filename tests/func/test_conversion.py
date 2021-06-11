"""Test stdio prefilters and pandoc filters for Markdown and Docx conversion."""



def test_convert_markdown(convert_fixture, catdiary_fixture):
    """Test prefilters and filters in series against expected output."""
    for item in convert_fixture:
        assert item.values[0] == item.values[1]
