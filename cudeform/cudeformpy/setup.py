from future import standard_library
standard_library.install_aliases()

from distutils.core import setup

setup(name='cudeformpy',
      version='0.0.0',
      author='Jonas Adler',
      author_email='jonasadl@kth.se',
      url='https://github.com/adler-j/cudeform',
      description='Python bindings for the cudeform library',
      license='Proprietary',
      packages=['cudeformpy'],
      package_dir={'cudeformpy': '.'},
      package_data={'cudeformpy': ['*.*']})
