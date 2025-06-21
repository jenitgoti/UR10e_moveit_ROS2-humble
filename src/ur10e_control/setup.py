from setuptools import find_packages, setup

package_name = 'ur10e_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jenit',
    maintainer_email='jenit@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ur10e_commander = ur10e_control.ur10e_commander:main',
            'ur10e_movit2 = ur10e_control.ur10e_movit2:main',
            'plane = ur10e_control.plane:main',
            'cylinder = ur10e_control.cylinder:main',
            'part_sphere = ur10e_control.part_sphere:main',
            'hemisphere = ur10e_control.hemisphere:main',
            'marker_publisher = ur10e_control.marker_publisher:main',

        ],
    },
)
