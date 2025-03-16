import docx
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DocumentProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Define common skills patterns
        self.skill_patterns = {
            'programming_languages': r'\b(Python|Java|JavaScript|TypeScript|C\+\+|C#|Ruby|PHP|Swift|Kotlin|Go|Rust)\b',
            'web_technologies': r'\b(HTML5|CSS3|React|Angular|Vue\.js|Node\.js|Express|Django|Flask)\b',
            'databases': r'\b(MongoDB|PostgreSQL|MySQL|Redis|SQLite|Oracle|SQL Server)\b',
            'cloud_platforms': r'\b(AWS|Azure|GCP|Google Cloud|Heroku|DigitalOcean)\b',
            'tools': r'\b(Docker|Kubernetes|Jenkins|Git|GitHub|GitLab|Jira|Confluence)\b',
            'concepts': r'\b(CI/CD|REST|GraphQL|Microservices|DevOps|Agile|Scrum)\b'
        }
    
    def read_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            return ' '.join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")

    def read_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return ' '.join(page.extract_text() for page in pdf_reader.pages)
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")

    def extract_skills(self, text):
        """Extract skills from text using regex patterns"""
        skills = set()
        
        # Convert text to lowercase for better matching
        text = text.lower()
        
        # Extract skills using patterns
        for category, pattern in self.skill_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        
        # Look for additional capitalized words that might be technologies
        words = text.split()
        capitalized_words = {word for word in words 
                           if word[0].isupper() and len(word) > 2 
                           and word.isalnum()}
        skills.update(capitalized_words)
        
        return list(skills)

    def calculate_match(self, resume_text, requirements_text):
        """Calculate match between resume and job requirements"""
        try:
            # Calculate text similarity
            text_matrix = self.vectorizer.fit_transform([resume_text, requirements_text])
            content_similarity = cosine_similarity(text_matrix[0:1], text_matrix[1:2])[0][0]
            
            # Extract and compare skills
            resume_skills = set(self.extract_skills(resume_text))
            required_skills = set(self.extract_skills(requirements_text))
            
            matching_skills = resume_skills.intersection(required_skills)
            missing_skills = required_skills - resume_skills
            
            # Calculate skills match percentage
            skills_match_percentage = (len(matching_skills) / len(required_skills)) if required_skills else 0
            
            # Calculate final score (weighted average)
            final_score = (content_similarity * 0.4) + (skills_match_percentage * 0.6)
            
            return {
                'overall_match': round(final_score * 100, 2),
                'content_similarity': round(content_similarity * 100, 2),
                'skills_match_percentage': round(skills_match_percentage * 100, 2),
                'matching_skills': list(matching_skills),
                'missing_skills': list(missing_skills)
            }
            
        except Exception as e:
            raise Exception(f"Error calculating match: {str(e)}")
