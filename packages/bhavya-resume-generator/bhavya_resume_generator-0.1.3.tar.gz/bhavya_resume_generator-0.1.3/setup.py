from setuptools import setup, find_packages

setup(
    name="bhavya-resume-generator",
    version="0.1.3",
    packages=find_packages(include=['bhavya_resume_generator', 'bhavya_resume_generator.*']),
    include_package_data=True,
    install_requires=[
        "python-docx>=0.8.11",
    ],
    author="Bhavya Gada",
    author_email="your.email@example.com",  # Replace with your email
    description="A Python package to generate professional resumes in Word format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resume-generator",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 