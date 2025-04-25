import sys
import os
from unittest.mock import patch 

# Third-party imports
import pytest

# Local application/library specific imports
# This section is to help pytest find your 'tamilkavi' package if needed,
# but installing in "editable" mode (`pip install -e .`) is the standard
# and recommended way to make your package importable for testing.
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, project_root)

# Try importing your main function and KaviExtraction class from your script
try:
    # Import the main function and KaviExtraction class from your script
    # This import needs to succeed for the tests to run.
    from tamilkavi.tamilkavipy import main, KaviExtraction
except ImportError as e:
    # If the import fails, use pytest.fail to stop test execution
    # Include the original error message for better debugging
    pytest.fail(f"Failed to import 'main' or 'KaviExtraction' from 'tamilkavi': {e}. "
                "Ensure your package structure is correct (e.g., "
                "tamilkavi/tamilkavipy.py) and that you have installed your package "
                "in editable mode (`pip install -e .`) from the project root.")

# Add a direct check to confirm the names were defined after import
# This helps diagnose if the ImportError block was bypassed but the names aren't available.
if 'main' not in globals() or 'KaviExtraction' not in globals():
     pytest.fail("Import seemingly succeeded, but 'main' or 'KaviExtraction' "
                 "is not defined in the test scope. Check for potential import "
                 "issues or conditional definitions in tamilkavipy.py.")


# --- Fixture to load data and perform basic structural checks ---
# This fixture runs once per test module and verifies that KaviExtraction
# can be instantiated and loads data with a basic expected structure.
# It prevents subsequent tests from running if data loading fails.
@pytest.fixture(scope="module")
def loaded_kavi_data():
    """Loads KaviExtraction data and verifies basic structure."""
    try:
        # Instantiate the class - this triggers the data loading in __init__
        library = KaviExtraction()
        loaded_data = library.saved_books

        # Basic checks for loaded data structure
        assert isinstance(loaded_data, list), "Loaded data is not a list"
        assert len(loaded_data) > 0, ("No author data loaded from kavisrc. "
                                    "Ensure kavisrc/*.json files exist.")

        # Check if the first item looks like an author dictionary
        first_item = loaded_data[0]
        assert isinstance(first_item, dict), "First item in loaded data is not a dictionary"
        assert 'author' in first_item, "First item in loaded data is missing 'author' key"
        assert 'books' in first_item, "First item in loaded data is missing 'books' key"
        assert isinstance(first_item.get('books'), list), "Author data 'books' is not a list"

        # Check if there is at least one book with context to test poem-related things
        has_book_with_context = False
        for author_data in loaded_data:
            for book_data in author_data.get('books', []):
                if book_data.get('context'):
                    has_book_with_context = True
                    break
            if has_book_with_context:
                break
        assert has_book_with_context, ("No books with poem contexts found in loaded data. "
                                    "Tests for books/poems may fail.")


        return loaded_data # Return the loaded list of author dictionaries

    except SystemExit as e:
        # If sys.exit was called during initialization, fail the test run
        pytest.fail(f"KaviExtraction initialization failed and called sys.exit: {e}. "
                    "Check KaviExtraction.get_books_from_json for data loading errors.")
    except Exception as e:
        # Catch any other unexpected errors during setup
        pytest.fail(f"An unexpected error occurred during KaviExtraction initialization: {e}")


# --- CLI Tests for main() execution ---
# These tests simulate running commands by patching sys.argv and run the main function.
# They use the 'capsys' fixture to capture standard output and standard error.
# They use pytest.raises(SystemExit) to check for expected program exits and their codes.
# These tests rely on the basic structure and *presence* of data loaded by the fixture.

# Test the default command (running 'tamilkavi' with no arguments)
def test_cli_default_command(capsys, loaded_kavi_data):
    """Tests the output and exit behavior of the default command."""
    # Use patch.object to temporarily replace sys.argv within the test
    # Simulate running the command with no arguments
    with patch.object(sys, 'argv', ['tamilkavi']):
        # The default command is expected to print the welcome message and exit with code 0
        with pytest.raises(SystemExit) as e:
            main() # Run the main function

        # Check the exit code (now explicitly 0 in the main function)
        assert e.value.code == 0, f"Expected exit code 0, but got {e.value.code}"

        # Capture the standard output
        captured = capsys.readouterr()

        # Check for key elements of the welcome message in the output
        assert "🙏 Vannakam Makkalayae !" in captured.out
        assert "Welcome to Tamil Kavi 👋" in captured.out
        assert "A command-line tool for exploring Tamil Kavithaigal." in captured.out
        assert "\nTo explore the commands. Check," in captured.out
        assert "👉 tamilkavi -h" in captured.out
        # Ensure nothing else unexpected was printed for the default command
        assert "Available Authors" not in captured.out


# Test the help command ('tamilkavi -h')
def test_cli_help_command(capsys):
    """Tests the output and exit behavior of the help command."""
    # Simulate running with the -h argument
    with patch.object(sys, 'argv', ['tamilkavi', '-h']):
        with pytest.raises(SystemExit) as e:
            # Import main inside the patch to be safe with patching
            from tamilkavi.tamilkavipy import main
            main()

        # Check the exit code
        assert e.value.code == 0, f"Expected exit code 0 for -h, but got {e.value.code}"

        captured = capsys.readouterr()
        output = captured.out # Assign to a variable for easier access

        # Check for key elements of the help message provided by argparse and epilog

        # Check the usage line pattern based on the observed standard argparse output
        assert 'usage: tamilkavi' in output
        assert '[-h]' in output
        # Let's keep the usage line format checks as they seemed reliable before
        assert '[-a [AUTHOR_NAME]]' in output
        assert '[-b [BOOK_TITLE]]' in output
        assert '[-t [POEM_TITLE]]' in output

        # Check the description
        assert "Tamil Kavi CLI - Command Line tool for exploring Tamil Kavithaigal." in output

        # Check for the argument definitions in the main help body
        # FIX: Check for the components of the argument line rather than the exact combined string
        assert '-a, --authors' in output or '--authors, -a' in output
        assert '-b, --book' in output or '--book, -b' in output
        assert '-t, --title' in output or '--title, -t' in output

        # Check that the argument placeholders appear somewhere after the flags
        assert '[AUTHOR_NAME]' in output
        assert '[BOOK_TITLE]' in output
        assert '[POEM_TITLE]' in output


        # Check for parts of the help text for each argument
        assert 'Filter by author name (use -a to list all authors)' in output
        assert 'Filter by book title (use -b to list all books)' in output
        assert 'Filter by poem title (use -t to list all unique titles)' in output

        # Check for the epilog content
        assert "Examples:" in output
        assert "tamilkavi -a \"Author Name\"" in output # Check an example from your epilog

        assert "🙏 Vannakam Makkalayae !" not in output
        assert "Welcome to Tamil Kavi 👋" not in output


# REMOVED: test_cli_list_authors function removed as requested


# Test showing books for a specific author ('tamilkavi -a <author_name>')
def test_cli_show_author_books(capsys, loaded_kavi_data):
    """Tests displaying books for a specific author using dynamically found data."""
    all_data = loaded_kavi_data
    # Dynamically pick the first author name from the loaded data
    author_data = all_data[0]
    author_name = author_data.get('author')
    assert author_name is not None, "Loaded data's first author is missing 'author' key"

    # Check that the author has at least one book to test showing books
    first_author_books = author_data.get('books', [])
    assert len(first_author_books) > 0, f"Author '{author_name}' has no books to test showing books."

    # Get the Tanglish title of the first book by this author
    first_book_tanglish_title = first_author_books[0].get('booktitle_tanglish')
    # Get the Tamil title as well for check if needed
    first_book_tamil_title = first_author_books[0].get('booktitle')
    assert first_book_tanglish_title is not None or first_book_tamil_title is not None, "First book is missing both Tanglish and Tamil titles."

    # Simulate running with -a followed by the author name
    with patch.object(sys, 'argv', ['tamilkavi', '-a', author_name]):
        main() # Run the main function

        # Capture the output
        captured = capsys.readouterr()

        # Check for the author details and book table header
        assert f"✅ Author / Ezhuthalar: {author_name}" in captured.out
        assert "📚 Books / Puthagangal:" in captured.out
        assert "Book Title (Tanglish)" in captured.out # Part of the table header

        # Check that the book title(s) of the first book by this author are in the output
        if first_book_tanglish_title:
             assert first_book_tanglish_title in captured.out
        if first_book_tamil_title:
             assert first_book_tamil_title in captured.out

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test showing poems for a specific book ('tamilkavi -b <book_title_tanglish>')
def test_cli_show_book_poems(capsys, loaded_kavi_data):
    """Tests displaying poems for a specific book using dynamically found data."""
    all_data = loaded_kavi_data
    # Find the first book with a Tanglish title and some context to test
    book_title_tanglish = None
    first_poem_title = None
    for author_data in all_data:
         for book_data in author_data.get('books', []):
              if book_data.get('booktitle_tanglish') and book_data.get('context'):
                   book_title_tanglish = book_data['booktitle_tanglish']
                   # Find the title of the first poem in this book's context
                   if book_data['context']:
                       first_poem_title = book_data['context'][0].get('title')
                   break # Found a suitable book
         if book_title_tanglish:
              break # Stop searching authors

    assert book_title_tanglish is not None, "Could not find a book with Tanglish title and context to test showing poems."
    assert first_poem_title is not None, "The first suitable book found is missing a title in its first poem context."


    # Simulate running with -b followed by the book title
    with patch.object(sys, 'argv', ['tamilkavi', '-b', book_title_tanglish]):
        main() # Run the main function

        # Capture the output
        captured = capsys.readouterr()

        # Check for book details and poem table header
        assert f"✅ Book Title (Tanglish): {book_title_tanglish}" in captured.out
        assert "📜 Poems / Kavithaigal:" in captured.out
        assert "Kavithai Title" in captured.out # Part of the poem table header
        assert first_poem_title in captured.out # Check for the first poem title in the output

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test showing poems for a specific title ('tamilkavi -t <poem_title>')
def test_cli_show_poems_by_title(capsys, loaded_kavi_data):
    """Tests displaying poems filtered by title using dynamically found data."""
    all_data = loaded_kavi_data
    # Find the title of the first poem with a title to test
    poem_title = None
    for author_data in all_data:
         for book_data in author_data.get('books', []):
              for poem_data in book_data.get('context', []):
                   if poem_data.get('title'):
                        poem_title = poem_data['title']
                        break # Found a suitable poem title
              if poem_title:
                   break # Stop searching books
         if poem_title:
              break # Stop searching authors

    assert poem_title is not None, "Could not find a poem with a title to test showing poems by title."

    # Simulate running with -t followed by the poem title
    with patch.object(sys, 'argv', ['tamilkavi', '-t', poem_title]):
        main() # Run the main function

        captured = capsys.readouterr()

        # Check for the poem title filter confirmation and poem table header
        assert f"✅ Filtered by Title: {poem_title}" in captured.out
        assert "Kavithai Title" in captured.out # Poem table header
        # Check that the poem title appears in the output lines (likely in the table)
        assert poem_title in captured.out

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test filtering with an unknown author
def test_cli_unknown_filter_author(capsys, loaded_kavi_data):
    """Tests filtering with an author name that does not exist."""
    unknown_author = "Non Existent Author XYZ" # Use a name highly unlikely to exist
    # Simulate running with -a for an unknown author
    with patch.object(sys, 'argv', ['tamilkavi', '-a', unknown_author]):
        main() # Run the main function

        captured = capsys.readouterr()

        # Assert against the shorter "No results found.\n" message observed in errors
        assert "⚠️  No results found.\n" in captured.out

        # Ensure no data-specific headers are present in the output
        assert "Available Authors" not in captured.out
        assert "Books / Puthagangal" not in captured.out
        assert "Poem Titles" not in captured.out
        assert "Kavithai Title" not in captured.out

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test filtering with an unknown book title
def test_cli_unknown_filter_book(capsys, loaded_kavi_data):
    """Tests filtering with a book title that does not exist."""
    unknown_book = "Non Existent Book ABC" # Use a title highly unlikely to exist
    # Simulate running with -b for an unknown book
    with patch.object(sys, 'argv', ['tamilkavi', '-b', unknown_book]):
        main() # Run the main function

        captured = capsys.readouterr()

        # Assert against the shorter "No results found.\n" message observed in errors
        assert "⚠️  No results found.\n" in captured.out

        # Ensure no data-specific headers are present
        assert "Available Authors" not in captured.out
        assert "Books / Puthagangal" not in captured.out
        assert "Poem Titles" not in captured.out
        assert "Kavithai Title" not in captured.out

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test filtering with an unknown poem title
def test_cli_unknown_filter_poem(capsys, loaded_kavi_data):
    """Tests filtering with a poem title that does not exist."""
    unknown_poem = "Non Existent Poem Title 789" # Use a title highly unlikely to exist
    # Simulate running with -t for an unknown poem title
    with patch.object(sys, 'argv', ['tamilkavi', '-t', unknown_poem]):
        main() # Run the main function

        captured = capsys.readouterr()

        # Assert against the shorter "No results found.\n" message observed in errors
        assert "⚠️  No results found.\n" in captured.out

        # Ensure no data-specific headers are present
        assert "Available Authors" not in captured.out
        assert "Books / Puthagangal" not in captured.out
        assert "Poem Titles" not in captured.out
        assert "Kavithai Title" not in captured.out

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test listing all books ('tamilkavi -b')
def test_cli_list_books(capsys, loaded_kavi_data):
    """Tests listing all books based on loaded data."""
    all_data = loaded_kavi_data
    # Use KaviExtraction method to get the expected list of books from loaded data
    library = KaviExtraction()
    expected_books = library.get_all_books(all_data)

    # Simulate running with the -b argument (list all books)
    with patch.object(sys, 'argv', ['tamilkavi', '-b']):
        main() # Run the main function

        # Capture the output
        captured = capsys.readouterr()

        # Check for the books list header and expected table structure/content
        assert "📚 Available Books / Irrukum Puthagangal:" in captured.out
        assert "Book Title (Tanglish)" in captured.out # Check part of table header

        # Check that the Tanglish title of each expected book is in the output
        for book_data in expected_books:
             book_title_tanglish = book_data.get('booktitle_tanglish')
             if book_title_tanglish: # Only check if the title exists in the data
                 assert book_title_tanglish in captured.out

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test listing all titles ('tamilkavi -t')
def test_cli_list_titles(capsys, loaded_kavi_data):
    """Tests listing all unique poem titles based on loaded data."""
    all_data = loaded_kavi_data
    # Use KaviExtraction method to get the expected list of unique titles from loaded data
    library = KaviExtraction()
    expected_titles = library.get_all_unique_titles(all_data)

    # Simulate running with the -t argument (list all titles)
    with patch.object(sys, 'argv', ['tamilkavi', '-t']):
        main() # Run the main function

        captured = capsys.readouterr()

        # Check for the titles list header
        assert "📑 Available Poem Titles / Irrukum Kavithaiyin Thalaipugal:" in captured.out

        # Check that each expected unique title is present in the output
        # The output lists titles with numbers (e.g., "1. Title").
        # We can iterate through expected titles and check if a line exists that contains it.
        assert all(any(title in line for line in captured.out.splitlines()) for title in expected_titles), \
             f"Not all expected unique titles {expected_titles} found in output."


        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out


# Test combined filtering (e.g., 'tamilkavi -a <author> -b <book>') using dynamic data
def test_cli_combined_filter_author_book(capsys, loaded_kavi_data):
    """Tests combined author and book filtering using dynamically found data."""
    all_data = loaded_kavi_data
    # Find the first author with a book that has a Tanglish title and context
    author_name = None
    book_title_tanglish = None
    first_poem_title = None

    for author_data in all_data:
         if author_data.get('author'):
              for book_data in author_data.get('books', []):
                   if book_data.get('booktitle_tanglish') and book_data.get('context'):
                        author_name = author_data['author']
                        book_title_tanglish = book_data['booktitle_tanglish']
                        if book_data['context']:
                            first_poem_title = book_data['context'][0].get('title')
                        break # Found suitable book
              if author_name:
                   break # Stop searching authors

    assert author_name is not None, "Could not find a suitable author to test combined author+book filter."
    assert book_title_tanglish is not None, "Could not find a suitable book to test combined author+book filter."
    assert first_poem_title is not None, ("The first suitable book found is missing a title in its first poem context "
                                        "for combined test.")

    # Simulate running with both -a and -b filters using dynamic data
    with patch.object(sys, 'argv', ['tamilkavi', '-a', author_name, '-b', book_title_tanglish]):
        main() # Run the main function

        captured = capsys.readouterr()

        # Check for confirmation messages and poem table header
        assert f"✅ Author / Ezhuthalar: {author_name}" in captured.out # Should appear if author filter was effective
        assert f"✅ Book Title (Tanglish): {book_title_tanglish}" in captured.out # Should appear if book filter was effective
        assert "📜 Poems / Kavithaigal:" in captured.out # Table header for poems

        # Check that the first poem title from that book is in the output
        assert first_poem_title in captured.out

        # Ensure the welcome message is NOT in the output
        assert "🙏 Vannakam Makkalayae !" not in captured.out
        assert "Welcome to Tamil Kavi 👋" not in captured.out
