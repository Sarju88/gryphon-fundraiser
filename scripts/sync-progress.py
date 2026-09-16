"""Read public fundraiser totals; preserve the last good data on failure."""
import http.cookiejar
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = 'https://shop.schoolshopping.org/index.asp?PID=152891'

def parse(html):
    def total(class_name):
        block = re.search(r'<div\b[^>]*class="[^"]*\b' + class_name + r'\b[^"]*"[^>]*>(.*?)</div>', html, re.S)
        match = re.search(r'class="tooltipAmt"[^>]*>\s*([\d,]+)\s+Items', block.group(1) if block else '', re.I)
        if not match:
            raise ValueError('Missing or invalid public fundraiser total: ' + class_name)
        return int(match.group(1).replace(',', ''))
    sold, goal = total('tooltipsStuRaised'), total('tooltipsBottomTotGoal')
    if not 0 <= sold <= 1000000 or not 0 < goal <= 1000000:
        raise ValueError('Fundraiser totals out of range')
    return sold, goal

def main():
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    for _ in range(3):
        with opener.open(URL, timeout=30) as response:
            html = response.read().decode('utf-8', errors='replace')
        if 'tooltipsStuRaised' in html:
            break
    sold, goal = parse(html)
    target = Path(__file__).resolve().parents[1] / 'progress.json'
    target.write_text(json.dumps({'sold': sold, 'goal': goal, 'checkedAt': datetime.now(timezone.utc).isoformat(), 'source': URL}, indent=2) + '\n')
    print(f'Public shop totals: {sold} / {goal}')

if __name__ == '__main__':
    main()
