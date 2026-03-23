from setuptools import setup
import os
from glob import glob

package_name = 'safety_node2'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Team3',
    maintainer_email='team3@example.com',
    description='Safety node package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'safety_node = safety_node2.safety_node:main',
        ],
    },
)