import re
from django.shortcuts import render
from django.http import HttpResponse
import io
from api.settings import BASE_DIR

def index(request):
    template = 'index.html'
    context = dict()
    context['data'] = parse_logfile(BASE_DIR / 'static/small.log')
    return render(request, template,context)

def parse_logfile(filename):
    """
    Parses a logfile line by line and extracts data.

    Args:
        filename: The name of the log file to parse.
    """
    data = {
        "block":[],
        "stake":[],
        "trust":[],
        "incentive":[],
        "consensus":[],
        "emission":[],
        "timestamp":[]
    }
    # Open the log file
    try:
        with open(filename, "r",encoding='utf-8') as f:
            # Read the file line by line
            #print('1')
            for line in f:
                #print('2')
                # Clean the line
                clean_line = line.encode('utf-8', 'ignore').decode('utf-8')

                # Regular expression for timestamp (YYYY-MM-DD HH:MM:SS.mmm)
                timestamp_regex = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}'

                # Regular expression for other values
                values_regex = r"Block: (\d+) \| Stake: ([\d.]+) \| Trust: ([\d.]+) \| Consensus: ([\d.]+) \| Incentive: ([\d.]+) \| Emission: ([\d.]+)"

                # Extract values
                match = re.search(values_regex, clean_line)
                # Extract data if there is a match
                if match:
                    # Extract timestamp
                    timestamp_match = re.search(timestamp_regex, clean_line)
                    timestamp = timestamp_match.group(0) if timestamp_match else "Not found"

                    data["timestamp"].append(timestamp)
                    data["block"].append( float(match.group(1)))
                    data["stake"].append( float(match.group(2)))
                    data["trust"].append( float(match.group(3)))
                    data["consensus"].append( float(match.group(4)))
                    data["incentive"].append( float(match.group(5)))
                    data["emission"].append( float(match.group(6)))
    except FileNotFoundError:
        print(f"Error: Log file '{filename}' not found")
    
    return data
