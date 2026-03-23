import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/arc2026/ws/src/safety_node2/install/safety_node2'
