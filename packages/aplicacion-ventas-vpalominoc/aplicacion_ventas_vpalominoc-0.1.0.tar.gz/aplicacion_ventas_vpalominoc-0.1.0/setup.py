from setuptools import setup,find_packages

setup(
      name='aplicacion_ventas_vpalominoc',
      version='0.1.0',
      author='Veruska Palomino Cisneros',
      author_email='vpalominoc@gmail.com',
      description='Paquete para gestionar ventas, precios, impuestos y descuentos',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown', 
      packages=find_packages(), 
      install_requires=[], 
      classifiers=[
                  'Programming Language :: Python :: 3',
                  'License :: OSI Approved :: MIT License',
                  'Operating System :: OS Independent',
                  ],
      python_requires='>=3.7'
)