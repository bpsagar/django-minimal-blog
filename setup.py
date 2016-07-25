from setuptools import find_packages, setup

setup(
    name='django-minimal-blog',
    version='1.0.0',
    author='Sagar Chakravarthy',
    author_email='bp.sagar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.9',
        'Markdown>=2.6',
        'docutils>=0.12',
        'jsonfield>=1.0',
        'Pillow>=3.3'
    ],
    zip_safe=False
)
