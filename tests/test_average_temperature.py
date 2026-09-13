#!/usr/bin/env python3

import contextlib
import io
import os
import unittest
from unittest.mock import patch

import pandas as pd

from src.average_temperature import average_temperature, main


class AverageTemperature(unittest.TestCase):

    def test_value(self):
        ret_val = average_temperature()
        self.assertAlmostEqual(
            ret_val,
            16.035483870967745,
            places=4,
            msg="Incorrect average temperature",
        )

    def test_output(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main()
        out = buf.getvalue().strip()
        pattern = r"Average temperature in July:\s+\d+.\d"
        self.assertRegex(out, pattern, msg="Output is not in correct form!")

    def test_called(self):
        with patch(
            "src.average_temperature.average_temperature",
            wraps=average_temperature,
        ) as pat, patch(
            "src.average_temperature.pd.read_csv", wraps=pd.read_csv
        ) as prc:
            main()
            pat.assert_called_once()
            prc.assert_called_once()
            args, kwargs = prc.call_args
            self.assertEqual(
                os.path.basename(args[0]),
                "kumpula-weather-2017.csv",
                msg="Wrong filename given to read_csv!",
            )
            if "sep" in kwargs:
                self.assertEqual(
                    kwargs["sep"],
                    ",",
                    msg="Incorrect separator in call to read_csv!",
                )


if __name__ == "__main__":
    unittest.main()
