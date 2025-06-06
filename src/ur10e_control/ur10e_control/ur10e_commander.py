import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
class UR10eCommander(Node):
    def __init__(self):
        super().__init__('ur10e_commander')
        self.publisher = self.create_publisher(JointTrajectory, '/scaled_joint_trajectory_controller/joint_trajectory', 10)

        timer_period = 2  # seconds
        self.timer = self.create_timer(timer_period, self.send_command)

    def send_command(self):
        traj = JointTrajectory()
        traj.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint',
        ]
        point = JointTrajectoryPoint()
        point.positions = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
        point.time_from_start = Duration(sec=2, nanosec=0)
        traj.points.append(point)

        self.publisher.publish(traj)
        self.get_logger().info('Sent trajectory command')

def main(args=None):
    rclpy.init(args=args)
    node = UR10eCommander()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

