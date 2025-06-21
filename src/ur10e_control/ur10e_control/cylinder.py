#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
import os

from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import (
    Constraints,
    JointConstraint,
    MotionPlanRequest,
    RobotState,
)
from sensor_msgs.msg import JointState


def parse_txt_file(file_path):
    joint_positions = []
    with open(file_path, 'r') as file:
        for line in file:
            positions = line.strip().split(',')
            joint_positions.append([float(pos) for pos in positions])
    return joint_positions


class MoveItJointGoalClient(Node):
    def __init__(self, joint_positions):
        super().__init__('moveit_joint_goal_client')

        self.joint_positions = joint_positions
        self.current_goal_index = 0

        self._action_client = ActionClient(self, MoveGroup, 'move_action')

        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

        self.send_next_goal()

    def send_next_goal(self):
        if self.current_goal_index >= len(self.joint_positions):
            self.get_logger().info("All joint goals executed.")
            rclpy.shutdown()
            return

        self.target_positions = self.joint_positions[self.current_goal_index]
        self.get_logger().info(f"Sending joint goal {self.current_goal_index + 1}: {self.target_positions}")

        self._action_client.wait_for_server()

        request = MotionPlanRequest()
        request.group_name = 'ur_manipulator'

        joint_constraints = []
        for name, pos in zip(self.joint_names, self.target_positions):
            jc = JointConstraint()
            jc.joint_name = name
            jc.position = pos
            jc.tolerance_above = 0.01
            jc.tolerance_below = 0.01
            jc.weight = 1.0
            joint_constraints.append(jc)

        request.goal_constraints.append(Constraints(joint_constraints=joint_constraints))

        current_state = RobotState()
        current_state.joint_state.name = self.joint_names
        current_state.joint_state.position = [0.0] * 6
        request.start_state = current_state

        request.allowed_planning_time = 5.0
        request.max_velocity_scaling_factor = 1.0
        request.max_acceleration_scaling_factor = 1.0

        goal_msg = MoveGroup.Goal()
        goal_msg.request = request

        self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        ).add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info('Planning feedback received.')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal was rejected.')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted.')
        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result.error_code.val == result.error_code.SUCCESS:
            self.get_logger().info('Motion planning succeeded.')
        else:
            self.get_logger().error(f'Motion planning failed with error code: {result.error_code.val}')

        self.current_goal_index += 1
        self.send_next_goal()


def main(args=None):
    rclpy.init(args=args)

    file_path = os.path.expanduser('~/joints_config_cylinder.txt')
    joint_positions = parse_txt_file(file_path)

    node = MoveItJointGoalClient(joint_positions)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

