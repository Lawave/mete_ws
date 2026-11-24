import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_srvs.srv import Trigger

class MonitorNode(Node):

    def __init__(self):
        super().__init__('monitor_node')

        self.subscription_ = self.create_subscription(Float32,'battery_level',self.listener_callback,10)
        self.client_ = self.create_client(Trigger, 'recharge')

    def listener_callback(self, msg):

        battery_level = msg.data
        self.get_logger().info(f"Battery Level: {battery_level}")
        if (battery_level < 20):
            self.get_logger().warn("Battery Level Below 20!!")

            if (battery_level < 5):
                self.recharge_battery()

    def recharge_battery(self):

        if not self.client_.service_is_ready():
            self.get_logger().warn("Recharge service is not ready")
            return
        
        request = Trigger.Request()

        future = self.client_.call_async(request)

        future.add_done_callback(self.response_callback)

    def response_callback(self,future):

        response = future.result()
        self.get_logger().info(f"Recharge callback response: {response.message}")


def main(args=None):
    rclpy.init(args=args)
    monitor_node = MonitorNode()
    try:
        rclpy.spin(monitor_node)

    except KeyboardInterrupt:
        pass

    finally:
        monitor_node.destroy_node()
        rclpy.try_shutdown()

    
if __name__ == '__main__':
    main()
