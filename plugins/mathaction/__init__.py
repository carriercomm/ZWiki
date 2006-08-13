###
### Monkey patch to make ZWiki be able to render Latex stuff
### Sean 9.01
### Last Revised: Oct 7, 2005 by Bill Page
### - allow "out of band" content in Pamphlet page type
###

__doc__ = """
LatexWiki __init__.py file docstring
"""

from ReplaceInlineLatex import replaceInlineLatex
from ReplacePamphlet import replacePamphlet
from Products.ZWiki.Utils import html_quote
from Products.ZWiki.pagetypes import registerPageType, registerPageTypeUpgrade
from Products.ZWiki.pagetypes.common import *
from Products.ZWiki.pagetypes.stx import ZwikiStxPageType
#from Products.ZWiki.pagetypes.html import ZwikiHtmlPageType
#from urllib import quote,unquote
from util import defaultcharsizepx, workingDir
#import zLOG
#import re,os,popen2
#itexpath = '/usr/local/bin/itex2MML'

#def initialize(context):
#    """ Initialize LatexWiki """
#
#    # This is so that FileSystemSite can see our images directory.
#    # warning! mkdir here creates an un-writable directory!
#    #try:
#    #    from Products.FileSystemSite.DirectoryView import registerDirectory
#    #    if(not os.access(workingDir, os.F_OK)): 
#    #        os.mkdir(workingDir)
#    #        zLOG.LOG('LatexWiki',zLOG.DEBUG, 'LatexWiki image directory %s created'%(workingDir)) 
#    #    mypaths = os.path.split(workingDir)
#    #    registerDirectory(mypaths[1], mypaths[0])
#    #except ImportError:
#    #    pass

#def runItex(t):
#    i, o = popen2.popen2(itexpath)
#    o.write(t)
#    o.close()
#    t = i.read()
#    return t

### This class supports STX + HTML + LaTeX
#class ZwikiLatexPageType(ZwikiStxPageType):
#    """
#    ZwikiLatexPageType docstring
#    """
#    #_id = 'msgstxprelinkdtmlfitissuehtmllatex'
#    _id = 'stxlatex'
#    _name = 'Structured Text + LaTeX'
#    supportsLaTeX = yes
#    supportsPlone = yes
#
#    def preRender(self, page, text=None):
#        latexTemplate = None
#        latexTemplatePage = getattr(page.folder(),
#                                    'LatexTemplate', None)
#        if latexTemplatePage:
#            latexTemplate = latexTemplatePage.text()
#        t = text or (page.document() + '\n' + MIDSECTIONMARKER + self.preRenderMessages(page))
#        t = page.applyWikiLinkLineEscapesIn(t)
#        # Be more generous in STX for links...so they can contain equations
#        t = re.sub(r'(^| )(?ms)"([^"]*)":(http://[-:A-Za-z0-9_,./\?=@#~&%()]*?)([.!?,;](?= )|(?= )|$)',\
#            r'\1<a href="\3">\2</a>\4',t)
#        # FIXME and the same for WikiLink's (harder)
#        t = replaceInlineLatex(t, getattr(page.folder(),'latex_font_size',defaultcharsizepx), \
#                                  getattr(page.folder(),'latex_align_fudge',0), 
#                                  getattr(page.folder(),'latex_res_fudge',1.03), latexTemplate)
#        t = self.renderStxIn(page, t)
#        if page.usingPurpleNumbers(): t = page.renderPurpleNumbersIn(t)
#        t = page.markLinksIn(t)
#        t = self.protectEmailAddresses(page,t)
#        return '<div class="latexwiki">\n' + t + '\n</div>\n'
#
#    def discussionSeparator(self, page):
#        return '\n\n<a name="comments"></a>\n\n'
#
#    def makeCommentHeading(self, page,
#                           subject, username, time, 
#                           message_id=None,in_reply_to=None):
#        heading = '\n<div class="commentsheading">'
#        if message_id:
#            # use the message id for linking, but strip the <>
#            # and leave it unquoted, browsers can handle it
#            heading += '<a name="msg%s"></a>' % \
#                       re.sub(r'^<(.*)>$',r'\1',message_id)
#        if page.inCMF():
#            heading += \
#              '<img src="discussionitem_icon.gif" style="border:none; margin:0" />'
#        heading += '<b>%s</b> --' % (subject or '...') #more robust
#        if username: heading = heading + '%s, ' % (username)
#        if message_id:
#            heading += ' <a href="%s#msg%s">%s</a>' % \
#                       (page.page_url(),
#                        re.sub(r'^<(.*)>$',r'\1',message_id),
#                        html_quote(time))
#            inreplytobit = '&in_reply_to='+quote(message_id)
#        else:
#            heading += html_quote(time)
#            inreplytobit = ''
#        heading += ' <a href="%s?subject=%s%s#bottom">reply</a>'\
#                   % (page.page_url(),quote(subject or ''),inreplytobit)
#        heading += '</div>'
#        return heading

# This class supports pamphlet (noweb) format for MathAction
# Oct 6, 2005 Bill Page

class ZwikiPamphletPageType(ZwikiStxPageType):
    """
    ZwikiPamphletPageType docstring
    """
    _id = 'stxpamphlet'
    _name = 'Pamphlet'
    supportsLaTeX = yes
    supportsPlone = yes

    def preRender(self, page, text=None):
        t = text or (page.document() + '\n' + MIDSECTIONMARKER + self.preRenderMessages(page))
        (b,t) = replacePamphlet(page,t)
	# Render remaining out-of-band text as stx+latex (axiom version)
        latexTemplate = None
        latexTemplatePage = getattr(page.folder(),
                                    'LatexTemplate', None)
        if latexTemplatePage:
            latexTemplate = latexTemplatePage.text()
        t = replaceInlineLatex(t, getattr(page.folder(),'latex_font_size',defaultcharsizepx), \
                                  getattr(page.folder(),'latex_align_fudge',0), 
                                  getattr(page.folder(),'latex_res_fudge',1.03), latexTemplate)
        t = page.applyWikiLinkLineEscapesIn(t)
        # Be more generous in STX for links...so they can contain equations
        t = re.sub(r'(^| )(?ms)"([^"]*)":(http://[-:A-Za-z0-9_,./\?=@#~&%()]*?)([.!?,;](?= )|(?= )|$)',\
            r'\1<a href="\3">\2</a>\4',t)
        t = self.format(t)
        t = page.markLinksIn(t)
        t = self.protectEmailAddresses(page,t)
        return '<div class="latexwiki">\n' + b + t + '\n</div>\n'

    def discussionSeparator(self, page):
        return '\n\n<a name="comments"></a>\n\n'

    def makeCommentHeading(self, page,
                           subject, username, time, 
                           message_id=None,in_reply_to=None):
        heading = '\n<div class="commentsheading">'
        if message_id:
            # use the message id for linking, but strip the <>
            # and leave it unquoted, browsers can handle it
            heading += '<a name="msg%s"></a>' % \
                       re.sub(r'^<(.*)>$',r'\1',message_id)
        if page.inCMF():
            heading += \
              '<img src="discussionitem_icon.gif" style="border:none; margin:0" />'
        heading += '<b>%s</b> --' % (subject or '...') #more robust
        if username: heading = heading + '%s, ' % (username)
        if message_id:
            heading += ' <a href="%s#msg%s">%s</a>' % \
                       (page.page_url(),
                        re.sub(r'^<(.*)>$',r'\1',message_id),
                        html_quote(time))
            inreplytobit = '&in_reply_to='+quote(message_id)
        else:
            heading += html_quote(time)
            inreplytobit = ''
        heading += ' <a href="%s?subject=%s%s#bottom">reply</a>'\
                   % (page.page_url(),quote(subject or ''),inreplytobit)
        heading += '</div>'
        return heading

# This class supports STX + HTML + LaTeX + Axiom + Reduce for MathAction
# Aug 1, 2005 Bill Page

class ZwikiMathPageType(ZwikiStxPageType):
    """
    ZwikiLatexPageType docstring
    """
    #_id = 'msgstxprelinkdtmlfitissuehtmllatex'
    _id = 'stxmath'
    _name = 'Axiom and Reduce'
    supportsLaTeX = yes
    supportsPlone = yes

    def preRender(self, page, text=None):
	global savePre
	savePre=[]
        reConsts = re.DOTALL+re.MULTILINE

        def hidePre(x):
            global savePre
            savePre.append(x.group(0))
            return '<pre></pre>'

        def restorePre(x):
            global savePre
            first,savePre = savePre[0],savePre[1:]
            return first

        latexTemplate = None
        latexTemplatePage = getattr(page.folder(),
                                    'LatexTemplate', None)
        if latexTemplatePage:
            latexTemplate = latexTemplatePage.text()
        t = text or (page.document() + '\n' + MIDSECTIONMARKER + self.preRenderMessages(page))
        # PROTECT all preformatted areas from LaTeX, Axiom etc.
	savePre=[]
	t = re.sub(r'<pre(?: .*?)?>.*?</pre>',hidePre,t,reConsts)
        t = replaceInlineLatex(t, getattr(page.folder(),'latex_font_size',defaultcharsizepx), \
                                  getattr(page.folder(),'latex_align_fudge',0), 
                                  getattr(page.folder(),'latex_res_fudge',1.03), latexTemplate)
        t = re.sub(r'<pre></pre>',restorePre,t,reConsts)
        # PROTECT all preformatted areas from stx
	savePre=[]
	t = re.sub(r'<pre(?: .*?)?>.*?</pre>',hidePre,t,reConsts)
        t = page.applyWikiLinkLineEscapesIn(t)
        # Be more generous in STX for links...so they can contain equations
        t = re.sub(r'(^| )(?ms)"([^"]*)":(http://[-:A-Za-z0-9_,./\?=@#~&%()]*?)([.!?,;](?= )|(?= )|$)',\
            r'\1<a href="\3">\2</a>\4',t)
        t = self.format(t)
        t = page.markLinksIn(t)
        t = self.protectEmailAddresses(page,t)
        t = re.sub(r'<pre></pre>',restorePre,t,reConsts)
        return '<div class="latexwiki">\n' + t + '\n</div>\n'

    def discussionSeparator(self, page):
        return '\n\n<a name="comments"></a>\n\n'

    def makeCommentHeading(self, page,
                           subject, username, time, 
                           message_id=None,in_reply_to=None):
        heading = '\n<div class="commentsheading">'
        if message_id:
            # use the message id for linking, but strip the <>
            # and leave it unquoted, browsers can handle it
            heading += '<a name="msg%s"></a>' % \
                       re.sub(r'^<(.*)>$',r'\1',message_id)
        if page.inCMF():
            heading += \
              '<img src="discussionitem_icon.gif" style="border:none; margin:0" />'
        heading += '<b>%s</b> --' % (subject or '...') #more robust
        if username: heading = heading + '%s, ' % (username)
        if message_id:
            heading += ' <a href="%s#msg%s">%s</a>' % \
                       (page.page_url(),
                        re.sub(r'^<(.*)>$',r'\1',message_id),
                        html_quote(time))
            inreplytobit = '&in_reply_to='+quote(message_id)
        else:
            heading += html_quote(time)
            inreplytobit = ''
        heading += ' <a href="%s?subject=%s%s#bottom">reply</a>'\
                   % (page.page_url(),quote(subject or ''),inreplytobit)
        heading += '</div>'
        return heading

#class ZwikiHtmlLatexPageType(ZwikiHtmlPageType):
#    """
#    ZwikiHtmlLatexPageType docstring
#    """
#    _id = 'htmllatex'
#    _name = 'HTML + LaTeX'
#    supportsLaTeX = yes
#    supportsHtml = yes
#    supportsDtml = yes
#    supportsPlone = yes
#
#    def preRender(self, page, text=None):
#        latexTemplate = None
#        latexTemplatePage = getattr(page.folder(),
#                                    'LatexTemplate', None)
#        if latexTemplatePage:
#            latexTemplate = latexTemplatePage.text()
#        t = text or (page.document() + '\n' + MIDSECTIONMARKER + self.preRenderMessages(page))
#        t = page.applyWikiLinkLineEscapesIn(t)
#        # Be more generous in STX for links...so they can contain equations
#        t = re.sub(r'(^| )(?ms)"([^"]*)":(http://[-:A-Za-z0-9_,./\?=@#~&%()]*?)([.!?,;](?= )|(?= )|$)',\
#            r'\1<a href="\3">\2</a>\4',t)
#        t = replaceInlineLatex(t, getattr(page.folder(),'latex_font_size',defaultcharsizepx), \
#                                  getattr(page.folder(),'latex_align_fudge',0), 
#                                  getattr(page.folder(),'latex_res_fudge',1.03), latexTemplate)
#        if page.usingPurpleNumbers(): t = page.renderPurpleNumbersIn(t)
#        t = page.markLinksIn(t)
#        t = self.protectEmailAddresses(page,t)
#        return '<div class="latexwiki">\n' + t + '\n</div>\n'
#
#    def discussionSeparator(self, page):
#        return '\n\n<a name="comments"></a>\n\n'
#
#    def makeCommentHeading(self, page,
#                           subject, username, time, 
#                           message_id=None,in_reply_to=None):
#        heading = '\n<div class="commentsheading">'
#        if message_id:
#            # use the message id for linking, but strip the <>
#            # and leave it unquoted, browsers can handle it
#            heading += '<a name="msg%s"></a>' % \
#                       re.sub(r'^<(.*)>$',r'\1',message_id)
#        if page.inCMF():
#            heading += \
#              '<img src="discussionitem_icon.gif" style="border:none; margin:0" />'
#        heading += '<b>%s</b> --' % (subject or '...') #more robust
#        if username: heading = heading + '%s, ' % (username)
#        if message_id:
#            heading += ' <a href="%s#msg%s">%s</a>' % \
#                       (page.page_url(),
#                        re.sub(r'^<(.*)>$',r'\1',message_id),
#                        html_quote(time))
#            inreplytobit = '&in_reply_to='+quote(message_id)
#        else:
#            heading += html_quote(time)
#            inreplytobit = ''
#        heading += ' <a href="%s?subject=%s%s#bottom">reply</a>'\
#                   % (page.page_url(),quote(subject or ''),inreplytobit)
#        heading += '</div>'
#        return heading

#class ZwikiItexPageType(ZwikiHtmlPageType):
#    """
#    ZwikiItexPageType docstring
#    """
#    _id = 'itex'
#    _name = 'iTeX'
#    supportsLaTeX = yes
#    supportsHtml = yes
#    supportsDtml = yes
#    supportsPlone = no # FIXME: For now...must update Plone's page templates for MathML to work.
#
#    def render(self, page, REQUEST={}, RESPONSE=None, **kw):
#        if RESPONSE:
#            RESPONSE['content-type'] = 'application/xhtml+xml'
#        if page.dtmlAllowed() and page.hasDynamicContent():
#            t = page.evaluatePreRenderedAsDtml(page,REQUEST,RESPONSE,**kw)
#        else:
#            t = page.preRendered()
#        t = page.renderMarkedLinksIn(t)
#        t = page.renderMidsectionIn(t)
#        t = page.addSkinTo(t,**kw)
#        return t
#
#    def preRender(self, page, text=None):
#        latexTemplate = None
#        latexTemplatePage = getattr(page.folder(),
#                                    'LatexTemplate', None)
#        if latexTemplatePage:
#            latexTemplate = latexTemplatePage.text()
#        t = text or (page.document() + '\n' + MIDSECTIONMARKER + self.preRenderMessages(page))
#        t = page.applyWikiLinkLineEscapesIn(t)
#        # Be more generous in STX for links...so they can contain equations
#        t = re.sub(r'(^| )(?ms)"([^"]*)":(http://[-:A-Za-z0-9_,./\?=@#~&%()]*?)([.!?,;](?= )|(?= )|$)',\
#            r'\1<a href="\3">\2</a>\4',t)
#        # Run itex to replace any latex with MathML
#        t = runItex(t)
#        # Run replaceInlineLatex to replace anything that itex didn't catch.
#        t = replaceInlineLatex(t, getattr(page.folder(),'latex_font_size',defaultcharsizepx), \
#                                  getattr(page.folder(),'latex_align_fudge',0), 
#                                  getattr(page.folder(),'latex_res_fudge',1.03), latexTemplate)
#        if page.usingPurpleNumbers(): t = page.renderPurpleNumbersIn(t)
#        t = page.markLinksIn(t)
#        t = self.protectEmailAddresses(page,t)
#        return '<div class="latexwiki">\n' + t + '\n</div>\n'
#
#    def discussionSeparator(self, page):
#        return '\n\n<a name="comments"></a>\n\n'
#
#    def makeCommentHeading(self, page,
#                           subject, username, time, 
#                           message_id=None,in_reply_to=None):
#        heading = '\n<div class="commentsheading">'
#        if message_id:
#            # use the message id for linking, but strip the <>
#            # and leave it unquoted, browsers can handle it
#            heading += '<a name="msg%s"></a>' % \
#                       html_quote(re.sub(r'^<(.*)>$',r'\1',message_id))
#        if page.inCMF():
#            heading += \
#              '<img src="discussionitem_icon.gif" style="border:none; margin:0" />'
#        heading += '<b>%s</b> --' % (subject or '...') #more robust
#        if username: heading = heading + '%s, ' % (username)
#        if message_id:
#            heading += ' <a href="'+html_quote('%s#msg%s' % \
#                       (page.page_url(), \
#                        re.sub(r'^<(.*)>$',r'\1',message_id))) \
#                        +'">%s</a>' %(html_quote(time))
#            inreplytobit = quote('&in_reply_to='+message_id)
#        else:
#            heading += html_quote(time)
#            inreplytobit = ''
#        heading += ' <a href=\''+'%s?subject=%s%s#bottom'\
#                   % (page.page_url(),quote(subject or ''),inreplytobit)
#        heading += '\'>reply</a>'
#        heading += '</div>'
#        return heading

## We require ZWiki 0.25 or higher now
#zwiki_min_version = 0.32
#if ZWiki.__version__ >= zwiki_min_version:
#    registerPageTypeUpgrade('msgstxprelinkdtmlfitissuehtmllatex', 'stxlatex')
#    registerPageTypeUpgrade('structuredtextlatex', 'stxlatex')
#    itexmatch = re.match(r'(/(\w+/)+itex2MML)', os.popen('which itex2MML').read())
#    if itexmatch != None: # Found itex
#        itexpath = itexmatch.group(1)
#        registerPageType(ZwikiItexPageType,prepend=1)
#    registerPageType(ZwikiHtmlLatexPageType,prepend=1)
#    registerPageType(ZwikiLatexPageType,prepend=1)
#    registerPageType(ZwikiMathPageType,prepend=1)
#    registerPageType(ZwikiPamphletPageType,prepend=1)
#else:
#    zLOG.LOG('LatexWiki',zLOG.ERROR,'Did not find ZWiki version greater than or equal to %s?'\
#        %(zwiki_min_version))
#    zLOG.log('LatexWiki',zLOG.ERROR,'LatexWiki will not work with your ZWiki.')
#    zLOG.log('LatexWiki',zLOG.ERROR,'Upgrade ZWiki or downgrade LatexWiki.')

registerPageType(ZwikiMathPageType)
registerPageType(ZwikiPamphletPageType)
