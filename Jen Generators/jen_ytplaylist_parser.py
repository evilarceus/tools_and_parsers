# -*- coding: UTF-8 -*-

import os, re, unicodedata, chardet
import dom_parser

class Generator:
    def __init__( self ):
        # create initial variables needed later

        # CHANGEME Set this to the output filename you want/need.
        self.htmlFilename = "test.txt"

        # CHANGEME to match the path needed for your generic fanart to add to each entry. Set to None to not set it.
        # Example: self.fanart = None
        self.fanart = 'https://raw.githubusercontent.com/muaddibttv/tantrumxmls/master/jbuddentv/media/fanart.jpg'

        self.tools_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))

        # generate files
        self._generate_yt_templates()

        # notify user
        print("Finished parsing the html. Output saved as output_html.txt")

    def _generate_yt_templates ( self ):

        print("Reading HTML File.....")
        _path = self.tools_path + os.path.sep + self.htmlFilename
        print(_path)
        fileEncoding = chardet.detect(open(_path, "rb").read())["encoding"]

        try:
            output_string = ''
            
            r = open(_path, encoding=fileEncoding)
            html = r.read()
            the_divs = parseDOM(html, 'div', attrs={'class':'feed-item-dismissable '})
            print('Total Playlists: ' + str(len(the_divs)))
            for the_div in the_divs:
                header = parseDOM(the_div, 'h3', attrs={'class':'yt-lockup-title '})[0]
                link = parseDOM(header, 'a', attrs={'class':'yt-uix-sessionlink.+?'}, ret='href')[0]
                title = parseDOM(header, 'a', attrs={'class':'yt-uix-sessionlink.+?'}, ret='title')[0]
                title = replaceEscapeCodes(title)
                title = replaceHTMLCodes(title).replace('"', '\'')
                title = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
                try:
                    icon = parseDOM(the_div, 'img', attrs={'aria-hidden':'true'}, ret='data-thumb')[0]
                except:
                    icon = parseDOM(the_div, 'img', attrs={'aria-hidden':'true'}, ret='src')[0]

                list = link.split('list=')[1]

                output_string = output_string + '<plugin>\n'
                output_string = output_string + '    <title>' + str(title) + '</title>\n'
                output_string = output_string + '    <link>plugin://plugin.video.youtube/channel/' + str(list) + '/</link>\n'
                output_string = output_string + '    <thumbnail>' + str(icon) + '</thumbnail>\n'
                if not self.fanart == None:
                    output_string = output_string + '    <fanart>' + str(self.fanart) + '</fanart>\n'
                output_string = output_string + '</plugin>\n\n'

        finally:
            # save file
            with open("output_html.txt", "w", encoding=fileEncoding) as f:
                f.write(output_string)

def parseDOM(html, name='', attrs=None, ret=False):
    if attrs: attrs = dict((key, re.compile(value + ('$' if value else ''))) for key, value in attrs.items())
    results = dom_parser.parse_dom(html, name, attrs, ret)
    if ret:
        results = [result.attrs[ret.lower()] for result in results]
    else:
        results = [result.content for result in results]
    return results

def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    import html.parser
    txt = html.parser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.strip()
    return txt

def replaceEscapeCodes(txt):
    import html.parser
    txt = html.parser.HTMLParser().unescape(txt)
    return txt

if ( __name__ == "__main__" ):
    # start
    Generator()