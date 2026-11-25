---
doc:
  quadrant: reference
  verified_on: "software 1.8.0.9, both boards"
---
# ROS interfaces

> [!warning] Review needed
> This page has not been reviewed by the team yet.

COSMO runs ROS 2 Humble. This page lists the nodes, the 144 topics visible on the Orin, their message types and rates, the services and the frames. Values marked (software 1.6.2.2) were not checked on 1.8.0.9. A dash means that the rate was not measured.

How to load the message types: [[software_overview#Load the Booster message types]]. Request and response calls: [[rpc_api]].

## Nodes

| Node | Runs on |
|---|---|
| `/loco_rpc_bridge` | x86 |
| `/joy_node` | x86 |
| `/boostercamera/camera` | Orin |
| `/booster_agent_manager`, `/booster_agent_telemetry_manager` | Orin |
| `/com_boosterobotics_default` | Orin |
| `/robot_mode_client` | [UNKNOWN] |

The list comes from `ros2 node list --no-daemon --spin-time 10`. Without the 10-second wait it is incomplete. The two boards share one graph, so the list does not show on which board a node runs. Many Booster programs use DDS directly and have no ROS node name.

## Topics

### Robot state and sensing

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/joint_states` | `sensor_msgs/msg/JointState` | 500 Hz, 1228 B | 23 joints, see [[hardware-overview#Actuators and joints]]. |
| `/low_state` | `booster_interface/msg/LowState` | 500 Hz, 1704 B | See [Message fields](#message-fields). |
| `/odometer_state` | `booster_interface/msg/Odometer` | 500 Hz, 16 B | See [Message fields](#message-fields). |
| `/odom` | `nav_msgs/msg/Odometry` | 500 Hz | Frame `odom`, child frame `trunk`, all covariances 0.0. |
| `/imu/data` | `sensor_msgs/msg/Imu` | 500 Hz | Frame `trunk`, covariance arrays empty. |
| `/tf` | `tf2_msgs/msg/TFMessage` | 500 Hz, 236 B | See [Frames and odometry](#frames-and-odometry). |
| `/tf_static` | `tf2_msgs/msg/TFMessage` | - | |
| `/head_pose` | `geometry_msgs/msg/Pose` | 94 Hz, 60 B (software 1.6.2.2) | |
| `/head_pose_stamped` | `geometry_msgs/msg/PoseStamped` | - | |
| `/robot_states` | `booster_interface/msg/RobotStatesMsg` | 2 Hz (16 B, software 1.6.2.2) | Current mode, see [Message fields](#message-fields). |
| `/robot_state` | `booster_interface/msg/RawBytesMsg` | 466 Hz, 120 B (software 1.6.2.2) | |
| `/fall_down` | `booster_interface/msg/FallDownState` | 1 Hz (12 B, software 1.6.2.2) | Constants: see [Message fields](#message-fields). |
| `/fall_down_recovery_state` | `booster_interface/msg/RawBytesMsg` | 1 Hz, 12 B (software 1.6.2.2) | |
| `/motion_state` | `booster/msg/MotionState` | - | No message definition on the robot. |
| `/battery_state` | `booster_interface/msg/BatteryState` | no messages | Has a publisher; no message arrives with the robot on mains. See [Message fields](#message-fields). |
| `/prone_body_control_status` | `booster_interface/msg/ProneBodyControlStatus` | 2 Hz, 8 B (software 1.6.2.2) | |
| `/booster_process_state` | `booster_interface/msg/RobotProcessStateMsg` | - | |
| `/device_gateway` | `booster_interface/msg/RobotStatusDdsMsg` | - | |

### Command, behaviour and hand topics

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/joint_ctrl` | `booster_interface/msg/LowCmd` | - | 0 publishers when idle, 1 subscriber (BEST_EFFORT). |
| `/kick_ball` | `brain/msg/Kick` | - | No message definition on the robot (package `brain` not found). |
| `/enter_safe_mode` | `booster_msgs/msg/BinaryData` | 3.3 Hz, 48 B (software 1.6.2.2) | |
| `/robocup_behavior_status` | `booster_interface/msg/RobocupBehaviorStatus` | - | |
| `/robot_replay_traj_id` | `booster_interface/msg/RobotReplayTrajID` | - | |
| `/trained_traj_status` | `booster_interface/msg/TrainedTrajStatus` | - | |
| `/booster_hand` | `booster_msgs/msg/HandDdsMsg` | - | No message definition on the robot (only `booster_interface/msg/HandDdsMsg` exists). |
| `/booster_hand_data` | `booster_interface/msg/HandReplyData` | - | |
| `/booster_hand_touch_data` | `booster_interface/msg/HandTouchData` | - | |

A topic that takes commands has a publisher only while a client sends commands. 0 publishers does not mean the topic is unused ([INFERENCE]).

### Camera

The camera node is `/boostercamera/camera` on the Orin. Camera data (resolution, intrinsics): [[hardware-overview#Head RGB-D camera]].

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/booster_video_stream` | `sensor_msgs/msg/CompressedImage` | 0 msgs | 0 publishers. |
| `/boostercamera/head/rgb` | `sensor_msgs/msg/Image` | 30 Hz | Colour image, `rgb8`. |
| `/boostercamera/head/rgb/camera_info` | `sensor_msgs/msg/CameraInfo` | 30 Hz | Frame `head_color_optical_frame`. |
| `/boostercamera/head/depth` | `sensor_msgs/msg/Image` | 30 Hz | Depth image aligned to colour, `16UC1`. |
| `/boostercamera/head/depth/camera_info` | `sensor_msgs/msg/CameraInfo` | - | Same values and frame as the colour `camera_info`. |
| `/boostercamera/camera/color/image_raw/compressed` | `sensor_msgs/msg/CompressedImage` | [UNVERIFIED] 80 B per message | [UNVERIFIED] Holds no image. |
| `/boostercamera/camera/color/image_raw/compressedDepth` | `sensor_msgs/msg/CompressedImage` | - | |
| `/boostercamera/camera/color/image_raw/theora` | `theora_image_transport/msg/Packet` | - | |
| `/boostercamera/camera/color/metadata` | `realsense2_camera_msgs/msg/Metadata` | - | |
| `/boostercamera/camera/depth/camera_info` | `sensor_msgs/msg/CameraInfo` | - | |
| `/boostercamera/camera/depth/image_rect_raw` | `sensor_msgs/msg/Image` | [UNKNOWN] | Unaligned depth. |
| `/boostercamera/camera/depth/image_rect_raw/compressed` | `sensor_msgs/msg/CompressedImage` | - | |
| `/boostercamera/camera/depth/image_rect_raw/compressedDepth` | `sensor_msgs/msg/CompressedImage` | 33.2 Hz, 145,936 B | Unaligned depth, carries data. |
| `/boostercamera/camera/depth/image_rect_raw/theora` | `theora_image_transport/msg/Packet` | - | |
| `/boostercamera/camera/depth/metadata` | `realsense2_camera_msgs/msg/Metadata` | - | |
| `/boostercamera/camera/aligned_depth_to_color/image_raw/compressed` | `sensor_msgs/msg/CompressedImage` | - | [UNVERIFIED] No data. |
| `/boostercamera/camera/aligned_depth_to_color/image_raw/compressedDepth` | `sensor_msgs/msg/CompressedImage` | - | [UNVERIFIED] No data. |
| `/boostercamera/camera/aligned_depth_to_color/image_raw/theora` | `theora_image_transport/msg/Packet` | - | |
| `/boostercamera/camera/extrinsics/depth_to_color` | `realsense2_camera_msgs/msg/Extrinsics` | - | |

### Audio

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/booster_sound` | `booster_msgs/msg/BinaryData` | - | |

The audio request/response topics are listed under [RPC request and response topics](#rpc-request-and-response-topics).

### Lights

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/light_control` | `booster_interface/msg/LightControlMsg` | - | |
| `/light_status` | `booster_interface/msg/RawBytesMsg` | 0 msgs (software 1.6.2.2) | |

The light request/response pair is `/LightControlApiTopicReq` and `/LightControlApiTopicResp`, see [RPC request and response topics](#rpc-request-and-response-topics).

### Remote controller and joystick

The joystick and its receiver: [[control_with_joystick]].

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/joy` | `sensor_msgs/msg/Joy` | 0 msgs (software 1.6.2.2) | |
| `/joy/set_feedback` | `sensor_msgs/msg/JoyFeedback` | - | 0 publishers when idle (software 1.6.2.2). |
| `/remote_controller_state` | `booster_interface/msg/RemoteControllerState` | 0 msgs (software 1.6.2.2) | |
| `/button_event` | `booster_interface/msg/ButtonEventMsg` | 0 msgs (software 1.6.2.2) | |

### Agent and AI

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/booster/agent/system/telemetry_msg` | `std_msgs/msg/String` | - | |

[UNKNOWN] Whether the agent, vision, voice and YOLO topics appear when their Booster programs run; none is in the list.

### Other

| Topic | Type | Rate | Notes |
|---|---|---|---|
| `/parameter_events` | `rcl_interfaces/msg/ParameterEvent` | - | |
| `/rosout` | `rcl_interfaces/msg/Log` | 0 msgs (software 1.6.2.2) | |
| `/record_upload` | `booster_msgs/msg/BinaryData` | - | |
| `/handeye_calib/feedback/image` | `sensor_msgs/msg/CompressedImage` | - | |
| `/handeye_calib/reload_camera_extrinsics` | `booster_interface/msg/RawBytesMsg` | - | |

### RPC request and response topics

Request/response pairs named `<stem>Req` (type `booster_msgs/msg/RpcReqMsg`) and `<stem>Resp` (type `booster_msgs/msg/RpcRespMsg`). Their format and the known calls: [[rpc_api]].

| Stem | Req / Resp | Rate | Notes |
|---|---|---|---|
| `/CameraApiTopic` | `Req` / `Resp` | - | |
| `/HandEyeCalibApiTopic` | `Req` / `Resp` | - | |
| `/LightControlApiTopic` | `Req` / `Resp` | - | |
| `/LocoApiTopic` | `Req` / `Resp` | - | `Req` has 10 publishers and 1 subscriber, see [[rpc_api]]. |
| `/daemon_locomotion` | `Req` / `Resp` | - | |
| `/wifi_connect` | `Req` / `Resp` | - | |
| `/zero_pose_set` | `Req` / `Resp` | - | |

`/LocoApiOperationEvent` has type `booster_msgs/msg/RpcRespMsg` and has no `Req` topic in the list.

Audio pairs, 35 stems under `/booster/audio/`, each with `<stem>Req` and `<stem>Resp` (70 topics):

| Stems |
|---|
| `connect_bluetooth_device`, `disconnect_bluetooth_device`, `forget_bluetooth_device`, `get_bluetooth_devices`, `start_bluetooth_scan`, `stop_bluetooth_scan` |
| `get_devices`, `set_preferred_device`, `get_doa_angle`, `register_client` |
| `get_system_mute`, `set_system_mute`, `get_system_volume`, `set_system_volume`, `set_volume` |
| `init_capture_stream`, `start_capture_stream`, `pause_capture_stream`, `stop_capture_stream`, `destroy_capture_stream`, `get_capture_stream_info` |
| `init_player`, `start_player`, `pause_player`, `stop_player`, `destroy_player`, `reset_player`, `get_player_info`, `send_pcm_data` |
| `init_recorder`, `start_recorder`, `pause_recorder`, `stop_recorder`, `destroy_recorder`, `get_recorder_info` |

Rates: [UNKNOWN].

## QoS

| Topic | Reliability | Durability |
|---|---|---|
| `/boostercamera/head/rgb`, `/boostercamera/head/depth` | RELIABLE | TRANSIENT_LOCAL |
| `/low_state`, `/imu/data`, `/fall_down`, `/battery_state` | RELIABLE | TRANSIENT_LOCAL |
| `/joint_ctrl` (subscriber) | BEST_EFFORT | VOLATILE |

[UNKNOWN] The QoS of the other topics.

## Message fields

### LowState and MotorState

- `LowState` is `imu_state` (`ImuState`: `float32[3] rpy`, `gyro`, `acc`) plus `motor_state_parallel[]` and `motor_state_serial[]`, 23 entries each.
- `MotorState` is `int8 mode`, `float32 q`, `dq`, `ddq`, `tau_est`, `int8 temperature`, `uint32 lost`, `uint32[2] reserve`.
- Meaning of `temperature` and `reserve`: [[hardware-overview#Motor state]].

### Odometer

`booster_interface/msg/Odometer` is `float32 x`, `float32 y`, `float32 theta`. [INFERENCE] The units are m, m and rad.

### BatteryState

Fields and known limits: [[hardware-overview#Power and battery]].

### RobotStatesMsg

`/robot_states`: `int32 current_mode`, `int32 current_body_control`, `int32[] current_actions`. Mode numbers: [[rpc_api#Mode numbers]].

### FallDownState

`/fall_down`: `uint32 fall_down_state`, `bool is_recovery_available`. Constants for `fall_down_state`: `IS_READY=0`, `IS_FALLING=1`, `HAS_FALLEN=2`, `IS_GETTING_UP=3`.

### LowCmd and MotorCmd

`/joint_ctrl`: `LowCmd` is `int8 cmd_type` plus `MotorCmd[] motor_cmd`. Constants for `cmd_type`: `CMD_TYPE_PARALLEL=0`, `CMD_TYPE_SERIAL=1`. `MotorCmd` is `int8 mode`, `float32 q`, `dq`, `tau`, `kp`, `kd`, `weight`.

### RpcReqMsg and RpcRespMsg

Used by all request/response topics. Fields `string uuid`, `string header` (JSON text), `string body`. See [[rpc_api#Message format]].

## Services

| Service | Type | Notes |
|---|---|---|
| `/booster_rpc_service` | `booster_interface/srv/RpcService` | Visible from both boards. See [[rpc_api]]. |

`booster_interface` also contains the service type `AgentService` (`string body` request, `string body` response). [UNKNOWN] What it is used for.

## Frames and odometry

- `/tf` on the Orin carries head frames: `child_frame_id` `head_color_optical_frame` and `head_point`, `frame_id` `aahead_pitch_link`. [INFERENCE] `/tf` holds only head frames.
- Odometry topics: `/odometer_state` (`Odometer`) and `/odom` (`nav_msgs/msg/Odometry`). Fields: see [Odometer](#odometer).

## Message packages

Topics per package:

| Package | Topics |
|---|---|
| `booster_msgs` | 89 |
| `booster_interface` | 21 |
| `sensor_msgs` | 18 |
| `realsense2_camera_msgs` | 3 |
| `theora_image_transport` | 3 |
| `geometry_msgs` | 2 |
| `rcl_interfaces` | 2 |
| `tf2_msgs` | 2 |
| `booster` | 1 |
| `brain` | 1 |
| `nav_msgs` | 1 |
| `std_msgs` | 1 |

Message definitions on the robot:

- Four workspaces under `/opt/booster/*/install` hold Booster definitions: `BoosterRos2`, `BoosterRos2Interface`, `BoosterAgent`, `BoosterFaceDetection`.
- `booster_interface` holds 36 messages and the services `AgentService` and `RpcService`. `booster_msgs` holds `BinaryData`, `RpcReqMsg`, `RpcRespMsg`. `detection` holds `Detection`, `DetectionMsgs`, `PersonFace`, `PersonFaceMsgs`.
- Types without a definition: `booster_msgs/msg/HandDdsMsg` (only `booster_interface/msg/HandDdsMsg` exists), `brain/msg/Kick` and `booster/msg/MotionState`.

## Known problems

| Symptom | Cause | Fix |
|---|---|---|
| `/booster_video_stream` shows nothing | No publisher. [INFERENCE] The video-stream program is installed but not running | Use `/boostercamera/head/rgb` |
| The `compressed` topics under `/boostercamera/camera/` show no image [UNVERIFIED] | [INFERENCE] The driver publishes its images under other names | Use `/boostercamera/head/rgb` or `/boostercamera/head/depth` |
| A topic cannot be decoded | Its type has no definition, see [Message packages](#message-packages) | None |
| Topic and node lists differ between runs | With `--no-daemon`, the discovery time is too short | Add `--spin-time 10` |
| `/battery_state` sends no messages | COSMO is on mains power. [UNKNOWN] Whether messages arrive on battery | None |

Problems with the Foxglove bridge: [[software_overview#Known problems]].
