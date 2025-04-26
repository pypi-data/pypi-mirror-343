from pyumlify.generate import extract_structure, scan_project, get_known_external_modules

def test_extract_structure():
    result = extract_structure("tests/fixtures/sample.py")
    assert result is not None
    assert "classes" in result
    assert isinstance(result["classes"], list)

def test_scan_project():
    results = scan_project("tests/fixtures")
    assert isinstance(results, list)
    assert any("classes" in file for file in results)

def test_detect_external_libs_from_requirements():
    libs = get_known_external_modules("tests/fixtures/requirements.txt")
    assert "requests" in libs
    assert "numpy" in libs
    assert "pypdf2" in libs or "PyPDF2".lower() in libs
