
# Get Started
Robot number：TU-BT1-03
## 1. Powering On

1. Connect the robot to a power source using the power cable.
2. Press the black power button, located above the power port.
3. Wait 1–2 minutes. A loud start-up sound signals that the robot has finished booting and is ready to use.

---

## 2. Connecting over SSH

1. **Join the robot's network.** Your computer must be on the same Wi-Fi network as the robot.

   | Network | Password |
   |---|---|
   | `Tech_United` | `RoboCupMSL` |

2. **Open a terminal and connect:**

   ```bash
   ssh booster@10.0.0.27
   ```

   | Field | Value |
   |---|---|
   | User | `booster` |
   | Host | `10.0.0.27` |
   | Password | `[Ask a team member]` |

3. **Accept the host key.** On the first connection, SSH asks you to confirm the host key fingerprint. Type `yes` to continue 

4. **When you are finished, log out:**

   ```bash
   exit
   ```

   ## 3. Robot Hardware

**Computers.** The T1 contains two separate onboard computers, each running its own Ubuntu 22.04:

| Board | Handles |
|---|---|
| Motion control board | Motor drivers, gait, balance, joystick input |
| Perception board | Camera, vision, strategy, decision making |

The perception board is an NVIDIA Jetson Orin, and it is the one you reach with the SSH command above. Some other T1 units use a Jetson plus an x86 processor instead.

**Joints.** 23 actuated joints in total:

| Section | Count | Joints |
|---|---|---|
| Head | 2 | yaw, pitch |
| Arms | 4 each | shoulder pitch, shoulder roll, elbow pitch, elbow yaw |
| Waist | 1 | yaw |
| Legs | 6 each | hip pitch, hip roll, hip yaw, knee pitch, ankle pitch, ankle roll |

**Sensors and peripherals.**

- Head RGB-D camera — 1280×720 colour and 1280×720 depth, both at 30 Hz
- IMU for orientation and balance
- Joint encoders reporting position, velocity, and effort
- Microphones and speakers
- Touch sensing in the hands
- Status LEDs
- Battery with monitoring daemon
- USB joystick / remote controller
- Two CAN buses for motor communication

When standing, the head sits roughly 1.13 m above the floor.

---

## Further Documentation

- [Booster T1 official documentation](http://www.docs.bipedal.de/projects/t1/html/index.html)
- [Booster T1 Application Development Guide -- Robocup](http://www.docs.bipedal.de/projects/t1/html/index.html)
- [Booster T1 Application Development Guide -- Robocup /Chinese version](https://booster.feishu.cn/wiki/P5kJw6nDGib5wskZ3Yfc289lnIg)
- [Booster Robotics GitHub repositories](https://github.com/BoosterRobotics)
- [Tech United Eindhoven humanoid pages](https://pages.techunited.dev/tech-united-eindhoven/humanoid/)
- [T1 Instruction Manual - V1.6](https://booster.feishu.cn/wiki/XAS3wv4lwiSiXXkDbMrceE6UnHc)
- [Booster docs -- Developer Guide](https://docs.booster.tech/developer-guide/)
