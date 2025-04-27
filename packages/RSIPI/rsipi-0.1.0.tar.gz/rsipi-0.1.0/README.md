# RSIPI: Robot Sensor Interface - Python Integration

RSIPI is a high-performance, Python-based communication and control system designed for real-time interfacing with KUKA robots using the Robot Sensor Interface (RSI) protocol. It provides both a robust **API** for developers and a powerful **Command Line Interface (CLI)** for researchers and engineers who need to monitor, control, and analyse robotic movements in real time.

---

🛡️ Safety Notice
RSIPI is a powerful tool that directly interfaces with industrial robotic systems. Improper use can lead to dangerous movements, property damage, or personal injury.

⚠️ Safety Guidelines
Test in Simulation First
Always verify your RSI communication and trajectories using simulation tools before deploying to a live robot.

Enable Emergency Stops
Ensure all safety hardware (E-Stop, fencing, light curtains) is active and functioning correctly.

Supervised Operation Only
Run RSIPI only in supervised environments with trained personnel present.

Limit Movement Ranges
Use KUKA Workspaces or software limits to constrain movement, especially when testing new code.

Use Logging for Debugging
Avoid debugging while RSI is active; instead, enable CSV logging and review logs post-run.

Secure Network Configuration
Ensure your RSI network is on a closed, isolated interface to avoid external interference or spoofing.

Never Rely on RSIPI for Safety
RSIPI is not a safety-rated system. Do not use it in applications where failure could result in harm.

## 📄 Description

RSIPI allows users to:
- Communicate with KUKA robots using the RSI XML-based protocol.
- Dynamically update control variables (TCP position, joint angles, I/O, external axes, etc.).
- Log and visualise robot movements.
- Analyse motion data and compare planned vs actual trajectories.

### Target Audience
- **Researchers** working on advanced robotic applications, control algorithms, and feedback systems.
- **Engineers** developing robotic workflows or automated processes.
- **Educators** using real robots in coursework or lab environments.
- **Students** learning about robot control systems and data-driven motion planning.

---

## 📊 Features
- Real-time network communication with KUKA RSI over UDP.
- Structured logging to CSV with British date formatting.
- Background execution and live variable updates.
- Fully-featured Python API for scripting or external integration.
- CLI for interactive control and live monitoring.
- Real-time and post-analysis graphing.
- Basic trajectory planning and playback (Cartesian and Joint interpolation).

---

## 📊 API Overview (`rsi_api.py`)

### Initialization

```python
from src.RSIPI import rsi_api

api = rsi_api.RSIAPI(config_path='examples/RSI_EthernetConfig.xml')
```

### Methods
| Method | CLI | API | Description |
|-------|-----|-----|-------------|
| `start_rsi()` | ✅ | ✅ | Starts RSI communication (non-blocking). |
| `stop_rsi()` | ✅ | ✅ | Stops RSI communication. |
| `update_variable(path, value)` | ✅ | ✅ | Dynamically updates a send variable (e.g. `RKorr.X`). |
| `get_variable(path)` | ✅ | ✅ | Retrieves the latest value of any variable. |
| `enable_logging(include=None, exclude=None)` | ❌ | ✅ | Starts CSV logging in background. |
| `disable_logging()` | ❌ | ✅ | Stops CSV logging. |
| `enable_graphing(mode='tcp')` | ❌ | ✅ | Enables real-time graphing (TCP or joint). |
| `disable_graphing()` | ❌ | ✅ | Disables graphing. |
| `plan_linear_cartesian(start, end, steps)` | ❌ | ✅ | Creates a Cartesian path. |
| `plan_linear_joint(start, end, steps)` | ❌ | ✅ | Creates a joint-space path. |
| `execute_trajectory(traj, delay=0.012)` | ❌ | ✅ | Sends a trajectory to robot using RSI corrections. |

---

## 🔧 CLI Overview (`rsi_cli.py`)

Start the CLI:
```bash
python main.py --cli
```

### Available Commands:
| Command | Description |
|---------|-------------|
| `start` | Starts the RSI client. |
| `stop` | Stops RSI communication. |
| `set <variable> <value>` | Updates a send variable. |
| `get <variable>` | Displays the current value of a variable. |
| `graph on/off` | Enables/disables live graphing. |
| `log on/off` | Enables/disables logging. |
| `status` | Displays current status. |
| `exit` | Exits the CLI. |

---

## 📃 Examples

### Start RSI and update Cartesian coordinates
```python
api.start_rsi()
api.update_variable('RKorr.X', 100.0)
api.update_variable('RKorr.Y', 200.0)
api.update_variable('RKorr.Z', 300.0)
```

### Retrieve joint positions
```python
a1 = api.get_variable('AIPos.A1')
```

### Plan and execute Cartesian trajectory
```python
start = {'X': 0, 'Y': 0, 'Z': 0, 'A': 0, 'B': 0, 'C': 0}
end   = {'X': 100, 'Y': 100, 'Z': 0, 'A': 0, 'B': 0, 'C': 0}
traj = api.plan_linear_cartesian(start, end, steps=50)
api.execute_trajectory(traj)
```

### CLI Sample
```bash
> start
> set RKorr.X 150
> set DiO 255
> get AIPos.A1
> log on
> graph on
> stop
```

---

## 📤 Output & Logs
- CSV logs saved to `logs/` folder.
- Each log includes timestamp, sent and received values in individual columns.
- Graphs can be saved manually as PNG/PDF from the visualisation window.

---

## 🚀 Getting Started
1. Connect robot and PC via Ethernet.
2. Deploy KUKA RSI program with matching configuration.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run `main.py` and use CLI or import API in your Python program.

---

## 🔖 Citation
If you use RSIPI in your research, please cite:
```
@software{rsipi2025,
  author = {RSIPI Development Team},
  title = {RSIPI: Robot Sensor Interface - Python Integration},
  year = {2025},
  url = {https://github.com/your-org/rsipi},
  note = {Accessed: [insert date]}
}
```

---

## ⚖️ License
RSIPI is licensed under the MIT License:

```
MIT License

Copyright (c) 2025 RSIPI Developers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🚧 Disclaimer
RSIPI is designed for research and experimental purposes only. Ensure safe robot operation with appropriate safety measures.

