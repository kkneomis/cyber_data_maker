import random
CORP = {
    "type": "general",
    "options" :
    [
        'What time is the <<staff||production||team||hr||marketing||finance||annual>> meeting?',
        'I am <<really||very||quite||somewhat||especially>> <<happy with||disappointed with||sad about||confused about||content with|| ambivalent about>> your <<performance on||contribution to||opinion of>> the <<Henderson||Michaelson||Strongfellow||Samuelson||Flaherty>> <<account||report||sale||analysis>>.'
    ]
}

def generateEmail(corp=CORP, type='general'):
    options = corp['options']
    opt = random.choice(options)
    while True:
        container = findNextContainer(opt)
        token = findNextToken(opt)
        if token == "":
            break
        else:
            term = selectTerm(token)
            opt = opt.replace(container, term, 1)
    return opt

def findNextContainer(blurb):
    s = blurb.find('<<')
    e = blurb.find('>>')
    if s > -1:
        return (blurb[s:e+2])
    else:
        return ("")

def findNextToken(blurb):
    s = blurb.find('<<')
    e = blurb.find('>>')
    if s > -1:
        return (blurb[s+2:e])
    else:
        return ("")


def selectTerm(token):
    terms = token.split('||')
    term = random.choice(terms)
    return term


generateEmail()

