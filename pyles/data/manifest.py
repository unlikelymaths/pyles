manifest_template = (
    '<Application xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
    '<VisualElements\n'
    '    BackgroundColor="#000000"\n'
    '    ShowNameOnSquare150x150Logo="off"\n'
    '    ForegroundText="light"\n'
    '    Square150x150Logo="icon.jpg"\n'
    '    Square70x70Logo="icon.jpg"/>\n'
    '</Application>\n')

    
def get_manifest(config = {}):
    return manifest_template