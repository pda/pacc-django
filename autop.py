import re

def autop(text):
    '''
    Convert line breaks into <p> and <br> in an intelligent fashion.
    Adapted from Drupal.
    '''
    # All block level tags
    block = '(?:table|thead|tfoot|caption|colgroup|tbody|tr|td|th|div|dl|dd|dt|ul|ol|li|pre|select|form|blockquote|address|p|h[1-6])'

    # Split at <pre>, <script>, <style> and </pre>, </script>, </style> tags.
    # We don't apply any processing to the contents of these tags to avoid messing
    # up code. We look for matched pairs and allow basic nesting. For example:
    # "processed <pre> ignored <script> ignored </script> ignored </pre> processed"
    chunks = re.split(r'(?i)(</?(?:pre|script|style)[^>]*>)', text)
    # Note: PHP ensures the array consists of alternating delimiters and literals
    # and begins and ends with a literal (inserting NULL as required).
    # Also true for Python, which will insert empty strings as required.
    ignore = False
    ignoretag = ''
    output = ''
    for i, chunk in enumerate(chunks):
        if i % 2:
            # Opening or closing tag?
            open = (chunk[1] != '/')
            tag = chunk[2 - open:].split('[ >]', 2)
            if not ignore:
                if open:
                    ignore = True
                    ignoretag = tag
            # Only allow a matching tag to close it.
            elif not open and ignoretag == tag:
                ignore = False
                ignoretag = ''
        elif not ignore:
            chunk = re.sub(r'\n*$', '', chunk) + "\n\n" # just to make things a little easier, pad the end
            chunk = re.sub(r'<br />\s*<br />', r"\n\n", chunk)
            chunk = re.sub(r'(<' + block + '[^>]*>)', r"\n\1", chunk) # Space things out a little
            chunk = re.sub(r'(</' + block + '>)', r"\1\n\n", chunk) # Space things out a little
            chunk = re.sub(r"\n\n+", r"\n\n", chunk) # take care of duplicates
            chunk = re.sub(r'(?s)\n?(.+?)(?:\n\s*\n|\Z)', r"<p>\1</p>\n", chunk) # make paragraphs, including one at the end
            chunk = re.sub(r'<p>\s*</p>\n', r'', chunk) # under certain strange conditions it could create a P of entirely whitespace
            chunk = re.sub(r"<p>(<li.+?)</p>", r"\1", chunk) # problem with nested lists
            chunk = re.sub(r'(?i)<p><blockquote([^>]*)>', r"<blockquote\1><p>", chunk)
            chunk = chunk.replace('</blockquote></p>', r'</p></blockquote>')
            chunk = re.sub(r'<p>\s*(</?' + block + '[^>]*>)', r"\1", chunk)
            chunk = re.sub(r'(</?' + block + '[^>]*>)\s*</p>', r"\1", chunk)
            chunk = re.sub(r'(?<!<br />)\s*\n', r"<br />\n", chunk) # make line breaks
            chunk = re.sub(r'(</?' + block + '[^>]*>)\s*<br />', r"\1", chunk)
            chunk = re.sub(r'<br />(\s*</?(?:p|li|div|th|pre|td|ul|ol)>)', r'\1', chunk)
            chunk = re.sub(r'&([^#])(?![A-Za-z0-9]{1,8};)', r'&amp;\1', chunk)
        output += chunk
    return output

