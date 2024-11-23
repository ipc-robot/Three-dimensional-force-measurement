from Robotic_Arm.rm_robot_interface import *
import time
import numpy as np

TOOL_FRAME_NAME = "celiji2"
WORK_FRAME_NAME = "sanweili"

class Sensor():
    pass

class Dynamometer():
    pass

def main():
    # 实例化RoboticArm类
    arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
    # 创建机械臂连接，打印连接id
    handle = arm.rm_create_robot_arm("192.168.1.18", 8080)
    print(f"\nhandle id:{handle.id}\n")

    # 设置机械臂为仿真模式
    arm.rm_set_arm_run_mode(1)

    cur_work_frame_name, cur_tool_frame_name = arm.rm_get_current_work_frame()[1].get('name'), arm.rm_get_current_tool_frame()[1].get('name')
    print(f"当前工具坐标系为：{cur_tool_frame_name} \n 当前工作坐标系为：{cur_work_frame_name}")
    
    if cur_work_frame_name == WORK_FRAME_NAME and cur_tool_frame_name == TOOL_FRAME_NAME:
        x_rad_sequence = np.round(np.arange(-0.5, 0.5, 0.1), decimals=10)
        
        for _x_rad in x_rad_sequence:
            print(f"set x rad to {_x_rad}")
            arm.rm_update_work_frame(WORK_FRAME_NAME, [-0.488474, 0.056408, 0.031589, _x_rad, 0, 0])
            arm.rm_movel([0, 0, 0.03, 3.142, 0, 0], 5, 0, 0, 1)
            arm.rm_movel([0, 0, 0, 3.142, 0, 0], 5, 0, 0, 1)
            arm.rm_movel([0, 0, 0.03, 3.142, 0, 0], 5, 0, 0, 1)

            time.sleep(1)

        print('匹配成功，开始三维力测量')

    else:
        print('匹配失败')
    

    # 断开机械臂链接。
    arm.rm_delete_robot_arm()

if __name__ == "__main__":
    main()