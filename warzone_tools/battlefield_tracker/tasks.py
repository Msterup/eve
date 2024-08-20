from scraper.extractor import get_web_data
from scraper.parser import consume_web_data

def report_completed_battlefields():
    data = get_web_data()
    result = consume_web_data(data)
    return result # For reporting in admin dashboard

if __name__ == "__main__":
    report_completed_battlefields()