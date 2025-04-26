from setuptools import setup, find_packages

with open('RPG_Dice_Roller/README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='RPG-Dice-Roller',
    version='1.0.1',
    author='Milton Ávila',
    python_requires=">=3.9.4",
    requirements=[
    ],
    license='MIT License',
    packages=find_packages(),
    long_description=description,
    long_description_content_type='text/markdown',
)