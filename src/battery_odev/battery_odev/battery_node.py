import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_srvs.srv import Trigger

class BatteryNode(Node):

    def __init__(self):
        super().__init__('battery_node')

        self.battery_level = 100.0

        self.publisher_ = self.create_publisher(Float32, 'battery_level', 10)
        self.timer_ = self.create_timer(1.0, self.timer_callback)
        self.service_ = self.create_service(Trigger, 'recharge', self.recharge_callback)

    def timer_callback(self):

        if (self.battery_level > 0):
            self.battery_level -= 1

        msg = Float32()
        msg.data = self.battery_level

        self.publisher_.publish(msg)

    def recharge_callback(self, request, response):

        self.battery_level = 100.0

        response.success = True
        response.message = "Pil şarj edildi"

        return response

def main(args=None):
    rclpy.init(args=args)
    battery_node = BatteryNode()
    try:
        rclpy.spin(battery_node)

    except KeyboardInterrupt:
        pass

    finally:
        battery_node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()