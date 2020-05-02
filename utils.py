import shutil, os, random, json
from jinja2 import Template

#============================================
# Prepare output folder to write actions
#============================================

def set_up_output_dir(OUTPUT_PATH):
    """
    Remove output folder if exists
    Create a new one
    """
    shutil.rmtree(OUTPUT_PATH)
    print('Removed existing output dir...')
    os.mkdir(OUTPUT_PATH)
    print('Created a new output dir...')
    os.mkdir(os.path.join(OUTPUT_PATH, 'emails'))
    print('Created a new emails dir...')


#============================================
# Add metadata for the challenge
#============================================

def add_employee_data(**config):
    """Add employee info to a file in the output"""
    print("Adding employee info to output....")

    hosts = config["company_info"]["employees"]
    with open('output/employees.json', 'w+') as f:
        f.write(json.dumps(hosts, indent=4))


def make_questions(**config):
    """Generate question set"""
    print("Generating questions....")
    with open('config/questions/base.txt') as f:
        text = f.read()
        template = Template(text)

    company = config["company_info"]["company_name"]
    description = config["company_info"]["description"]
    malicious_sender = random.choice(config["mal_config"]["senders"])

    content = template.render(company=company,
                              description=description,
                              malicious_sender=malicious_sender)

    with open('output/prompt.txt', 'w+') as f:
        f.write(content)


def list_to_file(EVENTS, filepath):
    """
    Write an input list of file to disk at specfied filename
    """
    with open(filepath, 'w+') as f:
        for event in EVENTS:
            f.write(event)
            f.write("\n")


