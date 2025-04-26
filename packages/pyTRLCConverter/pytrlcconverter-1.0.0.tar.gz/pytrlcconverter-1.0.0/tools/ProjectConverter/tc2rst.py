"""Project specific reStructuredText converter functions.

    Author: Andreas Merkle (andreas.merkle@newtec.de)
"""

# pyTRLCConverter - A tool to convert TRLC files to specific formats.
# Copyright (c) 2024 - 2025 NewTec GmbH
#
# This file is part of pyTRLCConverter program.
#
# The pyTRLCConverter program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# The pyTRLCConverter program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with pyTRLCConverter.
# If not, see <https://www.gnu.org/licenses/>.

# Imports **********************************************************************

from pyTRLCConverter.base_converter import RecordsPolicy
from pyTRLCConverter.ret import Ret

from pyTRLCConverter.trlc_helper import Record_Object

# pylint: disable=wrong-import-order
from generic_rsl_rst_converter import GenericRslRstConverter

# Variables ********************************************************************

# Classes **********************************************************************


class TestCaseRstConverter(GenericRslRstConverter):
    """Custom Project specific reStructuredText converter for test cases.
    """
    def __init__(self, args: any) -> None:
        """
        Initialize the custom reStructuredText converter.

        Args:
            args (any): The parsed program arguments.
        """
        super().__init__(args)

        # Set project specific record handlers for the converter.
        self._set_project_record_handlers(
           {
                "Image": self._print_image,
                "Info": self._print_info,
                "PlantUML": self._print_plantuml,
                "SwTestCase": self._print_sw_test_case,
           }
        )
        self._record_policy = RecordsPolicy.RECORD_SKIP_UNDEFINED

    @staticmethod
    def get_description() -> str:
        """ Return converter description.

         Returns:
            str: Converter description
        """
        return "Convert test case definitions into project extended reStructuredText format."

    def _print_sw_test_case(self, sw_test_case: Record_Object, level: int) -> Ret:
        """Prints the software test case.

        Args:
            sw_test_case (Record_Object): Software test case to print
            level (int): Current level of the record object

        Returns:
            Ret: Status
        """

        self._write_empty_line_on_demand()

        attribute_translation = {
            "description": "Description",
            "verifies": "Verifies"
        }

        return self._convert_record_object(sw_test_case, level, attribute_translation)

# Functions ********************************************************************

# Main *************************************************************************
