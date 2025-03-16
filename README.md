# Resume Matcher

## Description
Resume Matcher is an intelligent web application that leverages Natural Language Processing (NLP) and Machine Learning techniques to analyze and compare resumes against job requirements. The tool helps job seekers and recruiters by providing a detailed matching analysis, including an overall match percentage and specific skill comparisons.

## Key Features
- **Document Processing**: Supports both PDF and DOCX file formats
- **Intelligent Analysis**: Uses TF-IDF vectorization and cosine similarity for content matching
- **Skill Extraction**: Automatically identifies and extracts technical skills, frameworks, and technologies
- **Interactive UI**: Clean, modern interface with real-time feedback
- **Detailed Results**: 
  - Overall match percentage
  - Matching skills visualization
  - Missing skills identification
  - Content similarity analysis

## Technical Stack
- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **ML/NLP**: scikit-learn, TF-IDF Vectorization
- **Document Processing**: python-docx, PyPDF2
- **Server**: Waitress (Production-grade WSGI server)

## Use Cases
1. **Job Seekers**:
   - Optimize resumes for specific job postings
   - Identify skill gaps for targeted positions
   - Improve application success rate

2. **Recruiters**:
   - Efficiently screen candidates
   - Standardize the initial evaluation process
   - Identify best-matching candidates quickly

3. **Career Counselors**:
   - Guide students/clients on skill development
   - Provide data-driven career advice
   - Help in resume optimization

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the application at `http://localhost:8000`

## How It Works
1. **Upload Documents**: Submit both resume and job requirements in PDF or DOCX format
2. **Processing**: 
   - Documents are parsed and text is extracted
   - Skills are identified using predefined patterns
   - Content similarity is calculated using TF-IDF and cosine similarity
3. **Analysis**:
   - Overall match score is computed using weighted averages
   - Skills are compared and categorized
   - Results are presented in an intuitive interface

## Security Features
- Secure file handling
- Input validation
- File size limitations
- Temporary file cleanup
- Secure filename processing

## Limitations
- Maximum file size: 16MB
- Supported formats: PDF, DOCX
- English language support only
- Basic skill pattern matching

## Future Enhancements
- Multi-language support
- Advanced ML models for better matching
- Custom skill dictionary support
- Batch processing capability
- API integration options
- Resume improvement suggestions
- Export results functionality

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.