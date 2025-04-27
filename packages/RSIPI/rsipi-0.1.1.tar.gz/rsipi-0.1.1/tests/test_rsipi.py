import unittest
from time import sleep
from RSIPI.rsi_api import RSIAPI
import pandas as pd
import tempfile
import os

class TestRSIPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = RSIAPI("/RSI_EthernetConfig.xml")
        cls.api.start_rsi()
        sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.api.stop_rsi()

    def test_update_variable(self):
        response = self.api.update_variable("EStr", "TestMessage")
        self.assertIn("✅ Updated EStr to TestMessage", response)

    def test_toggle_digital_io(self):
        response = self.api.toggle_digital_io("DiO", 1)
        self.assertIn("✅ DiO set to 1", response)

    def test_move_external_axis(self):
        response = self.api.move_external_axis("E1", 150.0)
        self.assertIn("✅ Moved E1 to 150.0", response)

    def test_correct_position_rkorr(self):
        response = self.api.correct_position("RKorr", "X", 10.5)
        self.assertIn("✅ Applied correction: RKorr.X = 10.5", response)

    def test_correct_position_akorr(self):
        response = self.api.correct_position("AKorr", "A1", 5.0)
        self.assertIn("✅ Applied correction: AKorr.A1 = 5.0", response)

    def test_adjust_speed(self):
        response = self.api.adjust_speed("Tech.T21", 2.5)
        self.assertIn("✅ Set Tech.T21 to 2.5", response)

    def test_logging_start_and_stop(self):
        response_start = self.api.start_logging("test_log.csv")
        self.assertIn("✅ CSV Logging started", response_start)
        sleep(2)
        response_stop = self.api.stop_logging()
        self.assertIn("🛑 CSV Logging stopped", response_stop)

    def test_graphing_start_and_stop(self):
        response_start = self.api.start_graphing(mode="position")
        self.assertIn("✅ Graphing started in position mode", response_start)
        sleep(5)
        response_stop = self.api.stop_graphing()
        self.assertIn("🛑 Graphing stopped", response_stop)

    def test_get_live_data(self):
        data = self.api.get_live_data()
        self.assertIn("position", data)
        self.assertIn("force", data)

    def test_get_ipoc(self):
        ipoc = self.api.get_ipoc()
        self.assertTrue(str(ipoc).isdigit() or ipoc == "N/A", f"Invalid IPOC value: {ipoc}")

    def test_reconnect(self):
        response = self.api.reconnect()
        self.assertIn("✅ Network connection restarted", response)

    def test_reset_variables(self):
        response = self.api.reset_variables()
        self.assertIn("✅ Send variables reset to default values", response)

    def test_get_status(self):
        status = self.api.show_config_file()
        self.assertIn("network", status)
        self.assertIn("send_variables", status)
        self.assertIn("receive_variables", status)

    def test_export_data(self):
        response = self.api.export_movement_data("export_test.csv")
        self.assertIn("✅ Data exported to export_test.csv", response)

    def test_alert_toggle_and_threshold(self):
        response_enable = self.api.enable_alerts(True)
        self.assertIn("✅ Alerts enabled", response_enable)
        response_threshold = self.api.set_alert_threshold("deviation", 3.5)
        self.assertIn("✅ Deviation alert threshold set to 3.5", response_threshold)

    def test_visualization_methods(self):
        csv_file = "test_log.csv"
        # Create a dummy CSV file for testing
        pd.DataFrame({
            "RIst.X": [0, 1, 2], "RIst.Y": [0, 1, 2], "RIst.Z": [0, 1, 2],
            "AIPos.A1": [10, 20, 30], "PosCorr.X": [0.1, 0.2, 0.3]
        }).to_csv(csv_file, index=False)

        try:
            self.api.visualise_csv_log(csv_file, export=True)
        except Exception as e:
            self.fail(f"Visualisation test failed: {e}")
        finally:
            import shutil
            os.remove(csv_file)
            if os.path.exists("exports"):
                shutil.rmtree("exports")

    def test_krl_parsing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_file = os.path.join(tmpdir, "test.src")
            dat_file = os.path.join(tmpdir, "test.dat")
            csv_file = os.path.join(tmpdir, "test.csv")

            with open(src_file, "w") as f_src, open(dat_file, "w") as f_dat:
                f_src.write("PDAT_ACT=XP1\nPDAT_ACT=XP2\n")
                f_dat.write("DECL E6POS XP1={X 10,Y 20,Z 30,A 0,B 90,C 180,S 2,T 1,E1 0,E2 0}\n")
                f_dat.write("DECL E6POS XP2={X 40,Y 50,Z 60,A 0,B 90,C 180,S 2,T 1,E1 0,E2 0}\n")

            response = self.api.parse_krl_to_csv(src_file, dat_file, csv_file)
            self.assertTrue(response.startswith("✅"))
            df = pd.read_csv(csv_file)
            print("🔍 Parsed DataFrame:")
            print(df)
            self.assertEqual(len(df), 2)

    def test_inject_rsi(self):
        input_krl = "test_program.src"
        output_krl = "test_program_rsi.src"

        with open(input_krl, "w") as file:
            file.write("DEF Test()\n")
            file.write("  ;ENDFOLD (INI)\n")
            file.write("END\n")

        response = self.api.inject_rsi(input_krl, output_krl)
        self.assertIn("✅ RSI successfully injected", response)

        with open(output_krl, "r") as file:
            content = file.read()
            self.assertIn("RSI_CREATE", content)
            self.assertIn("RSI_ON", content)
            self.assertIn("RSI_OFF", content)

        # Cleanup
        os.remove(input_krl)
        os.remove(output_krl)

    def test_get_variables(self):
        """Test retrieval of full send and receive variable dictionaries."""
        variables = self.api.show_variables()
        self.assertIn("send_variables", variables)
        self.assertIn("receive_variables", variables)
        self.assertIsInstance(variables["send_variables"], dict)
        self.assertIsInstance(variables["receive_variables"], dict)

    def test_get_live_data_as_numpy(self):
        """Test live data returned as NumPy array."""
        array = self.api.get_live_data_as_numpy()
        self.assertEqual(array.shape[0], 4)  # position, velocity, acceleration, force
        self.assertEqual(array.shape[1], 6)  # Max possible length: 6 joints (A1-A6)

    def test_get_live_data_as_dataframe(self):
        """Test live data returned as a Pandas DataFrame."""
        df = self.api.get_live_data_as_dataframe()
        self.assertFalse(df.empty)
        self.assertIn("position", df.columns)


if __name__ == '__main__':
    unittest.main()