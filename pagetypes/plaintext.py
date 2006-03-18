from common import *
from Products.ZWiki.I18n import _
from Products.ZWiki.pagetypes import registerPageType

class PageTypePlaintext(PageTypeBase):
    _id = 'plaintext'
    _name = 'Plain text'

    def format(self,t):
        return "<pre>\n%s\n</pre>\n" % html_quote(t)

    def preRender(self, page, text=None):
        t = text or page.read()
        t = self.format(t)
        if not text: t += '\n'+MIDSECTIONMARKER
        t = self.protectEmailAddresses(page,t)
        return t

    def render(self, page, REQUEST={}, RESPONSE=None, **kw):
        t = page.preRendered()
        t = page.renderMidsectionIn(t,**kw)
        t = page.addSkinTo(t,**kw)
        return t

registerPageType(PageTypePlaintext)
