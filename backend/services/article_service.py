import httpx
from bs4 import BeautifulSoup

def extract_article_content(url: str = None, text: str = None) -> tuple[str, str]:
    """
    Extracts text and title from either a URL or raw text using BeautifulSoup.
    Returns (content, title).
    """
    if text and not url:
        return text.strip(), "Provided Text Article"
    
    if url:
        try:
            # Basic headers to avoid 403s on some sites
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            # Add verify=False if there are SSL issues, though generally bad practice
            response = httpx.get(url, headers=headers, timeout=15.0, follow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Title extraction
            title = "Extracted Article"
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
                
            # 2. Clean up noise
            for element in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
                element.extract()
                
            # 3. Content extraction - prefer paragraphs
            paragraphs = soup.find_all('p')
            content = "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            # Fallback if no paragraphs
            if len(content) < 100:
                content = soup.get_text(separator='\n\n', strip=True)
                
            return content, title
            
        except httpx.RequestError as e:
            return f"Error reaching the URL: {str(e)}\n\n{text or ''}", "Network Error"
        except Exception as e:
            return f"Error extracting from URL: {str(e)}\n\n{text or ''}", "Extraction Error"
    
    return "", "No Content"
