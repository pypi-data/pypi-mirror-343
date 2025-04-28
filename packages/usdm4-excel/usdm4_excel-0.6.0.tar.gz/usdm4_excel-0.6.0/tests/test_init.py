from unittest.mock import patch, MagicMock
from usdm4_excel import USDM4Excel


class TestUSDM4Excel:
    """Tests for the USDM4Excel class in __init__.py."""

    @patch("usdm4_excel.ExcelTableWriter")
    def test_default_sheet_name(self, mock_excel_table_writer):
        """Test that the default sheet name is set to 'study' when creating an ExcelTableWriter instance."""
        # Create an instance of USDM4Excel
        usdm4_excel = USDM4Excel()

        # Mock the open function and json.load to avoid file operations
        with (
            patch("builtins.open", MagicMock()),
            patch("usdm4_excel.json.load", return_value={}),
            patch("usdm4_excel.USDM4"),
            patch("usdm4_excel.Wrapper"),
        ):
            # Call the to_excel method
            usdm4_excel.to_excel("dummy_usdm.json", "dummy_excel.xlsx")

            # Verify that ExcelTableWriter was initialized with the correct default_sheet_name
            mock_excel_table_writer.assert_called_once_with(
                "dummy_excel.xlsx", default_sheet_name="study"
            )
