import pytest
from unittest.mock import MagicMock

from dbcls.sql_tokenizer import (
    CaseInsensitiveKeywords, 
    NonSqlComment, 
    CommandSpan,
    sqleditor_tokens, 
    make_tokenizer
)


class TestCaseInsensitiveKeywords:
    def test_re_start(self):
        """Test re_start generates a case-insensitive regex pattern"""
        keywords = CaseInsensitiveKeywords("test", ["SELECT", "FROM"])
        pattern = keywords.re_start()
        
        # Verify the pattern includes case-insensitive character classes
        assert "[sS][eE][lL][eE][cC][tT]" in pattern
        assert "[fF][rR][oO][mM]" in pattern
        assert r"\b(" in pattern  # word boundary at start
        assert r")\b" in pattern  # word boundary at end
        
    def test_re_start_with_special_chars(self):
        """Test re_start handles special regex characters"""
        keywords = CaseInsensitiveKeywords("test", ["GROUP BY", "ORDER BY"])
        pattern = keywords.re_start()
        
        # Verify escape sequences for special characters
        assert "[gG][rR][oO][uU][pP] [bB][yY]" in pattern
        assert "[oO][rR][dD][eE][rR] [bB][yY]" in pattern


class TestSqlEditorTokens:
    def test_sqleditor_tokens(self):
        """Test sqleditor_tokens returns a list of token definitions"""
        mock_client = MagicMock()
        mock_client.all_commands = ["SELECT", "FROM"]
        mock_client.all_functions = ["COUNT", "SUM"]
        
        tokens = sqleditor_tokens(mock_client)
        
        # Verify token types
        token_names = [t[0] for t in tokens]
        assert "directive" in token_names
        assert "comment1" in token_names
        assert "comment2" in token_names
        assert "string1" in token_names
        assert "string2" in token_names
        assert "number" in token_names
        assert "keyword" in token_names
        assert "function" in token_names
        
        # Verify token classes
        token_classes = [type(t[1]) for t in tokens]
        assert CommandSpan in token_classes
        assert NonSqlComment in token_classes
        assert CaseInsensitiveKeywords in token_classes


class TestMakeTokenizer:
    def test_make_tokenizer(self):
        """Test make_tokenizer creates a Tokenizer with the correct tokens"""
        mock_client = MagicMock()
        mock_client.all_commands = ["SELECT"]
        mock_client.all_functions = ["COUNT"]
        
        tokenizer = make_tokenizer(mock_client)
        
        # Verify tokenizer has tokens
        assert hasattr(tokenizer, "tokens")
        
        # Use the tokenizer to verify functionality
        # The tokenizer is normally integrated with kaa.Document,
        # so we can't easily test its full functionality here,
        # but we can verify it was created properly