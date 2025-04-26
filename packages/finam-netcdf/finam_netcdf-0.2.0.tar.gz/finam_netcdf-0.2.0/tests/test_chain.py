import unittest
from datetime import datetime
from os import path
from tempfile import TemporaryDirectory

import finam as fm
from numpy.testing import assert_allclose

from finam_netcdf import NetCdfPushWriter, NetCdfReader, Variable


class TestChain(unittest.TestCase):
    def test_chain(self):
        in_path = "tests/data/temp.nc"

        data_1 = []
        data_2 = []

        def store_data_1(name, data, time):
            data_1.append((time, data))

        def store_data_2(name, data, time):
            data_2.append((time, data))

        with TemporaryDirectory() as tmp:
            out_path = path.join(tmp, "test.nc")

            reader = NetCdfReader(in_path, [Variable("tmin", "LAI")])
            writer = NetCdfPushWriter(out_path, ["lai"])
            consumer = fm.components.DebugPushConsumer(
                inputs={
                    "LAI": fm.Info(time=None, grid=None, units=None),
                },
                callbacks={"LAI": store_data_1},
            )

            comp = fm.Composition([reader, writer, consumer])

            reader["LAI"] >> writer["lai"]
            reader["LAI"] >> consumer["LAI"]

            comp.run(end_time=datetime(1990, 1, 31))

            self.assertTrue(path.isfile(out_path))

            # Second iteration

            reader = NetCdfReader(out_path, ["lai"])
            consumer = fm.components.DebugPushConsumer(
                inputs={
                    "LAI": fm.Info(time=None, grid=None, units=None),
                },
                callbacks={"LAI": store_data_2},
            )

            comp = fm.Composition([reader, consumer])

            reader["lai"] >> consumer["LAI"]

            comp.run(end_time=datetime(1990, 1, 31))

            self.assertEqual(len(data_1), len(data_2))

            for (t1, d1), (t2, d2) in zip(data_1, data_2):
                self.assertEqual(t1, t2)
                assert_allclose(fm.data.get_magnitude(d1), fm.data.get_magnitude(d2))
                self.assertEqual(fm.data.get_units(d1), fm.data.get_units(d2))


if __name__ == "__main__":
    unittest.main()
