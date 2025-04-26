from setuptools import setup, find_packages

setup(
    name='qris-saweria',
    version='1.0.1',
    description='API tidak resmi saweria.co untuk membuat dan cek QRIS otomatis',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='AutoFTbot',
    author_email='aginazharmhlutpi14@gmail.com',
    url='https://github.com/AutoFTbot/saweria-qris',
    project_urls={
        'Source': 'https://github.com/AutoFTbot/saweria-qris',
        'Donate': 'https://ko-fi.com/FighterTunnel',
    },
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'qrcode',
        'Pillow',
    ],
    python_requires='>=3.7',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
)