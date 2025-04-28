from resume_generator import ResumeGenerator

def main():
    # Create a resume generator instance
    generator = ResumeGenerator()

    # Add candidate details
    generator.add_candidate_details(
        name="John Doe",
        email="john@example.com",
        phone="(123) 456-7890",
        location="New York, NY",
        linkedin="linkedin.com/in/johndoe"
    )

    # Add professional summary
    generator.add_summary("""
    - Experienced software engineer with 5+ years in full-stack development
    - Strong background in Python, JavaScript, and cloud technologies
    - Proven track record of delivering scalable solutions
    - Excellent problem-solving and communication skills
    """)

    # Add education
    generator.add_education(
        degree="Master of Science in Computer Science",
        university="Stanford University",
        graduation_year="2020"
    )

    # Add skills
    generator.add_skills({
        "Programming Languages": "Python, JavaScript, Java, C++",
        "Frameworks": "Django, React, Spring Boot",
        "Cloud": "AWS, Azure, Google Cloud",
        "Tools": "Git, Docker, Kubernetes",
        "Databases": "PostgreSQL, MongoDB, Redis"
    })

    # Add experience
    generator.add_experience([
        {
            "company": "Tech Corp",
            "location": "San Francisco, CA",
            "duration": "2020 - Present",
            "position": "Senior Software Engineer",
            "description": [
                "Led development of microservices architecture serving 1M+ users",
                "Implemented CI/CD pipelines reducing deployment time by 50%",
                "Mentored junior developers and conducted code reviews",
                "Optimized database queries improving response time by 40%"
            ],
            "skills": "Python, AWS, Docker, PostgreSQL"
        },
        {
            "company": "StartUp Inc",
            "location": "New York, NY",
            "duration": "2018 - 2020",
            "position": "Software Engineer",
            "description": [
                "Developed and maintained RESTful APIs using Django",
                "Built responsive frontend using React and Material-UI",
                "Implemented automated testing increasing coverage to 85%",
                "Collaborated with product team to deliver features on schedule"
            ],
            "skills": "Python, Django, React, JavaScript"
        }
    ])

    # Generate the resume
    output_file = "example_resume.docx"
    generator.generate(output_file)
    print(f"Resume generated successfully as '{output_file}'")

if __name__ == "__main__":
    main() 